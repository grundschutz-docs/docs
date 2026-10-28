// Gibt alle Zellen einer xlsx-Datei als JSON aus (gelesen mit exceljs), damit
// compare.py sie gegen die CSV des Generators vergleichen kann.
//   XLSX_ORACLE_DIR=/pfad node scripts/xlsx/oracle-dump.mjs datei.xlsx
import { createRequire } from 'node:module';
import { join } from 'node:path';
const require = createRequire(join(process.env.XLSX_ORACLE_DIR, 'package.json'));
const ExcelJS = require('exceljs');
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile(process.argv[2]);
const text = (c) => {
	if (c === null || c === undefined) return null;
	if (typeof c === 'object' && c.richText) return c.richText.map((r) => r.text).join('');
	if (typeof c === 'object' && 'text' in c) return { text: c.text, hyperlink: c.hyperlink ?? null };
	return c;
};
console.log(JSON.stringify(wb.worksheets.map((ws) => ({
	name: ws.name,
	rows: Array.from({ length: ws.rowCount }, (_, i) => ws.getRow(i + 1).values.slice(1).map(text)),
}))));
