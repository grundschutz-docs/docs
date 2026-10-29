// Die Auswahl der Exportseite als Checkliste fuer Tickets und Wikis (ADR-0013): Markdown und HTML.
// Reine Funktionen ohne Seite, damit sie ohne Browser testbar sind.
//
// Bewusst ohne Volltext der Anforderungen: In einem Ticket waere er unlesbar, und es kaeme BSI-Text in Massen
// dorthin. Jede Zeile verlinkt auf die Seite der Anforderung, dort steht der Text. Am Ende stehen die Quellenzeile
// (CC BY-SA 4.0, wie im Export) und der Link auf genau diese Auswahl, damit der Empfaenger sie live oeffnen kann.

export type ChecklistRow = {
	id: string;
	titel: string;
	praktik_id: string;
	pflichtgrad: string;
	seite: string;
	dokument: string;
};

export type ChecklistContext = {
	// Die Auswahl in Worten ("" = alle Anforderungen).
	auswahl: string;
	// Link auf genau diese Auswahl im Export.
	link: string;
	stand: string;
	// Quellenzeile aus der Datenquelle (BSI, Stand, CC BY-SA 4.0, "bearbeitet von ...").
	quelle: string;
	praktiken: { id: string; titel: string }[];
	// Adresse der Seite ohne Schraegstrich am Ende, fuer die Links auf die Dokument-Seiten.
	siteUrl: string;
};

// Wie tag_slug() im Generator: Umlaute ausgeschrieben, alles andere zu Bindestrichen. Die Dokument-Seiten
// liegen unter diesen Adressen (ADR-0012); ein Test oeffnet die Links aus der Liste.
export function dokumentSlug(name: string): string {
	return name
		.toLowerCase()
		.replace(/ä/g, 'ae')
		.replace(/ö/g, 'oe')
		.replace(/ü/g, 'ue')
		.replace(/ß/g, 'ss')
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-+|-+$/g, '');
}

export type DokumentZahl = { name: string; slug: string; anzahl: number };

/** Die Dokumenttypen, die die Anforderungen der Auswahl nennen, mit Zahl; haeufigste zuerst, dann nach Name. */
export function dokumenteDerAuswahl(rows: ChecklistRow[]): DokumentZahl[] {
	const zaehler = new Map<string, number>();
	for (const r of rows) if (r.dokument) zaehler.set(r.dokument, (zaehler.get(r.dokument) ?? 0) + 1);
	return [...zaehler.entries()]
		.map(([name, anzahl]) => ({ name, slug: dokumentSlug(name), anzahl }))
		.sort((a, b) => b.anzahl - a.anzahl || a.name.localeCompare(b.name, 'de'));
}

type Gruppe = { id: string; titel: string; rows: ChecklistRow[] };

function gruppiere(rows: ChecklistRow[], praktiken: { id: string; titel: string }[]): Gruppe[] {
	const nachId = new Map<string, ChecklistRow[]>();
	for (const r of rows) {
		const liste = nachId.get(r.praktik_id) ?? [];
		liste.push(r);
		nachId.set(r.praktik_id, liste);
	}
	const gruppen: Gruppe[] = [];
	for (const p of praktiken) {
		const liste = nachId.get(p.id);
		if (liste) gruppen.push({ id: p.id, titel: p.titel, rows: liste });
		nachId.delete(p.id);
	}
	// Eine Praktik, die nicht in der Liste steht, geht nicht verloren, sondern kommt hinten an.
	for (const [id, liste] of nachId) gruppen.push({ id, titel: '', rows: liste });
	return gruppen;
}

const md = (s: string) => s.replace(/[\\`*_\[\]<>]/g, '\\$&');
const html = (s: string) =>
	s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const kopf = (rows: ChecklistRow[], ctx: ChecklistContext) =>
	`${rows.length === 1 ? '1 Anforderung' : `${rows.length} Anforderungen`} · Stand ${ctx.stand}`;

export function toMarkdown(rows: ChecklistRow[], ctx: ChecklistContext): string {
	const zeilen: string[] = [
		'## Anforderungspaket Grundschutz++',
		'',
		`**Auswahl:** ${md(ctx.auswahl || 'alle Anforderungen')}`,
		'',
		`${kopf(rows, ctx)} · [Diese Auswahl öffnen](${ctx.link})`,
		'',
	];
	for (const g of gruppiere(rows, ctx.praktiken)) {
		zeilen.push(`### ${md(`${g.id}${g.titel ? ` ${g.titel}` : ''}`)} (${g.rows.length})`, '');
		for (const r of g.rows) {
			const pflicht = r.pflichtgrad === 'MUSS' ? '**MUSS**' : md(r.pflichtgrad);
			zeilen.push(`- [ ] [${r.id}](${r.seite}) · ${md(r.titel)} · ${pflicht}`);
		}
		zeilen.push('');
	}
	const dokumente = dokumenteDerAuswahl(rows);
	if (dokumente.length) {
		zeilen.push(`### Dokumente, die diese Anforderungen nennen (${dokumente.length})`, '');
		for (const d of dokumente) zeilen.push(`- [${md(d.name)}](${ctx.siteUrl}/dokumente/${d.slug}/) (${d.anzahl})`);
		zeilen.push('');
	}
	zeilen.push('---', '', `Quelle: ${ctx.quelle}`, '');
	return zeilen.join('\n');
}

export function toHtml(rows: ChecklistRow[], ctx: ChecklistContext): string {
	const teile: string[] = [
		'<h2>Anforderungspaket Grundschutz++</h2>',
		`<p><strong>Auswahl:</strong> ${html(ctx.auswahl || 'alle Anforderungen')}<br>${html(kopf(rows, ctx))} · <a href="${html(ctx.link)}">Diese Auswahl öffnen</a></p>`,
	];
	for (const g of gruppiere(rows, ctx.praktiken)) {
		teile.push(`<h3>${html(`${g.id}${g.titel ? ` ${g.titel}` : ''}`)} (${g.rows.length})</h3>`, '<ul>');
		for (const r of g.rows) {
			const pflicht = r.pflichtgrad === 'MUSS' ? '<strong>MUSS</strong>' : html(r.pflichtgrad);
			teile.push(`<li><a href="${html(r.seite)}">${html(r.id)}</a> · ${html(r.titel)} · ${pflicht}</li>`);
		}
		teile.push('</ul>');
	}
	const dokumente = dokumenteDerAuswahl(rows);
	if (dokumente.length) {
		teile.push(`<h3>Dokumente, die diese Anforderungen nennen (${dokumente.length})</h3>`, '<ul>');
		for (const d of dokumente) {
			teile.push(`<li><a href="${html(`${ctx.siteUrl}/dokumente/${d.slug}/`)}">${html(d.name)}</a> (${d.anzahl})</li>`);
		}
		teile.push('</ul>');
	}
	teile.push(`<p><small>Quelle: ${html(ctx.quelle)}</small></p>`);
	return teile.join('\n');
}
