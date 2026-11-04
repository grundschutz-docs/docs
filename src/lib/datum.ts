// Datumsdarstellung an einer Stelle. Der Stand des Katalogs gilt für den Tag der Veröffentlichung: es wird nur der
// Datumsteil des ISO-Strings gelesen, keine Zeitzone umgerechnet (eine Umrechnung könnte den Tag verschieben).
// Vorher standen drei gleiche Kopien in id-check.ts, feed.ts und Aenderungsprotokoll.astro.

const MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];

/** "2026-10-30T09:59:42Z" -> "2026-10-30". */
export const tag = (iso: string): string => iso.slice(0, 10);

/** "2026-10-30T09:59:42Z" -> "30. Oktober 2026". */
export function datumDe(iso: string): string {
	const [j, m, t] = tag(iso).split('-').map(Number);
	return `${t}. ${MONATE[m - 1]} ${j}`;
}
