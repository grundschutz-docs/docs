// Ein kleiner xlsx-Schreiber, nur für das, was die Exportseite braucht: mehrere
// Blätter, Kopfzeile, fixierte Zeilen und Spalten, Autofilter, Dropdown-Listen,
// Hyperlinks, ein paar Zellformate. Kein Lesen, keine Formeln, keine Diagramme.
//
// Warum selbst geschrieben statt exceljs: exceljs kann viel mehr, als wir brauchen,
// hängt 175 Pakete mit an (pnpm audit meldet eine Lücke in einer davon) und wird
// seit 2023 nicht mehr veröffentlicht. Eine xlsx-Datei ist ein ZIP mit XML-Dateien,
// das ZIP macht fflate (null Abhängigkeiten), das XML ist überschaubar.
//
// Der heikle Teil ist die Reihenfolge der XML-Elemente: Excel verlangt sie
// strikt nach dem Schema (ECMA-376, sml.xsd) und meldet sonst "Datei reparieren".
// Deshalb steht in scripts/xlsx/ eine Prüfung, die jede erzeugte Datei gegen das
// Schema validiert, mit LibreOffice öffnet und mit exceljs gegenliest.
//
// Aufbau einer Arbeitsmappe (die Teile, die hier erzeugt werden):
//   [Content_Types].xml          welche Datei welchen Typ hat
//   _rels/.rels                  Einstiegspunkte (Arbeitsmappe, Dokumenteigenschaften)
//   docProps/core.xml, app.xml   Titel, Autor, Erstellungsdatum
//   xl/workbook.xml              die Blätter und ihre Reihenfolge
//   xl/_rels/workbook.xml.rels   welches Blatt in welcher Datei liegt
//   xl/styles.xml                Schriften, Füllungen, Rahmen, Zellformate
//   xl/sharedStrings.xml         jeder Text steht einmal hier, Zellen verweisen darauf
//   xl/worksheets/sheetN.xml     die Zellen eines Blatts, plus Filter und Dropdowns
//   xl/worksheets/_rels/sheetN.xml.rels   Ziele der Hyperlinks dieses Blatts

import { strToU8, zipSync } from 'fflate';

const NS_MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main';
const NS_REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships';
const NS_PKG_REL = 'http://schemas.openxmlformats.org/package/2006/relationships';
const REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships';

const MAX_ROWS = 1048576;
const MAX_COLS = 16384;
const MAX_TEXT = 32767; // Grenze einer Zelle in Excel
const MAX_LIST = 255; // Grenze einer Dropdown-Liste, als Text gerechnet

/**
 * Zellformate nach Namen. Die Nummer ist der Index in cellXfs (styles.xml unten);
 * die Reihenfolge dort muss zu dieser Tabelle passen.
 */
export const STYLE = {
	default: 0,
	header: 1, // fett, hellblau, Rahmen, Zeilenumbruch
	body: 2, // Zeilenumbruch, oben ausgerichtet
	bodyNoWrap: 3, // ohne Umbruch, oben ausgerichtet (Zahlen, IDs)
	link: 4, // blau unterstrichen
	input: 5, // gelb hinterlegt, für eigene Eingaben
	title: 6, // große Überschrift
	label: 7, // fett, oben ausgerichtet
	center: 8, // mittig, oben ausgerichtet (Zahlen, Pflichtgrad)
};

// --- Hilfsfunktionen ---------------------------------------------------------

