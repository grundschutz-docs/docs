import { defineCollection, z } from 'astro:content';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';

/**
 * Zusatzfelder für Befunde (ADR-0009), als Erweiterung des docs-Schemas statt
 * als eigene Collection: Ein Befund ist eine ganz normale Seite mit Sidebar,
 * Suche und Anker — er hat nur zusätzliche Angaben, die vor dem Text stehen
 * müssen.
 *
 * Das Schema ist bewusst streng. Ein Register, in dem jemand "status: sollte
 * mal geprüft werden" schreiben kann, verliert genau die Eigenschaft, für die
 * es da ist. Ein Tippfehler bricht den Build, statt still durchzugehen.
 */
const befund = z
	.object({
		/**
		 * Wie belastbar die Aussage ist — die wichtigste Angabe, deshalb
		 * Pflichtfeld. Einen nachprüfbaren Defekt und eine rechtliche
		 * Einschätzung gleich zu präsentieren schadet beiden: die Einschätzung
		 * wirkt fester, als sie ist, der Defekt wird zur Meinung.
		 */
		typ: z.enum(['fakt', 'auslegung', 'beobachtung']),
		/**
		 * Lebenszyklus. "gemeldet" verlangt die Meldeangaben — ein Befund, der
		 * behauptet gemeldet zu sein, muss sagen wo und wann.
		 */
		status: z.enum(['offen', 'gemeldet', 'beantwortet', 'behoben', 'hinfaellig']),
		gefunden: z.date(),
		/** Betroffene Anforderungs- oder Baustein-IDs, für die spätere Verknüpfung. */
		betrifft: z.array(z.string()).default([]),
		/** Wo der Befund nachprüfbar ist: Datei, Dokument oder URL. */
		quelle: z.string().optional(),
		meldung: z
			.object({
				kanal: z.string(),
				datum: z.date(),
				link: z.string().url().optional(),
			})
			.optional(),
	})
	.refine((b) => b.status === 'offen' || b.status === 'hinfaellig' || b.meldung, {
		message:
			'Ab status "gemeldet" braucht der Befund eine meldung (kanal + datum) — sonst behauptet er etwas, das niemand nachvollziehen kann.',
	});

export const collections = {
	docs: defineCollection({
		loader: docsLoader(),
		schema: docsSchema({ extend: z.object({ befund: befund.optional() }) }),
	}),
	// Sobald `locales` in astro.config.mjs gesetzt ist — hier für `lang: 'de'`,
	// damit das Dokument die richtige Sprache meldet — sucht Starlight nach
	// dieser Sammlung und warnt bei jedem Build, wenn es sie nicht gibt.
	// Sie bleibt vorerst leer: die Übersetzung der Katalog-Inhalte existiert
	// noch nicht (siehe ROADMAP), das Gerüst steht damit aber bereit.
	i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
};
