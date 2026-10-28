// Baut aus den Export-Daten (public/downloads/grundschutzpp-anforderungen.json) die
// Excel-Mappe für den Soll-Ist-Abgleich: drei Blätter.
//
//   Anforderungen   eine Zeile je Anforderung, gelbe Spalten für eigene Eingaben
//   Dokumente       welche Dokumente der Katalog verlangt, passend zur Auswahl
//   Info & Lizenz   Datenstand, Urheber, Lizenz, Änderungshinweis, Erklärungen
//
// Alle Texte zu Quelle und Lizenz kommen aus payload.lizenz, das der Generator
// schreibt (scripts/generate_docs.py, export_license). Hier steht kein eigener
// Lizenztext, damit er nicht von LIZENZ.txt abweichen kann.
//
// Die Spalten werden über ihren Namen zugeordnet, nicht über die Position: die
// Arbeitsspalten stehen in Excel weiter links als in der CSV (sonst müsste man für
// einen Status 13 Spalten nach rechts scrollen), und eine neue Spalte im Generator
// darf nichts verschieben.

import { buildXlsx } from './xlsx.js';

// Drei Werte sind die des BSI-Standards 300-1 (4.1.1); "In Umsetzung" ergänzen wir,
// weil der Standard auch Anforderungen kennt, die schon in der Umsetzungsplanung sind.
export const STATUS_VALUES = ['Erfüllt', 'Nicht erfüllt', 'In Umsetzung', 'Nicht anwendbar'];
export const PRESENT_VALUES = ['Ja', 'Teilweise', 'Nein'];

// Reihenfolge und Breite der Spalten im Blatt "Anforderungen".
// Namen müssen zu payload.spalten und payload.arbeitsspalten passen; fehlt einer,
// bricht der Bau ab, statt eine Spalte stillschweigend wegzulassen.
const REQUIREMENT_COLUMNS = [
	{ name: 'ID', width: 11, style: 'bodyNoWrap' },
	{ name: 'Titel', width: 34, style: 'body' },
	{ name: 'Praktik', width: 24, style: 'body' },
	{ name: 'Anforderung', width: 70, style: 'body' },
	{ name: 'Pflichtgrad', width: 11, style: 'center' },
	{ name: 'Aufwand', width: 9, style: 'center' },
	{ name: 'Umsetzungsstatus', width: 17, style: 'input' },
	{ name: 'Verantwortlich', width: 18, style: 'input' },
	{ name: 'Frist', width: 12, style: 'input' },
	{ name: 'Bemerkung', width: 36, style: 'input' },
	{ name: 'Sicherheitsstufe', width: 20, style: 'body' },
	{ name: 'Zielobjektkategorien', width: 28, style: 'body' },
	{ name: 'Gilt auch für Unterkategorien', width: 34, style: 'body' },
	{ name: 'Ergebnis', width: 40, style: 'body' },
	{ name: 'Dokumentiert in', width: 26, style: 'body' },
	{ name: 'Gefährdungen', width: 40, style: 'body' },
	{ name: 'Vorgänger im Kompendium 2023', width: 34, style: 'body' },
	{ name: 'Seite', width: 12, style: 'link' },
	{ name: 'Quelle', width: 40, style: 'bodyNoWrap' },
];

function requirementCell(name, row, payload) {
	switch (name) {
		case 'ID': return row.id;
		case 'Titel': return row.titel;
		case 'Praktik': return row.praktik;
		case 'Anforderung': return row.anforderung;
		case 'Pflichtgrad': return row.pflichtgrad;
		// Aufwand als Zahl, damit Excel danach sortieren und filtern kann.
		case 'Aufwand': return row.aufwand === '' ? null : Number(row.aufwand);
		case 'Sicherheitsstufe': return row.stufe;
		case 'Zielobjektkategorien': return row.zielobjekte.join('; ');
		case 'Gilt auch für Unterkategorien': return row.unterkategorien.join('; ');
		case 'Ergebnis': return row.ergebnis;
		case 'Dokumentiert in': return row.dokument;
		case 'Gefährdungen': return row.gefaehrdungen.join('; ');
		case 'Vorgänger im Kompendium 2023': return row.vorgaenger.join('; ');
		case 'Seite': return { v: 'Zur Seite', link: row.seite };
		case 'Quelle': return payload.quelle;
		default: return null; // Arbeitsspalten: leer, aber gelb hinterlegt
	}
}

