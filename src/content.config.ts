import { defineCollection } from 'astro:content';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';

export const collections = {
	docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
	// Sobald `locales` in astro.config.mjs gesetzt ist — hier für `lang: 'de'`,
	// damit das Dokument die richtige Sprache meldet — sucht Starlight nach
	// dieser Sammlung und warnt bei jedem Build, wenn es sie nicht gibt.
	// Sie bleibt vorerst leer: die Übersetzung der Katalog-Inhalte existiert
	// noch nicht (siehe ROADMAP), das Gerüst steht damit aber bereit.
	i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
};
