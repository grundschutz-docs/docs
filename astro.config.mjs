// @ts-check
import { readFileSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';

// Name an einer Stelle definiert (.env, siehe .env.example) statt über
// mehrere Dateien verstreut — solange der endgültige Name noch nicht feststeht.
// Kein vite-Import hier: pnpms strenges node_modules verbietet den Zugriff auf
// nicht direkt deklarierte Abhängigkeiten, deshalb ein minimaler eigener Parser.
function readSiteName() {
	if (process.env.SITE_NAME) return process.env.SITE_NAME;
	try {
		const line = readFileSync(new URL('./.env', import.meta.url), 'utf-8')
			.split('\n')
			.find((l) => l.startsWith('SITE_NAME='));
		return line?.slice('SITE_NAME='.length).trim();
	} catch {
		return undefined;
	}
}

const SITE_NAME = readSiteName();

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
	],
});
