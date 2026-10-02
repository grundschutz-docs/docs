// @ts-check
import { readFileSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import mdx from '@astrojs/mdx';
import { satteri } from '@astrojs/markdown-satteri';

// .env in process.env laden, damit Komponenten (OperatorDetails.astro) sie
// beim Build lesen koennen. Kein vite/dotenv-Import: pnpms striktes
// node_modules verbietet den Zugriff auf nicht direkt deklarierte
// Abhaengigkeiten, deshalb ein minimaler eigener Parser.
//
// Echte Umgebungsvariablen gewinnen gegen die Datei — so kann eine
// Deployment-Plattform (Hetzner, CI) die Werte setzen, ohne dass eine
// .env auf dem Server liegen muss.
function loadEnvFile() {
	let raw;
	try {
		raw = readFileSync(new URL('./.env', import.meta.url), 'utf-8');
	} catch {
		return;
	}
	for (const line of raw.split('\n')) {
		const trimmed = line.trim();
		if (!trimmed || trimmed.startsWith('#')) continue;
		const eq = trimmed.indexOf('=');
		if (eq < 1) continue;
		const key = trimmed.slice(0, eq).trim();
		if (process.env[key] !== undefined) continue;
		process.env[key] = trimmed.slice(eq + 1).trim();
	}
}

loadEnvFile();

const SITE_NAME = process.env.SITE_NAME;

// https://astro.build/config
// Produktionsadresse. Ohne sie überspringt Astro die sitemap.xml still und
// setzt Canonical- und OG-URLs relativ, was beides nutzlos ist. Über
// SITE_URL in .env überschreibbar, damit ein Fork nicht auf diese Domain
// zeigt und eine Staging-Instanz sich selbst kanonisieren kann.
const SITE_URL = process.env.SITE_URL || 'https://grundschutz-docs.de';

export default defineConfig({
	site: SITE_URL,
	markdown: {
		// headingAttributes schaltet die native "# Text {#id .class}"-Syntax
		// des Satteri-Prozessors frei. Katalog- und Gruppen-Ueberschriften
		// nutzen sie fuer eine stabile ID statt Auto-Slug aus dem Titeltext
		// (siehe generate_docs.py, heading_anchor()).
		processor: satteri({ features: { headingAttributes: true } }),
	},
	integrations: [
		starlight({
			title: SITE_NAME || 'Grundschutz++ Docs',
			favicon: '/favicon.svg',
			// src/pages/404.astro ist die eigene 404-Seite; ohne das hier
			// injiziert Starlight zusaetzlich seine eigene unter derselben
			// Route ("/404" doppelt definiert).
			disable404Route: true,
			head: [
				// Apple und ältere Android-Browser nehmen kein SVG als Icon.
				{
					tag: 'link',
					attrs: { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
				},
				// Chromium bevorzugt seit Version 110 bei der Icon-Auswahl eine
				// ICO/PNG mit fester Größe gegenüber der SVG, sobald irgendeine
				// Variante "sizes=any" trägt (Starlights eigener favicon-Tag
				// erzeugt das implizit) — gibt es dann keine echte, erreichbare
				// größenfeste Datei (bei uns: kein favicon.ico), zeigt Chrome
				// gar kein Icon, statt auf die SVG zurückzufallen. Getestet:
				// Edge zeigte deshalb nichts, obwohl favicon.svg selbst korrekt
				// auslieferte. Diese beiden PNGs sind die geforderte feste
				// Rückfalloption.
				{
					tag: 'link',
					attrs: { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
				},
				{
					tag: 'link',
					attrs: { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
				},
				// Vorschaubild beim Teilen (LinkedIn, Mastodon, Slack). Absolute
				// URL ist Pflicht — relative Pfade ignorieren die Crawler.
				{ tag: 'meta', attrs: { property: 'og:image', content: `${SITE_URL}/og.png` } },
				{ tag: 'meta', attrs: { property: 'og:image:width', content: '1200' } },
				{ tag: 'meta', attrs: { property: 'og:image:height', content: '630' } },
				{ tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } },
				{ tag: 'meta', attrs: { name: 'twitter:image', content: `${SITE_URL}/og.png` } },
			],
			description: 'Eigene lesbare Aufbereitung des BSI Grundschutz++ OSCAL-Katalogs',
			locales: {
				root: { label: 'Deutsch', lang: 'de' },
			},
			plugins: [starlightLinksValidator()],
			customCss: ['./src/styles/custom.css'],
			components: {
				ThemeSelect: './src/components/ThemeToggle.astro',
				Hero: './src/components/Hero.astro',
				Footer: './src/components/Footer.astro',
				Banner: './src/components/Banner.astro',
				SocialIcons: './src/components/SocialIcons.astro',
				Header: './src/components/Header.astro',
				Search: './src/components/Search.astro',
			},
			social: [
				{
					icon: 'github',
					label: 'BSI Stand-der-Technik-Bibliothek',
					href: 'https://github.com/BSI-Bund/Stand-der-Technik-Bibliothek',
				},
			],
			sidebar: [
				{
					label: 'Rollen',
					items: [
						{ label: 'Für Geschäftsführung', slug: 'rollen/geschaeftsfuehrung' },
						{ label: 'Für ISB', slug: 'rollen/isb' },
						{ label: 'Für Devs', slug: 'rollen/devs' },
					],
				},
				{
					// Eigene Gruppe, nicht unter Grundschutz++: Befunde sind
					// Kommentar zum Katalog, nicht Teil davon (ADR-0009).
					label: 'Befunde',
					items: [{ autogenerate: { directory: 'befunde' } }],
				},
				{
					label: 'Grundschutz++',
					items: [
						{ label: 'Übersicht', slug: 'grundschutzpp' },
						{ label: 'Status & Zeitplan', slug: 'grundschutzpp/zeitplan' },
						{ label: 'Vergleich: Alt ↔ Neu', slug: 'vergleich' },
						{
							label: 'Managementsystem',
							items: [
								{ label: 'GC Governance und Compliance', slug: 'grundschutzpp/gc' },
								{ label: 'STM Strukturmodellierung', slug: 'grundschutzpp/stm' },
								{ label: 'UMS Umsetzung', slug: 'grundschutzpp/ums' },
								{ label: 'VRB Verbesserung', slug: 'grundschutzpp/vrb' },
								{ label: 'PERF Monitoring-Evaluation', slug: 'grundschutzpp/perf' },
								{ label: 'RISK Risikomanagement', slug: 'grundschutzpp/risk' },
							],
						},
						{
							label: 'Themenfelder',
							items: [
								{ label: 'ASST Informationen und Assets', slug: 'grundschutzpp/asst' },
								{ label: 'PERS Personal', slug: 'grundschutzpp/pers' },
								{ label: 'BES Beschaffungsmanagement', slug: 'grundschutzpp/bes' },
								{ label: 'DLS Dienstleistersteuerung', slug: 'grundschutzpp/dls' },
								{ label: 'TEST Änderungen und Tests', slug: 'grundschutzpp/test' },
								{ label: 'GEB Gebäudemanagement', slug: 'grundschutzpp/geb' },
								{ label: 'SENS Sensibilisierung', slug: 'grundschutzpp/sens' },
								{ label: 'ARCH Architektur', slug: 'grundschutzpp/arch' },
								{ label: 'BER Berechtigung', slug: 'grundschutzpp/ber' },
								{ label: 'NOT Notfallplanung', slug: 'grundschutzpp/not' },
								{ label: 'DET Detektion', slug: 'grundschutzpp/det' },
								{ label: 'REA Sicherheitsvorfallsbehandlung', slug: 'grundschutzpp/rea' },
								{ label: 'KONF Konfiguration', slug: 'grundschutzpp/konf' },
								{ label: 'DEV Entwicklung', slug: 'grundschutzpp/dev' },
							],
						},
					],
				},
			],
		}),
		mdx(),
	],
});
