// RSS-Feed des Änderungsprotokolls. Bewusst ohne Paket: ein Feed ist ein kleines XML-Dokument,
// und der klassische Fehler (ein "&" oder "<" im Text, das nicht maskiert ist) lässt sich mit
// einer einzigen Funktion und einem Test (scripts/tests/test_feed.py) abfangen.
//
// Was im Feed steht: nur IDs, Titel-Zahlen und Zählungen, nie der alte oder neue Wortlaut der
// BSI-Texte. Das hält die Einträge kurz und lesbar. Die Zusammenfassung wird aus den Daten
// berechnet, nicht von Hand formuliert: eine Änderung kann mehrere Felder betreffen.

type Feld = { name: string };
type Aenderung = { id: string; titel?: string; praktik?: string; felder: Feld[] };
export type Eintrag = {
	commit: string;
	veroeffentlicht: string;
	neu: unknown[];
	entfernt: unknown[];
	aenderungen: Aenderung[];
};

const MAX_IDS = 12;

// XML 1.0 erlaubt die meisten Steuerzeichen nicht, auch nicht maskiert.
const clean = (s: string) => s.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '');
export const xmlEscape = (s: string) =>
	clean(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const MONTHS = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
// Nur der Datumsteil des ISO-Strings, wie in Aenderungsprotokoll.astro: der Stand gilt für den
// Tag der Veröffentlichung, eine Umrechnung der Zeitzone könnte ihn verschieben.
const dateDe = (iso: string) => {
	const [y, m, d] = iso.slice(0, 10).split('-').map(Number);
	return `${d}. ${MONTHS[m - 1]} ${y}`;
};

const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

// Einträge ohne Änderung (das BSI hat veröffentlicht, am Katalog hat sich nichts geändert)
// sind für Abonnenten Rauschen und stehen nicht im Feed.
export const hasChanges = (e: Eintrag) => e.neu.length + e.entfernt.length + e.aenderungen.length > 0;

export function itemTitle(e: Eintrag) {
	const parts = [];
	if (e.aenderungen.length) parts.push(plural(e.aenderungen.length, 'geänderte Anforderung', 'geänderte Anforderungen'));
	if (e.neu.length) parts.push(plural(e.neu.length, 'neue Anforderung', 'neue Anforderungen'));
	if (e.entfernt.length) parts.push(plural(e.entfernt.length, 'entfernte Anforderung', 'entfernte Anforderungen'));
	return `Katalogstand vom ${dateDe(e.veroeffentlicht)}: ${parts.join(', ')}`;
}

export function itemText(e: Eintrag) {
	const lines: string[] = [];
	if (e.aenderungen.length) {
		const counts = new Map<string, number>();
		for (const a of e.aenderungen) for (const f of a.felder) counts.set(f.name, (counts.get(f.name) ?? 0) + 1);
		const fields = [...counts].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'de')).map(([n, c]) => `${n} (${c}×)`);
		lines.push(`Geänderte Felder: ${fields.join('; ')}.`);
		const ids = e.aenderungen.map((a) => a.id);
		const shown = ids.slice(0, MAX_IDS).join(', ');
		lines.push(`Betroffen: ${shown}${ids.length > MAX_IDS ? ` und ${ids.length - MAX_IDS} weitere` : ''}.`);
	}
	if (e.neu.length) lines.push(`Neu im Katalog: ${e.neu.length}.`);
	if (e.entfernt.length) lines.push(`Aus dem Katalog entfernt: ${e.entfernt.length}.`);
	lines.push(`Quelle: BSI Stand-der-Technik-Bibliothek (CC BY-SA 4.0), Commit ${e.commit.slice(0, 7)}.`);
	return lines.join(' ');
}

// Ein Link je geänderter ID auf die Anforderung (Praktik-Seite mit Anker), mit Titel und den Namen der
// geänderten Felder. Kein alter oder neuer Wortlaut. Der Text hier ist HTML; der Aufrufer maskiert ihn
// noch einmal fürs XML (content:encoded trägt HTML als Text).
export function itemHtml(e: Eintrag, base: string) {
	const rows = e.aenderungen.map((a) => {
		const felder = [...new Set(a.felder.map((f) => f.name))].join(', ');
		const id = a.praktik
			? `<a href="${xmlEscape(base)}/grundschutzpp/${xmlEscape(a.praktik.toLowerCase())}/#${xmlEscape(a.id)}">${xmlEscape(a.id)}</a>`
			: xmlEscape(a.id);
		return `<li>${id}${a.titel ? ` ${xmlEscape(a.titel)}` : ''}: ${xmlEscape(felder)}</li>`;
	});
	const counts: string[] = [];
	if (e.neu.length) counts.push(`${e.neu.length} neu im Katalog`);
	if (e.entfernt.length) counts.push(`${e.entfernt.length} aus dem Katalog entfernt`);
	return [
		`<p>${xmlEscape(itemTitle(e))}.${counts.length ? ` ${xmlEscape(counts.join(', '))}.` : ''}</p>`,
		rows.length ? `<ul>${rows.join('')}</ul>` : '',
		`<p>Alle Änderungen im Wortlaut: <a href="${xmlEscape(base)}/aenderungen/#stand-${e.commit.slice(0, 7)}">Änderungsprotokoll</a>. `,
		`Quelle: BSI Stand-der-Technik-Bibliothek (CC BY-SA 4.0), Commit ${e.commit.slice(0, 7)}.</p>`,
	].join('');
}

export function changelogFeed(entries: Eintrag[], site: string) {
	const base = site.replace(/\/$/, '');
	const shown = entries.filter(hasChanges).sort((a, b) => Date.parse(b.veroeffentlicht) - Date.parse(a.veroeffentlicht));
	// lastBuildDate ist der neueste Eintrag, nicht die Build-Zeit: ein Neubau ohne neuen Stand
	// ändert die Datei nicht, und Reader melden dann nichts.
	const last = shown.length ? new Date(shown[0].veroeffentlicht).toUTCString() : new Date(0).toUTCString();
	const items = shown
		.map(
			(e) => `		<item>
			<title>${xmlEscape(itemTitle(e))}</title>
			<link>${base}/aenderungen/#stand-${e.commit.slice(0, 7)}</link>
			<guid isPermaLink="false">bsi-commit-${e.commit}</guid>
			<pubDate>${new Date(e.veroeffentlicht).toUTCString()}</pubDate>
${[...new Set(e.aenderungen.map((a) => a.praktik).filter(Boolean))].map((k) => `			<category>${xmlEscape(k as string)}</category>\n`).join('')}			<description>${xmlEscape(itemText(e))}</description>
			<content:encoded>${xmlEscape(itemHtml(e, base))}</content:encoded>
		</item>`,
		)
		.join('\n');
	return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
	<channel>
		<title>Grundschutz++ Docs: Änderungen am Katalog</title>
		<link>${base}/aenderungen/</link>
		<atom:link href="${base}/aenderungen/feed.xml" rel="self" type="application/rss+xml" />
		<description>Neue Stände des Grundschutz++-Katalogs und was sich darin geändert hat. Unabhängige, inoffizielle Aufbereitung; maßgeblich ist das BSI-Original. Quelle: BSI Stand-der-Technik-Bibliothek (CC BY-SA 4.0).</description>
		<language>de</language>
		<copyright>Katalogdaten: © BSI-Bund, CC BY-SA 4.0. Unabhängige Aufbereitung, kein Angebot des BSI.</copyright>
		<ttl>1440</ttl>
		<lastBuildDate>${last}</lastBuildDate>
${items}
	</channel>
</rss>
`;
}
