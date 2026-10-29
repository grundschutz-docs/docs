// Die Auswahl der Exportseite als Adresse (ADR-0013): lesen, schreiben und unbekannte Werte
// erkennen. Reine Funktionen ohne Seite, damit sie ohne Browser testbar sind.
//
// Warum "unbekannte Werte erkennen": Fehlt ein Wert aus dem Link auf der Seite (das BSI hat eine
// Kategorie umbenannt), bleibt kein Kaestchen angehakt, und nichts angehakt heisst bei dieser
// Seite "keine Einschraenkung". Der Link auf das "Webserver-Paket" liefert dann still den ganzen
// Katalog. Deshalb merkt sich parseQuery, welche Werte es nicht gibt, und die Seite meldet sie.

export const GROUPS = ['praktik', 'pflicht', 'stufe', 'aufwand', 'ziel'] as const;
export type Group = (typeof GROUPS)[number];

export type QueryState = {
	selected: Record<Group, string[]>;
	// Anforderungen ohne Zielobjektkategorie mitnehmen. Standard: ja (Standard 300-1, 3.4.1).
	ohne: boolean;
};

export type ParsedQuery = {
	state: QueryState;
	unknown: Partial<Record<Group, string[]>>;
};

const empty = (): Record<Group, string[]> => ({ praktik: [], pflicht: [], stufe: [], aufwand: [], ziel: [] });

/**
 * Liest die Auswahl aus einer Adresse (`location.search`, mit oder ohne "?").
 * `valid` nennt je Gruppe die Werte, die es auf der Seite gibt. Alles andere landet in `unknown`.
 * `ohne=nein` schaltet die Anforderungen ohne Zielobjektkategorie ab, jeder andere Wert (oder keiner) laesst sie an.
 */
export function parseQuery(search: string, valid: Record<Group, Set<string>>): ParsedQuery {
	const params = new URLSearchParams(search);
	const state: QueryState = { selected: empty(), ohne: params.get('ohne') !== 'nein' };
	const unknown: Partial<Record<Group, string[]>> = {};
	for (const group of GROUPS) {
		const wanted = (params.get(group) ?? '')
			.split(',')
			.map((v) => v.trim())
			.filter(Boolean);
		for (const value of [...new Set(wanted)]) {
			if (valid[group].has(value)) state.selected[group].push(value);
			else (unknown[group] ??= []).push(value);
		}
	}
	return { state, unknown };
}

/**
 * Schreibt die Auswahl als Adressanhang ("" bei leerer Auswahl). Werte werden einzeln kodiert und mit
 * einem Komma verbunden (wie die bestehenden Links von den Praktik-Seiten: `?praktik=GC,STM`);
 * `ohne=nein` steht nur da, wo es etwas aendert, also nur zusammen mit einer Zielobjektkategorie.
 */
export function buildQuery(state: QueryState): string {
	const parts: string[] = [];
	for (const group of GROUPS) {
		const values = state.selected[group];
		if (values.length) parts.push(`${group}=${values.map(encodeURIComponent).join(',')}`);
	}
	if (!state.ohne && state.selected.ziel.length) parts.push('ohne=nein');
	return parts.length ? `?${parts.join('&')}` : '';
}

const LABELS: Record<Group, string> = {
	praktik: 'Praktik',
	pflicht: 'Pflichtgrad',
	stufe: 'Sicherheitsstufe',
	aufwand: 'Aufwand',
	ziel: 'Zielobjektkategorie',
};

/** Der Hinweis, den die Seite zeigt, wenn der Link Werte nennt, die es nicht gibt. "" wenn alles bekannt ist. */
export function unknownMessage(unknown: Partial<Record<Group, string[]>>, state: QueryState): string {
	const parts: string[] = [];
	for (const group of GROUPS) {
		const values = unknown[group];
		if (values?.length) parts.push(`${LABELS[group]} ${values.map((v) => `„${v}“`).join(', ')}`);
	}
	if (!parts.length) return '';
	const keepsFilter = Object.values(state.selected).some((v) => v.length);
	const noZiel = unknown.ziel?.length && !state.selected.ziel.length;
	return (
		`Im Link steht etwas, das es auf dieser Seite nicht (mehr) gibt: ${parts.join('; ')}. Es wird ignoriert.` +
		(noZiel ? ' Ohne gültige Zielobjektkategorie gilt keine Einschränkung nach Kategorie.' : '') +
		(keepsFilter ? '' : ' Es ist nichts ausgewählt, die Zahl unten zeigt deshalb alle Anforderungen.')
	);
}
