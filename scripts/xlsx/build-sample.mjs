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
	console.error('Aufruf: node build-sample.mjs <ausgabe.xlsx> [praktik=GC,STM] [pflicht=MUSS] [stufe=...] [aufwand=1,2] [ziel=Webserver] [ohne=nein]');
	process.exit(2);
}
const payload = JSON.parse(readFileSync(new URL('../../public/downloads/grundschutzpp-anforderungen.json', import.meta.url), 'utf-8'));
const f = Object.fromEntries(filters.map((s) => [s.split('=')[0], s.split('=')[1].split(',')]));
// Zielobjekt wie auf der Exportseite (ExportTabelle.astro): eine Anforderung gilt für ihre
// Kategorie und die darunter; die ohne Kategorie bleiben dabei, außer bei ohne=nein.
const NO_TARGET = 'Ohne Zielobjektkategorie';
const mitOhne = f.ohne?.[0] !== 'nein';
const trifftZiel = (r) => {
	const ohne = r.zielobjekte.length === 1 && r.zielobjekte[0] === NO_TARGET;
	return [...r.zielobjekte, ...r.unterkategorien].some((t) => f.ziel.includes(t)) || (ohne && mitOhne);
};
const rows = payload.anforderungen.filter(
	(r) =>
		(!f.praktik || f.praktik.includes(r.praktik_id)) &&
		(!f.pflicht || f.pflicht.includes(r.pflichtgrad)) &&
		(!f.stufe || f.stufe.includes(r.stufe)) &&
		(!f.aufwand || f.aufwand.includes(r.aufwand)) &&
		(!f.ziel || trifftZiel(r)),
);
const bytes = buildExportWorkbook(payload, rows, { filterText: filters.join('; ') || undefined, now: new Date('2026-10-28T12:00:00Z') });
writeFileSync(out, bytes);
console.log(`${out}: ${rows.length} Anforderungen, ${bytes.length} Bytes`);
