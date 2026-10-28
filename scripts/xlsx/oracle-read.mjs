// Liest eine xlsx-Datei mit exceljs und gibt eine Zusammenfassung als JSON aus.
// Dient nur als Gegenprobe in verify.py: exceljs ist ein fremder, weit verbreiteter
// Leser, der unseren Schreiber nicht kennt. Wenn er die Datei anders versteht als
// verify.py (das das XML selbst liest), stimmt etwas nicht.
//
// exceljs liegt bewusst NICHT im Projekt (175 Pakete, eine Sicherheitsmeldung in
// einer Unterabhängigkeit), sondern in einem getrennten Verzeichnis, das über
// XLSX_ORACLE_DIR angegeben wird: pnpm add --save-exact exceljs@4.4.0
//
//   XLSX_ORACLE_DIR=/pfad node scripts/xlsx/oracle-read.mjs datei.xlsx

import { createRequire } from 'node:module';
import { join } from 'node:path';

const dir = process.env.XLSX_ORACLE_DIR;
const file = process.argv[2];
if (!dir || !file) {
	console.error('Aufruf: XLSX_ORACLE_DIR=<Verzeichnis mit node_modules/exceljs> node oracle-read.mjs <datei.xlsx>');
	process.exit(2);
}
const require = createRequire(join(dir, 'package.json'));
const ExcelJS = require('exceljs');

const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile(file);

const out = wb.worksheets.map((ws) => {
	const view = ws.views?.[0] ?? {};
	const validations = [];
	// exceljs legt die Dropdowns je Zelle ab (ws.dataValidations.model: Adresse -> Regel)
	for (const [address, rule] of Object.entries(ws.dataValidations?.model ?? {})) {
		validations.push({ address, type: rule.type, formulae: rule.formulae });
	}
	let hyperlinks = 0;
	ws.eachRow((row) => row.eachCell((cell) => { if (cell.hyperlink) hyperlinks += 1; }));
	return {
		name: ws.name,
		rows: ws.actualRowCount,
		lastRow: ws.rowCount,
		columns: ws.columnCount,
		autoFilter: ws.autoFilter ?? null,
		frozen: view.state === 'frozen' ? { x: view.xSplit ?? 0, y: view.ySplit ?? 0 } : null,
		validations,
		hyperlinks,
		header: ws.getRow(1).values.slice(1).map((v) => (v && v.richText ? v.richText.map((r) => r.text).join('') : v)),
	};
});
console.log(JSON.stringify({ sheets: out }));
