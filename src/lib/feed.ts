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

type Kanal = { pfad: string; titel: string; beschreibung: string; urheber: string };
type Beitrag = { titel: string; link: string; guid: string; datum: Date; kategorien: string[]; text: string; html: string };

// Der Rahmen beider Feeds. lastBuildDate ist der neueste Eintrag, nicht die Build-Zeit: ein Neubau
// ohne neue Meldung ändert die Datei nicht, und Reader melden dann nichts.
function rss(base: string, kanal: Kanal, beitraege: Beitrag[]) {
	const last = beitraege.length ? beitraege[0].datum : new Date(0);
	const items = beitraege
		.map(
			(b) => `		<item>
			<title>${xmlEscape(b.titel)}</title>
			<link>${xmlEscape(b.link)}</link>
			<guid isPermaLink="false">${xmlEscape(b.guid)}</guid>
			<pubDate>${b.datum.toUTCString()}</pubDate>
${b.kategorien.map((k) => `			<category>${xmlEscape(k)}</category>\n`).join('')}			<description>${xmlEscape(b.text)}</description>
			<content:encoded>${xmlEscape(b.html)}</content:encoded>
		</item>`,
		)
		.join('\n');
	return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
	<channel>
		<title>${xmlEscape(kanal.titel)}</title>
		<link>${base}${kanal.pfad}</link>
		<atom:link href="${base}${kanal.pfad}feed.xml" rel="self" type="application/rss+xml" />
		<description>${xmlEscape(kanal.beschreibung)}</description>
		<language>de</language>
		<copyright>${xmlEscape(kanal.urheber)}</copyright>
		<ttl>1440</ttl>
		<lastBuildDate>${last.toUTCString()}</lastBuildDate>
${items}
	</channel>
</rss>
`;
}

export function changelogFeed(entries: Eintrag[], site: string) {
	const base = site.replace(/\/$/, '');
	const shown = entries.filter(hasChanges).sort((a, b) => Date.parse(b.veroeffentlicht) - Date.parse(a.veroeffentlicht));
	return rss(
		base,
		{
			pfad: '/aenderungen/',
			titel: 'Grundschutz++ Docs: Änderungen am Katalog',
			beschreibung:
				'Neue Stände des Grundschutz++-Katalogs und was sich darin geändert hat. Unabhängige, inoffizielle Aufbereitung; maßgeblich ist das BSI-Original. Quelle: BSI Stand-der-Technik-Bibliothek (CC BY-SA 4.0).',
			urheber: 'Katalogdaten: © BSI-Bund, CC BY-SA 4.0. Unabhängige Aufbereitung, kein Angebot des BSI.',
		},
		shown.map((e) => ({
			titel: itemTitle(e),
			link: `${base}/aenderungen/#stand-${e.commit.slice(0, 7)}`,
			guid: `bsi-commit-${e.commit}`,
			datum: new Date(e.veroeffentlicht),
			kategorien: [...new Set(e.aenderungen.map((a) => a.praktik).filter((k): k is string => !!k))],
			text: itemText(e),
			html: itemHtml(e, base),
		})),
	);
}

// --- Befunde ---------------------------------------------------------------------------------

export type Befund = {
	slug: string;
	titel: string;
	beschreibung: string;
	typ: 'fakt' | 'auslegung' | 'beobachtung';
	status: 'offen' | 'gemeldet' | 'beantwortet' | 'behoben' | 'hinfaellig';
	gefunden: Date;
	behoben?: Date;
	meldung?: { datum: Date; kanal: string };
	betrifft: string[];
};

const TYP = { fakt: 'Fakt', auslegung: 'Auslegung', beobachtung: 'Beobachtung' } as const;
const STATUS = { offen: 'offen', gemeldet: 'gemeldet', beantwortet: 'beantwortet', behoben: 'behoben', hinfaellig: 'hinfällig' } as const;
const tag = (d: Date) => d.toISOString().slice(0, 10);

