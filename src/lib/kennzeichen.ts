// Erklaerungen zu Pflichtgrad, Sicherheitsstufe und Aufwand. Eine Quelle fuer die Pillen
// (ControlMeta.astro) und die Legende auf den Praktik-Seiten (KennzeichenLegende.astro).

// Quelle: Grundschutz-PlusPlus/documentation/namespaces/modal_verbs.csv
export const MODAL_VERBS: Record<string, { hint: string; family: string }> = {
	MUSS: {
		hint: 'Uneingeschränkte Anforderung – muss unbedingt erfüllt werden (nach RFC2119 / DIN 820-2:2022, Anhang H).',
		family: 'danger',
	},
	SOLLTE: {
		hint: 'Normalerweise zu erfüllen, Abweichung nur mit sorgfältig abgewogener, stichhaltiger Begründung (nach RFC2119 / DIN 820-2:2022, Anhang H).',
		family: 'warn',
	},
	KANN: {
		hint: 'Keine generelle Verpflichtung – je nach Situation (Risikoanalyse) sinnvoll (vgl. DIN 820-2:2022-12).',
		family: 'calm',
	},
};

// Quelle: Grundschutz-PlusPlus/documentation/namespaces/security_level.csv
export const SEC_LEVELS: Record<string, { label: string; hint: string; family: string }> = {
	'normal-SdT': { label: 'Standard-Sicherheitsstufe', hint: 'Standard-Sicherheitsstufe (Stand der Technik).', family: 'info' },
	erhöht: { label: 'Erhöhte Sicherheitsstufe', hint: 'Erhöhte Sicherheitsstufe – höherer Schutzbedarf.', family: 'info-strong' },
};

// Quelle: Grundschutz-PlusPlus/documentation/namespaces/effort_level.csv
export const EFFORT: Record<string, { hint: string; family: string }> = {
	// Steht neben der 1-5-Skala, nicht darüber. Früher als volle schwarze
	// Fläche gesetzt -- das machte die unwichtigste Angabe der Zeile zur
	// auffälligsten, direkt neben einem blass getönten MUSS. Dass die
	// Umsetzung zwingend ist, sagt ohnehin der Pflichtgrad; hier bleibt nur
	// "nicht bewertet" übrig, und das ist eine leise Angabe.
	'0': {
		hint: 'Wird nicht bewertet – die Umsetzung ist in jedem Fall zwingend erforderlich.',
		family: 'neutral',
	},
	'1': {
		hint: 'Quick Win: meist noch am selben Tag umsetzbar, kein laufender Pflegeaufwand.',
		family: 'calm',
	},
	'2': {
		hint: 'Meist innerhalb einer Woche mit eigenen Mitteln umsetzbar, nur geringer laufender Aufwand.',
		family: 'calm',
	},
	'3': {
		hint: 'Wochen bis Monate, ggf. externe Dienstleister nötig; laufender Betrieb durch kleines Team möglich.',
		family: 'accent',
	},
	'4': {
		hint: 'Langfristige Umsetzung/Beibehaltung; Expertenwissen und oft Drittunterstützung nötig.',
		family: 'warn',
	},
	'5': {
		hint: 'Aufwändige, komplexe Maßnahmen; tiefes Expertenwissen und sorgfältige Planung nötig.',
		family: 'danger',
	},
};
