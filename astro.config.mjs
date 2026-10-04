// @ts-check
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { satteri } from '@astrojs/markdown-satteri';

// Welche Seiten unter /en/ *wirklich* übersetzt sind, statt Starlights
// Fallback-Kopie des deutschen Originals zu zeigen. Von der Dateistruktur
// unter src/content/docs/en/ abgeleitet statt von Hand gepflegt -- aus
// demselben Grund wie TIMELINE in generate_docs.py: eine Liste, die
// unabhaengig vom tatsaechlichen Zustand gepflegt wird, laeuft irgendwann
// auseinander. Treibt unten den Sitemap-Filter: ohne ihn stuenden alle ~130
// Fallback-Seiten (deutscher Inhalt, zufaellig unter einer /en/-URL) als
// angebliche englische Seiten in der Sitemap -- Duplicate Content, den
// Suchmaschinen selbst herausfinden muessten statt dass wir es ihnen sagen.
function translatedEnSlugs() {
	const root = fileURLToPath(new URL('./src/content/docs/en/', import.meta.url));
	const slugs = new Set();
	function walk(dir, prefix) {
		for (const entry of readdirSync(dir, { withFileTypes: true })) {
			if (entry.isDirectory()) {
				walk(`${dir}/${entry.name}`, `${prefix}${entry.name}/`);
				continue;
			}
			const match = entry.name.match(/^(.*)\.mdx?$/);
			if (!match) continue;
			const base = match[1] === 'index' ? '' : match[1];
			slugs.add(`${prefix}${base}`.replace(/\/$/, ''));
		}
	}
	walk(root, '');
	return slugs;
}
const TRANSLATED_EN_SLUGS = translatedEnSlugs();

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

// Plausible-Einbindung ist komplett env-gesteuert, aus demselben Grund wie
// die OPERATOR_*-Werte: ein Fork soll nicht automatisch Traffic an die
// Analytics-Instanz des Original-Betreibers melden. Ohne PLAUSIBLE_SCRIPT_URL
// wird gar kein Script eingebunden. PLAUSIBLE_DOMAIN ist optional und nur für
// den Fall gedacht, dass der "data-domain"-Wert vom SITE_URL-Host abweichen
// soll (z. B. mehrere Domains auf eine Plausible-Site gemappt).
const PLAUSIBLE_SCRIPT_URL = process.env.PLAUSIBLE_SCRIPT_URL?.trim();
const PLAUSIBLE_DOMAIN = process.env.PLAUSIBLE_DOMAIN?.trim() || new URL(SITE_URL).hostname;

// Sitewide WebSite-Schema (JSON-LD) fuer Google & Co. Bewusst eng geschnitten:
// - Kein sameAs/publisher-Bezug zum BSI -- diese Seite ist kein offizielles
//   BSI-Angebot (siehe ueber.mdx, impressum.mdx), das Schema darf diese
//   Trennung nicht verwischen. Es beschreibt nur die Website selbst.
// - publisher nur, wenn OPERATOR_NAME tatsaechlich gesetzt ist, aus demselben
//   Grund wie bei OperatorDetails.astro: ein ungesetzter Platzhalter-String
//   wie "[Name]" darf nicht in maschinenlesbare Daten durchsickern.
// - Kein potentialAction/SearchAction: Pagefind laeuft rein im Browser, es
//   gibt keine crawlbare Such-URL mit Query-Parameter, die dieses Schema
//   wahrheitsgemaess beschreiben koennte.
const OPERATOR_NAME = process.env.OPERATOR_NAME?.trim();
const WEBSITE_JSONLD = {
	'@context': 'https://schema.org',
	'@type': 'WebSite',
	name: SITE_NAME || 'Grundschutz++ Docs',
	url: SITE_URL,
	description: 'Eigene lesbare Aufbereitung des BSI Grundschutz++ OSCAL-Katalogs',
	inLanguage: 'de',
	...(OPERATOR_NAME ? { publisher: { '@type': 'Organization', name: OPERATOR_NAME } } : {}),
};

// Google-Search-Console-Verifizierung per Meta-Tag, als Alternative zur
// DNS-TXT-Methode. Env-gesteuert wie PLAUSIBLE_SCRIPT_URL: ohne gesetzten
// Code kein Tag, damit ein Fork nicht versehentlich die GSC-Property des
// Original-Betreibers zu verifizieren versucht.
const GOOGLE_SITE_VERIFICATION = process.env.GOOGLE_SITE_VERIFICATION?.trim();

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
				// WebSite-Schema fuer alle Seiten identisch -- siehe Kommentar bei
				// der Konstante weiter oben zu den bewussten Auslassungen.
				{
					tag: 'script',
					attrs: { type: 'application/ld+json' },
					content: JSON.stringify(WEBSITE_JSONLD),
				},
				// Nur vorhanden, wenn GOOGLE_SITE_VERIFICATION gesetzt ist -- siehe
				// Kommentar bei der Konstante weiter oben.
				...(GOOGLE_SITE_VERIFICATION
					? [
							{
								tag: 'meta',
								attrs: { name: 'google-site-verification', content: GOOGLE_SITE_VERIFICATION },
							},
						]
					: []),
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
				// Nur vorhanden, wenn PLAUSIBLE_SCRIPT_URL gesetzt ist -- siehe
				// Kommentar bei der Konstante weiter oben. Der zweite Tag ist
				// Plausibles Event-Queue-Shim: ohne ihn würfe ein plausible(...)-Aufruf,
				// der vor dem Laden des (deferred) Hauptscripts passiert, einen Fehler.
				// Aktuell rufen wir plausible() selbst nirgends manuell auf, aber die
				// erweiterten Script-Varianten (file-downloads, outbound-links, ...)
				// nutzen dieselbe Queue intern -- Plausibles eigener Installations-
				// Assistent liefert ihn deshalb standardmäßig mit.
				...(PLAUSIBLE_SCRIPT_URL
					? [
							{
								tag: 'script',
								attrs: {
									defer: true,
									'data-domain': PLAUSIBLE_DOMAIN,
									src: PLAUSIBLE_SCRIPT_URL,
								},
							},
							{
								tag: 'script',
								content:
									"window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }",
							},
						]
					: []),
			],
			description: 'Eigene lesbare Aufbereitung des BSI Grundschutz++ OSCAL-Katalogs',
			locales: {
				root: { label: 'Deutsch', lang: 'de' },
				en: { label: 'English', lang: 'en' },
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
				Head: './src/components/Head.astro',
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
		// Eigene statt Starlights automatisch zugeschaltete sitemap-Integration
		// (siehe node_modules/@astrojs/starlight/dist/integrations/sitemap.js --
		// sie tritt nur zurueck, wenn "@astrojs/sitemap" schon im integrations-
		// Array steht). Noetig fuer den filter: ohne ihn landen alle ~130
		// deutschen Fallback-Seiten unter /en/... in der Sitemap, als gaebe es
		// dort echten englischen Inhalt.
		sitemap({
			i18n: {
				defaultLocale: 'root',
				locales: { root: 'de', en: 'en' },
			},
			filter: (page) => {
				const path = new URL(page).pathname;
				if (!path.startsWith('/en/') && path !== '/en') return true;
				const slug = path.replace(/^\/en\/?/, '').replace(/\/$/, '');
				return TRANSLATED_EN_SLUGS.has(slug);
			},
		}),
	],
});
