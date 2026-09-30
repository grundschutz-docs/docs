// @ts-check
import { readFileSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import mdx from '@astrojs/mdx';

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
export default defineConfig({
	integrations: [
		starlight({
			title: SITE_NAME || 'Grundschutz++ Docs',
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