// Ein Befund erzeugt bis zu drei Meldungen: "Neuer Befund" (gefunden), "gemeldet" (meldung.datum)
// und "behoben" (behoben). Eine Meldung am selben Tag wie der Fund entfällt: sie wäre dieselbe
// Nachricht zweimal, der erste Eintrag nennt den Stand ("bereits behoben", "bereits gemeldet").
// Es gibt nur Daten für das, was im Frontmatter steht; nichts wird aus Git geraten.
export function befundBeitraege(b: Befund, base: string): Beitrag[] {
	const link = `${base}/befunde/${b.slug}/`;
	const mitBetrifft = (kopf: string) => {
		const ids = b.betrifft.length ? ` Betrifft: ${b.betrifft.join(', ')}.` : '';
		return `${kopf} ${b.beschreibung}${ids}`;
	};
	const html = (kopf: string) =>
		`<p>${xmlEscape(kopf)}</p><p>${xmlEscape(b.beschreibung)}</p>` +
		(b.betrifft.length ? `<p>Betrifft: ${b.betrifft.map((i) => `<code>${xmlEscape(i)}</code>`).join(', ')}</p>` : '') +
		`<p><a href="${xmlEscape(link)}">Zum Befund</a></p>`;
	const meldungSpaeter = b.meldung && tag(b.meldung.datum) > tag(b.gefunden) ? b.meldung : undefined;
	const behobenSpaeter = b.behoben && tag(b.behoben) > tag(b.gefunden) ? b.behoben : undefined;

	const stand: string[] = [];
	// "bereits gemeldet" nur, wenn der Befund jetzt wirklich den Status "gemeldet" hat: bei einem eigenen
	// Fehler steht meldung nur, weil das Register sie ab "gemeldet" verlangt, nicht weil jemand etwas meldete.
	if (b.behoben && !behobenSpaeter) stand.push('bereits behoben');
	else if (b.status === 'gemeldet' && b.meldung && !meldungSpaeter) stand.push('bereits gemeldet');
	const zusatz = stand.length ? ` (${stand.join(', ')})` : '';
	const kopfNeu = `Neuer Befund${zusatz}: ${b.titel}`;
	const kat = [TYP[b.typ]];
	const out: Beitrag[] = [
		{
			titel: kopfNeu,
			link,
			guid: `befund-${b.slug}-neu`,
			datum: b.gefunden,
			kategorien: kat,
			text: mitBetrifft(`${TYP[b.typ]}, Status: ${STATUS[b.status]}.`),
			html: html(`${TYP[b.typ]}, Status: ${STATUS[b.status]}.`),
		},
	];
	if (meldungSpaeter) {
		const kopf = `Befund gemeldet: ${b.titel}`;
		out.push({
			titel: kopf,
			link,
			guid: `befund-${b.slug}-gemeldet`,
			datum: meldungSpaeter.datum,
			kategorien: kat,
			text: mitBetrifft(`Gemeldet über: ${meldungSpaeter.kanal}.`),
			html: html(`Gemeldet über: ${meldungSpaeter.kanal}.`),
		});
	}
	if (behobenSpaeter) {
		out.push({
			titel: `Befund behoben: ${b.titel}`,
			link,
			guid: `befund-${b.slug}-behoben`,
			datum: behobenSpaeter,
			kategorien: kat,
			text: mitBetrifft('Die Ursache ist beseitigt.'),
			html: html('Die Ursache ist beseitigt.'),
		});
	}
	return out;
}

export function befundeFeed(befunde: Befund[], site: string) {
	const base = site.replace(/\/$/, '');
	const rang = { neu: 0, gemeldet: 1, behoben: 2 } as const;
	const beitraege = befunde
		.flatMap((b) => befundBeitraege(b, base))
		// Neueste zuerst; am selben Tag eine feste Reihenfolge (Ereignis, dann ID), damit der Feed
		// bei jedem Build gleich aussieht.
		.sort(
			(a, b) =>
				b.datum.getTime() - a.datum.getTime() ||
				rang[a.guid.split('-').pop() as keyof typeof rang] - rang[b.guid.split('-').pop() as keyof typeof rang] ||
				a.guid.localeCompare(b.guid),
		);
	return rss(
		base,
		{
			pfad: '/befunde/',
			titel: 'Grundschutz++ Docs: Befunde',
			beschreibung:
				'Neue Befunde im Register der Unstimmigkeiten im Grundschutz++-Katalog und auf dieser Seite selbst, und wann sie gemeldet oder behoben wurden. Unabhängige, inoffizielle Aufbereitung; maßgeblich ist das BSI-Original.',
			urheber: 'Texte: CC BY 4.0. Katalogdaten: © BSI-Bund, CC BY-SA 4.0. Kein Angebot des BSI.',
		},
		beitraege,
	);
}