function requirementsSheet(payload, rows) {
	const known = new Set([...payload.spalten, ...payload.arbeitsspalten, 'Quelle']);
	const unplaced = [...known].filter((n) => !REQUIREMENT_COLUMNS.some((c) => c.name === n));
	const missing = REQUIREMENT_COLUMNS.filter((c) => !known.has(c.name)).map((c) => c.name);
	if (unplaced.length || missing.length) {
		throw new Error(
			`Spalten passen nicht zusammen (Generator <-> Mappe). Nicht platziert: ${unplaced.join(', ') || '-'}; fehlen in den Daten: ${missing.join(', ') || '-'}`,
		);
	}
	return {
		name: 'Anforderungen',
		tabColor: 'FF4472C4',
		autoFilter: true,
		freeze: { rows: 1, cols: 1 },
		columns: REQUIREMENT_COLUMNS.map((c) => ({ header: c.name, width: c.width, style: c.style })),
		validations: [
			{
				column: REQUIREMENT_COLUMNS.findIndex((c) => c.name === 'Umsetzungsstatus'),
				list: STATUS_VALUES,
				title: 'Umsetzungsstatus',
				message: `Bitte einen der Werte wählen: ${STATUS_VALUES.join(', ')}.`,
			},
		],
		rows: rows.map((row) => REQUIREMENT_COLUMNS.map((c) => requirementCell(c.name, row, payload))),
	};
}

/** Wie zu der Beschreibung eines Dokumenttyps gekommen wurde, in einem Satz. */
export function descriptionNote(doc) {
	if (doc.zuordnung === 'schreibweise') {
		return `Zugeordnet über die Schreibweise: „${doc.bsi_name}“ in der BSI-Tabelle`;
	}
	if (doc.zuordnung === 'exakt') {
		return doc.beschreibung ? '' : 'Die BSI-Tabelle hat dafür noch keine Beschreibung';
	}
	return 'Der Name steht nicht in der BSI-Tabelle, deshalb keine Beschreibung';
}

/**
 * Dokumenttypen, die für die gewählten Zeilen nötig sind: Anzahl und MUSS-Anzahl
 * aus der Auswahl gezählt, Beschreibung, Kategorie und Zielgruppe aus der
 * Dokumenttabelle des BSI (payload.dokumente).
 */
export function documentsForSelection(payload, rows) {
	const order = payload.praktiken.map((p) => p.id);
	const byName = new Map();
	for (const row of rows) {
		if (!row.dokument) continue;
		const e = byName.get(row.dokument) ?? { anzahl: 0, muss: 0, praktiken: new Set() };
		e.anzahl += 1;
		if (row.pflichtgrad === 'MUSS') e.muss += 1;
		e.praktiken.add(row.praktik_id);
		byName.set(row.dokument, e);
	}
	const info = new Map(payload.dokumente.map((d) => [d.dokument, d]));
	return [...byName.entries()]
		.map(([name, e]) => {
			const d = info.get(name);
			if (!d) throw new Error(`Dokumenttyp "${name}" fehlt in payload.dokumente`);
			return { ...d, anzahl: e.anzahl, muss: e.muss, praktiken: [...e.praktiken].sort((a, b) => order.indexOf(a) - order.indexOf(b)) };
		})
		.sort((a, b) => b.anzahl - a.anzahl || a.dokument.localeCompare(b.dokument, 'de'));
}

function documentsSheet(payload, rows) {
	const docs = documentsForSelection(payload, rows);
	const columns = [
		{ header: 'Dokument', width: 34, style: 'body' },
		{ header: 'Anforderungen', width: 15, style: 'center' },
		{ header: 'davon MUSS', width: 12, style: 'center' },
		{ header: 'Praktiken', width: 22, style: 'body' },
		{ header: 'Kategorie', width: 26, style: 'body' },
		{ header: 'Zielgruppe', width: 22, style: 'body' },
		{ header: 'Beschreibung laut BSI-Tabelle', width: 70, style: 'body' },
		{ header: 'Hinweis zur Beschreibung', width: 36, style: 'body' },
		{ header: 'Vorhanden', width: 13, style: 'input' },
		{ header: 'Ablageort', width: 30, style: 'input' },
		{ header: 'Verantwortlich', width: 18, style: 'input' },
		{ header: 'Letzte Prüfung', width: 14, style: 'input' },
		{ header: 'Nächste Prüfung', width: 15, style: 'input' },
	];
	return {
		name: 'Dokumente',
		tabColor: 'FF70AD47',
		autoFilter: true,
		freeze: { rows: 1, cols: 1 },
		columns,
		validations: [
			{ column: 8, list: PRESENT_VALUES, title: 'Vorhanden', message: `Bitte einen der Werte wählen: ${PRESENT_VALUES.join(', ')}.` },
		],
		rows: docs.map((d) => [
			d.dokument, d.anzahl, d.muss, d.praktiken.join(', '), d.kategorie, d.zielgruppe, d.beschreibung, descriptionNote(d),
			null, null, null, null, null,
		]),
	};
}

