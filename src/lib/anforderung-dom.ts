// Anforderungen auf den Katalogseiten (/grundschutzpp/...): Welche gibt es, und wo steht ihre Pillenzeile?
// Der Generator schreibt je Anforderung eine Überschrift mit der ID als Anker, danach die Pillenzeile
// (p.control-meta). Beide Skripte, die Zeilen anhängen (Kurzlink, "Zuletzt geändert"), brauchen dieselbe Zuordnung.

export type AnforderungImDom = { id: string; titel: string; meta: HTMLElement };

const UEBERSCHRIFT = 'h3[id], h4[id], h5[id]';

export function istKatalogseite(pfad: string = location.pathname): boolean {
	return /^(\/en)?\/grundschutzpp\//.test(pfad);
}

export function anforderungenImDom(): AnforderungImDom[] {
	const out: AnforderungImDom[] = [];
	document.querySelectorAll<HTMLElement>('p.control-meta').forEach((meta) => {
		// Die Überschrift mit der ID steht davor, mit einem Zwischenelement (sr-only-Span).
		let vorher = meta.previousElementSibling;
		while (vorher && !vorher.querySelector(UEBERSCHRIFT)) vorher = vorher.previousElementSibling;
		const h = vorher?.querySelector<HTMLElement>(UEBERSCHRIFT);
		if (!h?.id) return;
		const text = (h.textContent ?? '').trim();
		out.push({ id: h.id, titel: text.startsWith(h.id) ? text.slice(h.id.length).replace(/^\s*[–-]\s*/, '') : text, meta });
	});
	return out;
}