// Zeichen, die in XML 1.0 nicht vorkommen dürfen, und einzelne Surrogate-Hälften.
// Beides würde Excel als beschädigte Datei melden.
const XML_ILLEGAL = /[\u0000-\u0008\u000B\u000C\u000E-\u001F￾￿]/g;
const LONE_SURROGATE = /[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/g;

export function xmlText(value) {
	return String(value)
		.replace(XML_ILLEGAL, '')
		.replace(LONE_SURROGATE, '�')
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;');
}

/** 0 -> A, 25 -> Z, 26 -> AA ... (Spaltenbuchstaben wie in Excel) */
export function columnLetters(index) {
	let n = index + 1;
	let out = '';
	while (n > 0) {
		const rest = (n - 1) % 26;
		out = String.fromCharCode(65 + rest) + out;
		n = Math.floor((n - 1) / 26);
	}
	return out;
}

const cellRef = (col, row) => `${columnLetters(col)}${row}`;

// Blattnamen: höchstens 31 Zeichen, keine []:*?/\ , nicht mit ' beginnen oder enden,
// und jeder Name nur einmal (ohne Rücksicht auf Groß-/Kleinschreibung).
function checkSheetName(name, seen) {
	if (typeof name !== 'string' || name.length === 0 || name.length > 31) {
		throw new Error(`Blattname "${name}": 1 bis 31 Zeichen nötig`);
	}
	if (/[\[\]:*?/\\]/.test(name)) throw new Error(`Blattname "${name}": enthält ein verbotenes Zeichen`);
	if (name.startsWith("'") || name.endsWith("'")) throw new Error(`Blattname "${name}": darf nicht mit ' beginnen oder enden`);
	if (seen.has(name.toLowerCase())) throw new Error(`Blattname "${name}" kommt doppelt vor`);
	seen.add(name.toLowerCase());
}

const quoteSheet = (name) => `'${name.replace(/'/g, "''")}'`;

// --- Texte (sharedStrings) -----------------------------------------------------

class SharedStrings {
	constructor() {
		this.index = new Map();
		this.list = [];
		this.count = 0;
	}
	add(text) {
		if (text.length > MAX_TEXT) throw new Error(`Zelltext mit ${text.length} Zeichen, erlaubt sind ${MAX_TEXT}`);
		this.count += 1;
		let i = this.index.get(text);
		if (i === undefined) {
			i = this.list.length;
			this.index.set(text, i);
			this.list.push(text);
		}
		return i;
	}
	xml() {
		// xml:space="preserve" nur dort, wo es nötig ist: sonst schneidet Excel führende
		// und abschließende Leerzeichen ab. Das Schema (sml.xsd) kennt das Attribut an
		// <t> nicht, obwohl der Standard es vorsieht und Excel es selbst schreibt;
		// scripts/xlsx/verify.sh nimmt es deshalb vor der Schema-Prüfung heraus.
		const items = this.list
			.map((t) => `<si><t${/^\s|\s$|[\t\n\r]/.test(t) ? ' xml:space="preserve"' : ''}>${xmlText(t)}</t></si>`)
			.join('');
		return (
			`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
			`<sst xmlns="${NS_MAIN}" count="${this.count}" uniqueCount="${this.list.length}">${items}</sst>`
		);
	}
}

// --- Formatvorlagen ------------------------------------------------------------

function stylesXml() {
	const font = (inner) => `<font>${inner}<name val="Calibri"/><family val="2"/></font>`;
	const fonts = [
		font('<sz val="11"/>'), // 0 normal
		font('<b/><sz val="11"/>'), // 1 fett
		font('<u/><sz val="11"/><color rgb="FF0563C1"/>'), // 2 Link
		font('<b/><sz val="14"/>'), // 3 Titel
	];
	const solid = (rgb) =>
		`<fill><patternFill patternType="solid"><fgColor rgb="${rgb}"/><bgColor indexed="64"/></patternFill></fill>`;
	// Die ersten beiden Füllungen sind in jeder Datei Pflicht (keine, gray125).
	const fills = [
		'<fill><patternFill patternType="none"/></fill>',
		'<fill><patternFill patternType="gray125"/></fill>',
		solid('FFD9E2F3'), // 2 Kopfzeile
		solid('FFFFF2CC'), // 3 Eingabe
	];
	const side = (n) => `<${n} style="thin"><color rgb="FFBFBFBF"/></${n}>`;
	const borders = [
		'<border><left/><right/><top/><bottom/><diagonal/></border>',
		`<border>${side('left')}${side('right')}${side('top')}${side('bottom')}<diagonal/></border>`,
	];
	// numFmtId 0 = Standard, fontId/fillId/borderId zeigen in die Listen oben.
	const xf = (fontId, fillId, borderId, align) => {
		const a = align ? `<alignment ${align}/>` : '';
		return (
			`<xf numFmtId="0" fontId="${fontId}" fillId="${fillId}" borderId="${borderId}" xfId="0"` +
			`${fontId ? ' applyFont="1"' : ''}${fillId ? ' applyFill="1"' : ''}${borderId ? ' applyBorder="1"' : ''}` +
			`${align ? ' applyAlignment="1"' : ''}>${a}</xf>`
		);
	};
	const xfs = [
		'<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>', // 0 default
		xf(1, 2, 1, 'vertical="center" wrapText="1"'), // 1 header
		xf(0, 0, 0, 'vertical="top" wrapText="1"'), // 2 body
		xf(0, 0, 0, 'vertical="top"'), // 3 bodyNoWrap
		xf(2, 0, 0, 'vertical="top"'), // 4 link
		xf(0, 3, 1, 'vertical="top" wrapText="1"'), // 5 input
		xf(3, 0, 0, 'vertical="center"'), // 6 title
		xf(1, 0, 0, 'vertical="top" wrapText="1"'), // 7 label
		xf(0, 0, 0, 'horizontal="center" vertical="top"'), // 8 center
	];
	return (
		`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
		`<styleSheet xmlns="${NS_MAIN}">` +
		`<fonts count="${fonts.length}">${fonts.join('')}</fonts>` +
		`<fills count="${fills.length}">${fills.join('')}</fills>` +
		`<borders count="${borders.length}">${borders.join('')}</borders>` +
		`<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>` +
		`<cellXfs count="${xfs.length}">${xfs.join('')}</cellXfs>` +
		`<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>` +
		`<dxfs count="0"/><tableStyles count="0" defaultTableStyle="TableStyleMedium9" defaultPivotStyle="PivotStyleLight16"/>` +
		`</styleSheet>`
	);
}

// --- Ein Blatt -------------------------------------------------------------------

/**
 * @typedef {string|number|null|undefined|{v?: string|number|null, style?: string, link?: string}} Cell
 *
 * @typedef {object} Column
 * @property {string} [header]   Text der Kopfzeile
 * @property {number} [width]    Breite in Zeichen
 * @property {string} [style]    Standardformat der Spalte (Name aus STYLE)
 *
 * @typedef {object} Validation
 * @property {number} column     0-basierter Spaltenindex
 * @property {string[]} list     erlaubte Werte
 * @property {string} [title]    Titel der Fehlermeldung
 * @property {string} [message]  Text der Fehlermeldung
 *
 * @typedef {object} Sheet
 * @property {string} name
 * @property {Column[]} columns
 * @property {Cell[][]} rows
 * @property {boolean} [headerRow=true]   erste Zeile aus den Spaltenüberschriften
 * @property {boolean} [autoFilter=false] Filterpfeile in der Kopfzeile
 * @property {{rows?: number, cols?: number}} [freeze]  fixierte Zeilen/Spalten
 * @property {Validation[]} [validations]
 * @property {string} [tabColor]  ARGB, z. B. "FF4472C4"
 */

function resolveStyle(name) {
	if (name === undefined) return STYLE.default;
	const i = STYLE[name];
	if (i === undefined) throw new Error(`Unbekanntes Zellformat "${name}"`);
	return i;
}

function checkUrl(url) {
	if (!/^https?:\/\/[^\s]+$/i.test(url)) throw new Error(`Hyperlink "${url}": nur http(s)-Adressen erlaubt`);
	return url;
}

function sheetXml(sheet, sst, isFirst) {
	const headerRow = sheet.headerRow !== false;
	const cols = sheet.columns;
	if (cols.length === 0 || cols.length > MAX_COLS) throw new Error(`Blatt "${sheet.name}": ungültige Spaltenzahl`);
	const links = []; // {ref, url}
	const rowXml = [];

	let rowNo = 0;
	if (headerRow) {
		rowNo = 1;
		const cells = cols
			.map((c, i) => `<c r="${cellRef(i, rowNo)}" s="${STYLE.header}" t="s"><v>${sst.add(c.header ?? '')}</v></c>`)
			.join('');
		rowXml.push(`<row r="${rowNo}" ht="32" customHeight="1">${cells}</row>`);
	}

	for (const row of sheet.rows) {
		rowNo += 1;
		if (rowNo > MAX_ROWS) throw new Error(`Blatt "${sheet.name}": mehr als ${MAX_ROWS} Zeilen`);
		if (row.length > cols.length) throw new Error(`Blatt "${sheet.name}", Zeile ${rowNo}: mehr Zellen als Spalten`);
		let cells = '';
		for (let i = 0; i < cols.length; i++) {
			const raw = row[i];
			const spec = raw !== null && typeof raw === 'object' ? raw : { v: raw };
			const styleName = spec.style ?? (spec.link ? 'link' : cols[i].style);
			const s = resolveStyle(styleName);
			const ref = cellRef(i, rowNo);
			const v = spec.v;
			if (spec.link) links.push({ ref, url: checkUrl(spec.link) });
			if (v === null || v === undefined || v === '') {
				// Leere Zelle nur schreiben, wenn sie ein Format trägt (z. B. gelbe Eingabespalte).
				if (s !== STYLE.default) cells += `<c r="${ref}" s="${s}"/>`;
			} else if (typeof v === 'number') {
				if (!Number.isFinite(v)) throw new Error(`Blatt "${sheet.name}", ${ref}: Zahl ist nicht endlich`);
				cells += `<c r="${ref}" s="${s}"><v>${v}</v></c>`;
			} else {
				cells += `<c r="${ref}" s="${s}" t="s"><v>${sst.add(String(v))}</v></c>`;
			}
		}
		rowXml.push(`<row r="${rowNo}">${cells}</row>`);
	}
	const lastRow = Math.max(rowNo, 1);
	const lastCol = columnLetters(cols.length - 1);
	const dimension = `A1:${lastCol}${lastRow}`;

	// sheetPr: Reihenfolge laut Schema tabColor, dann pageSetUpPr.
	const sheetPr =
		`<sheetPr>${sheet.tabColor ? `<tabColor rgb="${sheet.tabColor}"/>` : ''}` + `<pageSetUpPr fitToPage="1"/></sheetPr>`;

	// Fixierte Zeilen/Spalten. Excel erwartet bei state="frozen" die passenden
	// selection-Elemente je Fensterbereich.
	const fr = sheet.freeze?.rows ?? 0;
	const fc = sheet.freeze?.cols ?? 0;
	let pane = '';
	if (fr || fc) {
		const topLeft = cellRef(fc, fr + 1);
		const active = fr && fc ? 'bottomRight' : fr ? 'bottomLeft' : 'topRight';
		pane =
			`<pane${fc ? ` xSplit="${fc}"` : ''}${fr ? ` ySplit="${fr}"` : ''} topLeftCell="${topLeft}" activePane="${active}" state="frozen"/>`;
		if (fr && fc) {
			pane +=
				`<selection pane="topRight"/><selection pane="bottomLeft"/>` +
				`<selection pane="bottomRight" activeCell="${topLeft}" sqref="${topLeft}"/>`;
		} else {
			pane += `<selection pane="${active}" activeCell="${topLeft}" sqref="${topLeft}"/>`;
		}
	}
	const sheetViews =
		`<sheetViews><sheetView${isFirst ? ' tabSelected="1"' : ''} workbookViewId="0">${pane}</sheetView></sheetViews>`;

	// Bei Spalten mit Filterpfeil muss die Überschrift plus Pfeil in die Breite passen:
	// Excel legt den Pfeil über den Text, und ein einzelnes Wort bricht nicht um, sondern
	// wird verdeckt ("Pflichtgrad" erschien als "Pflichtgrac"). Die Pfeilbreite sind rund
	// 3 Zeichen; die Überschrift ist fett und damit etwas breiter als normaler Text.
	const arrow = sheet.autoFilter && headerRow ? 3 : 0;
	const widthOf = (c) => Math.max(c.width ?? 12, c.header && arrow ? Math.ceil(c.header.length * 1.15) + arrow : 0);
	const colXml = cols
		.map((c, i) => `<col min="${i + 1}" max="${i + 1}" width="${widthOf(c)}" customWidth="1"/>`)
		.join('');

	const filterRef = `A1:${lastCol}${lastRow}`;
	const autoFilter = sheet.autoFilter && headerRow ? `<autoFilter ref="${filterRef}"/>` : '';

	let validations = '';
	if (sheet.validations?.length) {
		const firstData = headerRow ? 2 : 1;
		const items = sheet.validations
			.map((v) => {
				if (v.column < 0 || v.column >= cols.length) throw new Error(`Dropdown: Spalte ${v.column} gibt es nicht`);
				if (v.list.some((x) => x.includes(','))) throw new Error('Dropdown-Werte dürfen kein Komma enthalten');
				const formula = v.list.join(',');
				if (formula.length > MAX_LIST) throw new Error(`Dropdown-Liste länger als ${MAX_LIST} Zeichen`);
				const col = columnLetters(v.column);
				const sqref = `${col}${firstData}:${col}${Math.max(lastRow, firstData)}`;
				return (
					`<dataValidation type="list" allowBlank="1" showInputMessage="1" showErrorMessage="1"` +
					` errorTitle="${xmlText(v.title ?? 'Ungültiger Wert')}"` +
					` error="${xmlText(v.message ?? 'Bitte einen Wert aus der Liste wählen.')}" sqref="${sqref}">` +
					`<formula1>"${xmlText(formula)}"</formula1></dataValidation>`
				);
			})
			.join('');
		validations = `<dataValidations count="${sheet.validations.length}">${items}</dataValidations>`;
	}

	const hyperlinks = links.length
		? `<hyperlinks>${links.map((l, i) => `<hyperlink ref="${l.ref}" r:id="rId${i + 1}"/>`).join('')}</hyperlinks>`
		: '';

	// Reihenfolge laut Schema (CT_Worksheet): sheetPr, dimension, sheetViews,
	// sheetFormatPr, cols, sheetData, autoFilter, dataValidations, hyperlinks,
	// pageMargins, pageSetup. Eine andere Reihenfolge meldet Excel als beschädigt.
	const xml =
		`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
		`<worksheet xmlns="${NS_MAIN}" xmlns:r="${NS_REL}">` +
		sheetPr +
		`<dimension ref="${dimension}"/>` +
		sheetViews +
		`<sheetFormatPr defaultRowHeight="15"/>` +
		`<cols>${colXml}</cols>` +
		`<sheetData>${rowXml.join('')}</sheetData>` +
		autoFilter +
		validations +
		hyperlinks +
		`<pageMargins left="0.5" right="0.5" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>` +
		`<pageSetup paperSize="9" orientation="landscape" fitToWidth="1" fitToHeight="0"/>` +
		`</worksheet>`;

	const relsXml = links.length
		? `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
			`<Relationships xmlns="${NS_PKG_REL}">` +
			links
				.map(
					(l, i) =>
						`<Relationship Id="rId${i + 1}" Type="${REL}/hyperlink" Target="${xmlText(l.url)}" TargetMode="External"/>`,
				)
				.join('') +
			`</Relationships>`
		: null;

	return { xml, relsXml, filterRef: autoFilter ? filterRef : null };
}

// --- Die ganze Arbeitsmappe ------------------------------------------------------

/**
 * @param {{sheets: Sheet[], properties?: {title?: string, creator?: string, created?: Date}}} book
 * @returns {Uint8Array} Inhalt der .xlsx-Datei
 */
export function buildXlsx(book) {
	if (!book.sheets?.length) throw new Error('Eine Arbeitsmappe braucht mindestens ein Blatt');
	const seen = new Set();
	book.sheets.forEach((s) => checkSheetName(s.name, seen));

	const sst = new SharedStrings();
	const parts = book.sheets.map((s, i) => sheetXml(s, sst, i === 0));
	const n = book.sheets.length;
	const props = book.properties ?? {};
	const created = (props.created ?? new Date()).toISOString().replace(/\.\d{3}Z$/, 'Z');

	const contentTypes =
		`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
		`<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">` +
		`<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>` +
		`<Default Extension="xml" ContentType="application/xml"/>` +
		`<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>` +
		book.sheets
			.map(
				(_, i) =>
					`<Override PartName="/xl/worksheets/sheet${i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`,
			)
			.join('') +
		`<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>` +
		`<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>` +
		`<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>` +
		`<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>` +
		`</Types>`;

	const rootRels =
		`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
		`<Relationships xmlns="${NS_PKG_REL}">` +
		`<Relationship Id="rId1" Type="${REL}/officeDocument" Target="xl/workbook.xml"/>` +
		`<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>` +
		`<Relationship Id="rId3" Type="${REL}/extended-properties" Target="docProps/app.xml"/>` +
		`</Relationships>`;

	const core =
		`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
		`<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"` +
		` xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"` +
		` xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">` +
		(props.title ? `<dc:title>${xmlText(props.title)}</dc:title>` : '') +
		(props.creator ? `<dc:creator>${xmlText(props.creator)}</dc:creator>` : '') +
		`<dcterms:created xsi:type="dcterms:W3CDTF">${created}</dcterms:created>` +
		`<dcterms:modified xsi:type="dcterms:W3CDTF">${created}</dcterms:modified>` +
		`</cp:coreProperties>`;

	const app =
		`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
		`<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">` +
		`<Application>grundschutz-docs.de</Application></Properties>`;

	// definedNames: Excel legt für jeden Autofilter einen versteckten Namen an.
	// Ohne ihn öffnet die Datei auch, mit ihm entspricht sie dem, was Excel selbst schreibt.
	const definedNames = parts
		.map((p, i) =>
			p.filterRef
				? `<definedName name="_xlnm._FilterDatabase" localSheetId="${i}" hidden="1">${xmlText(
						`${quoteSheet(book.sheets[i].name)}!${p.filterRef.replace(/([A-Z]+)(\d+)/g, '$$$1$$$2')}`,
					)}</definedName>`
				: '',
		)
		.join('');

	const workbook =
		`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
		`<workbook xmlns="${NS_MAIN}" xmlns:r="${NS_REL}">` +
		`<bookViews><workbookView activeTab="0"/></bookViews>` +
		`<sheets>${book.sheets
			.map((s, i) => `<sheet name="${xmlText(s.name)}" sheetId="${i + 1}" r:id="rId${i + 1}"/>`)
			.join('')}</sheets>` +
		(definedNames ? `<definedNames>${definedNames}</definedNames>` : '') +
		`</workbook>`;

	const workbookRels =
		`<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
		`<Relationships xmlns="${NS_PKG_REL}">` +
		book.sheets.map((_, i) => `<Relationship Id="rId${i + 1}" Type="${REL}/worksheet" Target="worksheets/sheet${i + 1}.xml"/>`).join('') +
		`<Relationship Id="rId${n + 1}" Type="${REL}/styles" Target="styles.xml"/>` +
		`<Relationship Id="rId${n + 2}" Type="${REL}/sharedStrings" Target="sharedStrings.xml"/>` +
		`</Relationships>`;

	// [Content_Types].xml zuerst: manche Programme erwarten es am Anfang des ZIP.
	const files = {
		'[Content_Types].xml': strToU8(contentTypes),
		'_rels/.rels': strToU8(rootRels),
		'docProps/core.xml': strToU8(core),
		'docProps/app.xml': strToU8(app),
		'xl/workbook.xml': strToU8(workbook),
		'xl/_rels/workbook.xml.rels': strToU8(workbookRels),
		'xl/styles.xml': strToU8(stylesXml()),
		'xl/sharedStrings.xml': strToU8(sst.xml()),
	};
	parts.forEach((p, i) => {
		files[`xl/worksheets/sheet${i + 1}.xml`] = strToU8(p.xml);
		if (p.relsXml) files[`xl/worksheets/_rels/sheet${i + 1}.xml.rels`] = strToU8(p.relsXml);
	});
	return zipSync(files, { level: 6 });
}
