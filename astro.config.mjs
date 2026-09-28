// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Klartext',
			description: 'Eigene lesbare Aufbereitung des BSI Grundschutz++ OSCAL-Katalogs',
			customCss: ['./src/styles/custom.css'],
				components: {
					ThemeSelect: './src/components/ThemeToggle.astro',
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
						{ label: 'GC Governance und Compliance', slug: 'grundschutzpp/gc' },
						{ label: 'STM Strukturmodellierung', slug: 'grundschutzpp/stm' },
						{ label: 'UMS Umsetzung', slug: 'grundschutzpp/ums' },
						{ label: 'VRB Verbesserung', slug: 'grundschutzpp/vrb' },
						{ label: 'PERF Monitoring-Evaluation', slug: 'grundschutzpp/perf' },
						{ label: 'RISK Risikomanagement', slug: 'grundschutzpp/risk' },
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
		}),
	],
});
