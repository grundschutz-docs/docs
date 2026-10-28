// Baut die Excel-Mappe aus den echten Export-Daten und schreibt sie in eine Datei,
// damit scripts/xlsx/verify.py und compare.py sie prüfen können.
//
//   node scripts/xlsx/build-sample.mjs <ausgabe.xlsx> [praktik=GC,STM] [pflicht=MUSS]
//
// Ohne Filter: alle Anforderungen. Filter wirken wie auf der Exportseite
// (kein Häkchen = keine Einschränkung).

import { readFileSync, writeFileSync } from 'node:fs';
import { buildExportWorkbook } from '../../src/lib/xlsx/export-workbook.js';

const [out, ...filters] = process.argv.slice(2);
if (!out) {
	console.error('Aufruf: node build-sample.mjs <ausgabe.xlsx> [praktik=GC,STM] [pflicht=MUSS] [stufe=...] [aufwand=1,2]');
	process.exit(2);
}
const payload = JSON.parse(readFileSync(new URL('../../public/downloads/grundschutzpp-anforderungen.json', import.meta.url), 'utf-8'));
const f = Object.fromEntries(filters.map((s) => [s.split('=')[0], s.split('=')[1].split(',')]));
const rows = payload.anforderungen.filter(
	(r) =>
		(!f.praktik || f.praktik.includes(r.praktik_id)) &&
		(!f.pflicht || f.pflicht.includes(r.pflichtgrad)) &&
		(!f.stufe || f.stufe.includes(r.stufe)) &&
		(!f.aufwand || f.aufwand.includes(r.aufwand)),
);
const bytes = buildExportWorkbook(payload, rows, { filterText: filters.join('; ') || undefined, now: new Date('2026-10-28T12:00:00Z') });
writeFileSync(out, bytes);
console.log(`${out}: ${rows.length} Anforderungen, ${bytes.length} Bytes`);