function infoSheet(payload, rows, opts) {
	const l = payload.lizenz;
	const total = payload.anforderungen.length;
	const now = opts.now ?? new Date();
	const date = `${String(now.getDate()).padStart(2, '0')}.${String(now.getMonth() + 1).padStart(2, '0')}.${now.getFullYear()}`;
	const selection =
		rows.length === total
			? `Alle ${total} Anforderungen`
			: `${rows.length} von ${total} Anforderungen` + (opts.filterText ? ` (Auswahl: ${opts.filterText})` : '');
	const info = (label, value) => [{ v: label, style: 'label' }, value];
	const rowsOut = [
		[{ v: 'Grundschutz++: Anforderungen für den Soll-Ist-Abgleich', style: 'title' }, null],
		[null, null],
		info('Datenstand des Katalogs', l.stand),
		info('Diese Datei enthält', selection),
		info('Erstellt', `am ${date} auf grundschutz-docs.de`),
		[null, null],
		info('Urheber', l.urheber),
		info('Werk', l.werk),
		info('Original', { v: l.original, link: l.original }),
		info('Lizenz', { v: l.lizenz, link: l.lizenz_url }),
		info('Änderungen', l.aenderungen),
		info('Weitergabe', l.weitergabe),
		info('Nicht enthalten', l.nicht_enthalten),
		info('Hinweis', l.hinweis),
		[null, null],
		info('Blatt „Anforderungen“', 'Eine Zeile je Anforderung. Die gelb hinterlegten Spalten (Umsetzungsstatus, Verantwortlich, Frist, Bemerkung) sind für deine Eingaben. Filterpfeile in der Kopfzeile, ID und Kopfzeile bleiben beim Scrollen sichtbar.'),
		info('Blatt „Dokumente“', l.dokumente),
		info('Eigene Werte', l.eigene_werte),
		info('Aufwand', '0 = wird nicht bewertet, 1 = Quick Win (meist am selben Tag), 5 = aufwändig und komplex. Skala des BSI.'),
		info('Zielobjektkategorien', '„Ohne Zielobjektkategorie“ heißt: Die Anforderung gehört nach dem BSI-Standard 300-1 (3.4.1) in jedes Anforderungspaket, unabhängig davon, welche Assets es gibt. Die Spalte „Zielobjektkategorien“ nennt die direkt zugeordnete Kategorie. Der Katalog verlangt in STM.2.1.4.1, dass ein Asset auch die übergeordneten Kategorien erbt; die Spalte „Gilt auch für Unterkategorien“ nennt deshalb die Kategorien darunter, für die die Anforderung ebenfalls gilt. Wer in Excel selbst nach einer Kategorie filtert, braucht beide Spalten. Einfacher ist die Auswahl auf der Exportseite, sie berücksichtigt die Vererbung.'),
	];
	return {
		name: 'Info & Lizenz',
		tabColor: 'FFA5A5A5',
		headerRow: false,
		columns: [{ width: 26, style: 'label' }, { width: 100, style: 'body' }],
		rows: rowsOut,
	};
}

/**
 * @param {object} payload  Inhalt von grundschutzpp-anforderungen.json
 * @param {object[]} rows   die gewählten Anforderungen (Teilmenge von payload.anforderungen)
 * @param {{filterText?: string, now?: Date}} [opts]
 * @returns {Uint8Array}
 */
export function buildExportWorkbook(payload, rows, opts = {}) {
	return buildXlsx({
		properties: {
			title: 'Grundschutz++: Anforderungen für den Soll-Ist-Abgleich',
			creator: 'grundschutz-docs.de',
			created: opts.now,
		},
		sheets: [requirementsSheet(payload, rows), documentsSheet(payload, rows), infoSheet(payload, rows, opts)],
	});
}
