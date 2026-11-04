import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
import { getCollection } from 'astro:content';

// Welche Seiten es wirklich gibt, getrennt nach Sprache (Dateien unter src/content/docs/ und .../en/),
// nicht nur als Fallback. Dieselbe Quelle wie die Sitemap in astro.config.mjs, nur über die Inhalts-
// Sammlung gelesen.
let sprachen: { de: Set<string>; en: Set<string> } | undefined;
async function vorhandene() {
	if (!sprachen) {
		const de = new Set<string>();
		const en = new Set<string>();
		for (const e of await getCollection('docs')) {
			const id = e.id.replace(/\.mdx?$/, '');
			if (id.startsWith('en/')) en.add(id.slice(3));
			else de.add(id);
		}
		sprachen = { de, en };
	}
	return sprachen;
}

// Fallback-Routen unter /en/ zeigen den deutschen Text einer nicht übersetzten
// Seite. Head.astro setzt dort noindex, Pagefind beachtet das aber nicht und
// würde sie in den englischen Suchindex aufnehmen (Duplicate Content, deutsche
// Treffer in der englischen Suche). `pagefind: false` nimmt den Seiteninhalt
// aus dem Index. Starlight klont die Route-Daten pro Seite, die deutsche Seite
// bleibt davon unberührt.
//
// Zweitens hreflang: Starlight schreibt für jede Seite einen Verweis auf die englische Fassung,
// auch wenn es nur den Fallback gibt. Der zeigt auf eine noindex-Seite; Suchmaschinen ignorieren
// solche Verweise und das Versprechen "hier gibt es Englisch" stimmt nicht. Der Verweis bleibt nur,
// wo es die Übersetzung gibt.
export const onRequest = defineRouteMiddleware(async (context) => {
	const route = context.locals.starlightRoute;
	if (route.isFallback) route.entry.data.pagefind = false;

	const id = route.id.replace(/^en\//, '');
	const { de, en } = await vorhandene();
	// hreflang nur dorthin, wo die Seite existiert: "en" nur mit Übersetzung, "de" und "x-default" nur mit
	// deutscher Fassung (operating-in-germany gibt es nur auf Englisch).
	const erlaubt = (sprache: unknown) => (sprache === 'en' ? en.has(id) : de.has(id));
	route.head = route.head.filter(
		(h) => !(h.tag === 'link' && h.attrs?.rel === 'alternate' && h.attrs?.hreflang && !erlaubt(h.attrs.hreflang)),
	);
});
