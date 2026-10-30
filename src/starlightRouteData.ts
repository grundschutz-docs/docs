import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

// Fallback-Routen unter /en/ zeigen den deutschen Text einer nicht übersetzten
// Seite. Head.astro setzt dort noindex, Pagefind beachtet das aber nicht und
// würde sie in den englischen Suchindex aufnehmen (Duplicate Content, deutsche
// Treffer in der englischen Suche). `pagefind: false` nimmt den Seiteninhalt
// aus dem Index. Starlight klont die Route-Daten pro Seite, die deutsche Seite
// bleibt davon unberührt.
export const onRequest = defineRouteMiddleware((context) => {
	const route = context.locals.starlightRoute;
	if (route.isFallback) route.entry.data.pagefind = false;
});
