// Reine Funktionen für den ID-Check (/id-check/). Kein DOM, damit sie sich einzeln prüfen lassen.
// Der Check zeigt nur, was im Änderungsprotokoll steht: welche der eingegebenen Anforderungen das BSI
// seit einem Datum geändert hat. Er bewertet nicht, ob eine Änderung für jemanden wichtig ist.

export type Aenderung = { datum: string; commit: string; titel: string; praktik: string; felder: string[] };
export type Markierung = { datum: string; commit: string };
export type IdDaten = {
	stand: { commit: string; veroeffentlicht: string };
	beginn: string;
	ids: string[];
	aenderungen: Record<string, Aenderung[]>;
	neu: Record<string, Markierung[]>;
	entfernt: Record<string, Markierung[]>;
};

// Anforderungs-IDs sehen aus wie GC.5.1.1 oder BES.7.4.12: 2 bis 6 Buchstaben, dann Punkt und Zahl, mehrfach.
// Gefunden werden sie überall im Text, egal ob getrennt durch Zeilen, Kommas, Semikolons oder Tabulatoren
// (ein eingefügtes Excel-Blatt oder eine CSV-Datei funktioniert damit ohne weiteres).
const ID = /\b([A-Za-z]{2,6}(?:\.\d+){2,})\b/g;

export function parseIds(text: string): string[] {
	const gesehen = new Set<string>();
	for (const m of text.matchAll(ID)) gesehen.add(m[1].toUpperCase());
	return [...gesehen];
}

export type Ergebnis =
	| { id: string; art: 'geaendert'; aenderungen: Aenderung[] }
	| { id: string; art: 'unveraendert' }
	| { id: string; art: 'neu'; seit: Markierung }
	| { id: string; art: 'entfernt'; seit: Markierung }
	| { id: string; art: 'unbekannt' };

// "Seit" heißt: ab diesem Tag einschließlich. Der Stand eines Tages kann vor oder nach der eigenen
// Bewertung am selben Tag veröffentlicht worden sein; im Zweifel zeigen wir lieber eine Änderung zu viel.
export function pruefe(daten: IdDaten, eingegeben: string[], seit: string): Ergebnis[] {
	const bekannt = new Set(daten.ids);
	const ab = <T extends { datum: string }>(liste: T[] | undefined) => (liste ?? []).filter((x) => x.datum >= seit);
	return eingegeben.map((id): Ergebnis => {
		const entfernt = ab(daten.entfernt[id]);
		if (entfernt.length) return { id, art: 'entfernt', seit: entfernt[0] };
		if (!bekannt.has(id) && !(daten.entfernt[id] ?? []).length) return { id, art: 'unbekannt' };
		const neu = ab(daten.neu[id]);
		if (neu.length) return { id, art: 'neu', seit: neu[0] };
		const aenderungen = ab(daten.aenderungen[id]);
		return aenderungen.length ? { id, art: 'geaendert', aenderungen } : { id, art: 'unveraendert' };
	});
}
