// @ts-check
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { satteri } from '@astrojs/markdown-satteri';

/**
 * @param {string} file relativ zu dieser Datei
 * @param {(data: any) => string | undefined} pick
 */
const dataDate = (file, pick) => {
	try {
		return pick(JSON.parse(readFileSync(new URL(file, import.meta.url), 'utf-8')));
	} catch {
		return undefined;
	}
};
/** @type {Record<string, string | undefined>} */
const LASTMOD = {
	// "stand" der Export-Daten ist der Katalogstand als TT.MM.JJJJ
	'/export/': dataDate('./public/downloads/grundschutzpp-anforderungen.json', (d) => {
		const [day, month, year] = String(d.stand).split('.');
		return year && month && day ? `${year}-${month}-${day}` : undefined;
	}),
	'/aenderungen/': dataDate('./src/data/changelog.json', (d) => d.stand?.veroeffentlicht?.slice(0, 10)),
};

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
				// Das sitewide WebSite-JSON-LD sitzt in Head.astro statt hier --
				// dieses Array ist pro Locale identisch, das Schema darf es nicht
				// sein (inLanguage/description muessen zur jeweiligen Seite passen).
				//
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
				// Download-Links unter /downloads/ (Export-CSV): Plausibles file-downloads-
				// Skript fängt solche Klicks ab, unterbindet das normale Verhalten und
				// navigiert danach selbst per window.location zur Datei. Dabei geht das
				// download-Attribut verloren, und der Browser zeigt eine CSV als Text, statt
				// sie zu speichern. Dieser Handler läuft in der Capture-Phase vor dem von
				// Plausible, stoppt die Weitergabe, lässt dem Browser aber sein Speichern
				// und meldet das Ereignis selbst (gleicher Name und gleiche Eigenschaft wie
				// Plausibles eigener Aufruf, die Download-Zählung bleibt also vergleichbar).
				// Ohne Plausible (Forks) ist er harmlos: window.plausible fehlt dann einfach.
				{
					tag: 'script',
					content:
						"document.addEventListener('click',function(e){var a=e.target&&e.target.closest&&e.target.closest('a[download]');if(!a||a.origin!==location.origin||a.pathname.indexOf('/downloads/')!==0)return;e.stopPropagation();if(window.plausible)window.plausible('File Download',{props:{url:a.href}})},true)",
				},
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
			routeMiddleware: './src/starlightRouteData.ts',
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
				LanguageSelect: './src/components/LanguageSelect.astro',
			},
			social: [
				{
					icon: 'github',
					label: 'Grundschutz++ Docs on GitHub',
					href: 'https://github.com/grundschutz-docs/docs',
				},
			],
			sidebar: [
				{
					label: 'Rollen',
					translations: { en: 'Roles' },
					items: [
						{ label: 'Für Geschäftsführung', translations: { en: 'For management' }, slug: 'rollen/geschaeftsfuehrung' },
						{ label: 'Für ISB', translations: { en: 'For the information security officer (ISB)' }, slug: 'rollen/isb' },
						{ label: 'Für Devs', translations: { en: 'For developers' }, slug: 'rollen/devs' },
					],
				},
				{
					// Eigene Gruppe, nicht unter Grundschutz++: Befunde sind
					// Kommentar zum Katalog, nicht Teil davon (ADR-0009).
					label: 'Befunde',
					translations: { en: 'Findings' },
					items: [{ autogenerate: { directory: 'befunde' } }],
				},
				{
					// Eigene Gruppe: RAG ist ein Werkzeug auf dem Katalog, nicht Teil
					// des Katalogs. Die Übersetzung steht hier, weil die Gruppe sonst
					// unter /en/ mit deutschem Namen erscheint.
					label: 'Daten & Werkzeuge',
					translations: { en: 'Data & tools' },
					items: [
						{ label: 'Export für Excel', translations: { en: 'Excel export (German)' }, slug: 'export' },
						{ label: 'Katalog für Sprachmodelle (RAG)', translations: { en: 'Catalog for language models (RAG)' }, slug: 'rag' },
					],
				},
				{
					label: 'Grundschutz++',
					items: [
						{ label: 'Übersicht', translations: { en: 'Overview' }, slug: 'grundschutzpp' },
						{ label: 'Status & Zeitplan', translations: { en: 'Status & timeline' }, slug: 'grundschutzpp/zeitplan' },
						{ label: 'Änderungen am Katalog', translations: { en: 'Catalog changes' }, slug: 'aenderungen' },
						{ label: 'Methodik (BSI-Standard 300-1)', translations: { en: 'Methodology (BSI Standard 300-1)' }, slug: 'methodik' },
						{ label: 'Vergleich: Alt ↔ Neu', translations: { en: 'Comparison: old ↔ new' }, slug: 'vergleich' },
						{ label: 'Themen', translations: { en: 'Topics' }, slug: 'grundschutzpp/themen' },
						{ label: 'Zielobjekte', translations: { en: 'Target objects' }, slug: 'zielobjekte' },
						{ label: 'Dokumente', translations: { en: 'Documents' }, slug: 'dokumente' },
						{
							label: 'Managementsystem',
							translations: { en: 'Management system' },
							items: [
								{ label: 'GC Governance und Compliance', translations: { en: 'GC Governance and Compliance' }, slug: 'grundschutzpp/gc' },
								{ label: 'STM Strukturmodellierung', translations: { en: 'STM Structure modeling' }, slug: 'grundschutzpp/stm' },
								{ label: 'UMS Umsetzung', translations: { en: 'UMS Implementation' }, slug: 'grundschutzpp/ums' },
								{ label: 'VRB Verbesserung', translations: { en: 'VRB Improvement' }, slug: 'grundschutzpp/vrb' },
								{ label: 'PERF Monitoring-Evaluation', translations: { en: 'PERF Monitoring and evaluation' }, slug: 'grundschutzpp/perf' },
								{ label: 'RISK Risikomanagement', translations: { en: 'RISK Risk management' }, slug: 'grundschutzpp/risk' },
							],
						},
						{
							label: 'Themenfelder',
							translations: { en: 'Topic areas' },
							items: [
								{ label: 'ASST Informationen und Assets', translations: { en: 'ASST Information and assets' }, slug: 'grundschutzpp/asst' },
								{ label: 'PERS Personal', translations: { en: 'PERS Personnel' }, slug: 'grundschutzpp/pers' },
								{ label: 'BES Beschaffungsmanagement', translations: { en: 'BES Procurement management' }, slug: 'grundschutzpp/bes' },
								{ label: 'DLS Dienstleistersteuerung', translations: { en: 'DLS Service provider management' }, slug: 'grundschutzpp/dls' },
								{ label: 'TEST Änderungen und Tests', translations: { en: 'TEST Changes and tests' }, slug: 'grundschutzpp/test' },
								{ label: 'GEB Gebäudemanagement', translations: { en: 'GEB Facility management' }, slug: 'grundschutzpp/geb' },
								{ label: 'SENS Sensibilisierung', translations: { en: 'SENS Awareness' }, slug: 'grundschutzpp/sens' },
								{ label: 'ARCH Architektur', translations: { en: 'ARCH Architecture' }, slug: 'grundschutzpp/arch' },
								{ label: 'BER Berechtigung', translations: { en: 'BER Authorization' }, slug: 'grundschutzpp/ber' },
								{ label: 'NOT Notfallplanung', translations: { en: 'NOT Contingency planning' }, slug: 'grundschutzpp/not' },
								{ label: 'DET Detektion', translations: { en: 'DET Detection' }, slug: 'grundschutzpp/det' },
								{ label: 'REA Sicherheitsvorfallsbehandlung', translations: { en: 'REA Security incident handling' }, slug: 'grundschutzpp/rea' },
								{ label: 'KONF Konfiguration', translations: { en: 'KONF Configuration' }, slug: 'grundschutzpp/konf' },
								{ label: 'DEV Entwicklung', translations: { en: 'DEV Development' }, slug: 'grundschutzpp/dev' },
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
			// lastmod nur dort, wo das Datum aus den Daten der Seite selbst kommt: Google
			// wertet die Angabe nur, wenn sie verlässlich ist, und für die übrigen Seiten
			// gibt es kein zuverlässiges Datum (im Docker-Build fehlt .git). /export/ ändert
			// sich mit dem Katalogstand, /aenderungen/ mit dem neuesten Eintrag. Fehlt die
			// Datei (Fork), entfällt die Angabe.
			serialize(item) {
				const lastmod = LASTMOD[new URL(item.url).pathname];
				if (lastmod) item.lastmod = lastmod;
				return item;
			},
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
