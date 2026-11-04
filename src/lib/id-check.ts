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

// Eine Eingabezeile: die ID und, wenn die Tabelle eine Spalte "Bewertet am" hat, das Datum der eigenen Bewertung.
export type Eingabe = { id: string; seit?: string };

export type Ergebnis = { id: string; ab: string; eigenesDatum: boolean } & (
	| { art: 'geaendert'; aenderungen: Aenderung[] }
	| { art: 'unveraendert' }
	| { art: 'neu'; seit: Markierung }
	| { art: 'entfernt'; seit: Markierung }
	| { art: 'unbekannt' }
);

// Datum aus einer Zelle: JJJJ-MM-TT oder TT.MM.JJJJ (auch TT.MM.JJ), so schreibt es deutsches Excel in eine CSV-Datei.
// Alles andere (zum Beispiel 8/1/2026, bei dem Tag und Monat nicht eindeutig sind) gilt als ungültig.
export function parseDatum(zelle: string): string | undefined {
	const t = zelle.trim();
	let j: number, m: number, d: number;
	let treffer = t.match(/^(\d{4})-(\d{2})-(\d{2})(?:[T ].*)?$/);
	if (treffer) [j, m, d] = [Number(treffer[1]), Number(treffer[2]), Number(treffer[3])];
	else if ((treffer = t.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4}|\d{2})$/))) {
		[d, m, j] = [Number(treffer[1]), Number(treffer[2]), Number(treffer[3])];
		if (treffer[3].length === 2) j += 2000;
	} else return undefined;
	const echt = new Date(Date.UTC(j, m - 1, d));
	if (echt.getUTCFullYear() !== j || echt.getUTCMonth() !== m - 1 || echt.getUTCDate() !== d) return undefined;
	return `${String(j).padStart(4, '0')}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
}

const ZELLE_ID = /^[A-Za-z]{2,6}(?:\.\d+){2,}$/;

// CSV lesen wie Excel sie schreibt: Trennzeichen aus der Kopfzeile, Felder in Anführungszeichen dürfen das Trennzeichen,
// Zeilenumbrüche und doppelte Anführungszeichen ("") enthalten. Ohne das verschöben Felder wie "A; B" (Zielobjekte,
// Gefährdungen im Export dieser Seite) alle folgenden Spalten.
function trennzeichen(text: string): string {
	const kopf = text.split(/\r?\n/).find((z) => /(^|[;\t,"])\s*"?(anforderungs-)?id"?\s*($|[;\t,])/i.test(z)) ?? '';
	let innen = false;
	const zahl: Record<string, number> = { ';': 0, '\t': 0, ',': 0 };
	for (const c of kopf) {
		if (c === '"') innen = !innen;
		else if (!innen && c in zahl) zahl[c] += 1;
	}
	return Object.entries(zahl).sort((x, y) => y[1] - x[1])[0][1] > 0 ? Object.entries(zahl).sort((x, y) => y[1] - x[1])[0][0] : ';';
}

function lieseCsv(text: string, sep: string): string[][] {
	const zeilen: string[][] = [];
	let zeile: string[] = [];
	let feld = '';
	let innen = false;
	for (let i = 0; i < text.length; i++) {
		const c = text[i];
		if (innen) {
			if (c === '"' && text[i + 1] === '"') {
				feld += '"';
				i += 1;
			} else if (c === '"') innen = false;
			else feld += c;
		} else if (c === '"') innen = true;
		else if (c === sep) {
			zeile.push(feld.trim());
			feld = '';
		} else if (c === '\n' || c === '\r') {
			if (c === '\r' && text[i + 1] === '\n') i += 1;
			zeile.push(feld.trim());
			zeilen.push(zeile);
			zeile = [];
			feld = '';
		} else feld += c;
	}
	if (feld !== '' || zeile.length) {
		zeile.push(feld.trim());
		zeilen.push(zeile);
	}
	return zeilen;
}

export type Eingaben = { eintraege: Eingabe[]; mitDatum: boolean; ungueltigeDaten: number };

// Liest die Eingabe. Hat sie eine Kopfzeile mit den Spalten "ID" und "Bewertet am" (so heißen sie im Excel-Export dieser
// Seite), gilt je Zeile das eigene Datum; sonst werden die IDs im Text gesucht und alle mit demselben Datum geprüft.
// Kommt eine ID mehrfach vor, zählt das früheste Datum: lieber eine Änderung zu viel anzeigen als eine zu wenig.
export function parseEingabe(text: string): Eingaben {
	const sauber = text.replace(/^\uFEFF/, '');
	const tabelle = lieseCsv(sauber, trennzeichen(sauber));
	const kopf = tabelle.findIndex((z) => z.some((c) => /^(anforderungs-)?id$/i.test(c)));
	if (kopf >= 0) {
		const spalten = tabelle[kopf];
		const idSpalte = spalten.findIndex((c) => /^(anforderungs-)?id$/i.test(c));
		const datumSpalte = spalten.findIndex((c) => /^bewertet am$/i.test(c));
		if (datumSpalte >= 0) {
			const nachId = new Map<string, Eingabe>();
			let ungueltig = 0;
			for (const c of tabelle.slice(kopf + 1)) {
				if (!ZELLE_ID.test(c[idSpalte] ?? '')) continue;
				const id = c[idSpalte].toUpperCase();
				const roh = c[datumSpalte] ?? '';
				const datum = roh ? parseDatum(roh) : undefined;
				if (roh && !datum) ungueltig += 1;
				const vorher = nachId.get(id);
				if (!vorher) nachId.set(id, { id, seit: datum });
				else if (!datum || (vorher.seit && datum < vorher.seit) || !vorher.seit) vorher.seit = datum ?? vorher.seit;
			}
			return { eintraege: [...nachId.values()], mitDatum: [...nachId.values()].some((e) => e.seit), ungueltigeDaten: ungueltig };
		}
	}
	return { eintraege: parseIds(text).map((id) => ({ id })), mitDatum: false, ungueltigeDaten: 0 };
}

// "Seit" heißt: ab diesem Tag einschließlich. Der Stand eines Tages kann vor oder nach der eigenen
// Bewertung am selben Tag veröffentlicht worden sein; im Zweifel zeigen wir lieber eine Änderung zu viel.
// Hat eine Zeile ein eigenes Datum, gilt dieses, sonst das allgemeine.
export function pruefe(daten: IdDaten, eingaben: (string | Eingabe)[], seit: string): Ergebnis[] {
	const bekannt = new Set(daten.ids);
	return eingaben.map((eingabe): Ergebnis => {
		const { id, seit: eigenes } = typeof eingabe === 'string' ? { id: eingabe, seit: undefined } : eingabe;
		const ab = eigenes ?? seit;
		const basis = { id, ab, eigenesDatum: Boolean(eigenes) };
		const nach = <T extends { datum: string }>(liste: T[] | undefined) => (liste ?? []).filter((x) => x.datum >= ab);
		const entfernt = nach(daten.entfernt[id]);
		if (entfernt.length) return { ...basis, art: 'entfernt', seit: entfernt[0] };
		if (!bekannt.has(id) && !(daten.entfernt[id] ?? []).length) return { ...basis, art: 'unbekannt' };
		const neu = nach(daten.neu[id]);
		if (neu.length) return { ...basis, art: 'neu', seit: neu[0] };
		const aenderungen = nach(daten.aenderungen[id]);
		return aenderungen.length ? { ...basis, art: 'geaendert', aenderungen } : { ...basis, art: 'unveraendert' };
	});
}

// Wie sie angezeigt werden, steht in datum.ts; hier bleibt der Name für die Aufrufer (Seite und Test).
export { datumDe } from './datum.ts';

// Die jüngste Änderung einer Anforderung laut Änderungsprotokoll, oder undefined, wenn dort keine steht.
export function letzteAenderung(daten: IdDaten, id: string): Aenderung | undefined {
	const liste = daten.aenderungen[id];
	return liste?.reduce((a, b) => (b.datum >= a.datum ? b : a));
}

// Ein Satz dazu, was aus der Eingabe erkannt wurde, damit man vor dem Prüfen sieht, ob sie richtig gelesen wird.
export function beschreibeEingabe(e: Eingaben): string {
	const n = e.eintraege.length;
	if (n === 0) return 'Noch keine Anforderungs-IDs erkannt.';
	const ids = `${n} ${n === 1 ? 'ID' : 'IDs'} erkannt`;
	if (!e.mitDatum) return `${ids}, alle werden ab dem Datum oben geprüft.`;
	const eigene = e.eintraege.filter((x) => x.seit).length;
	const rest = n - eigene;
	return (
		`${ids}, ${eigene} mit eigenem Datum aus „Bewertet am“` +
		(rest ? `, ${rest} ohne (sie werden ab dem Datum oben geprüft)` : '') +
		(e.ungueltigeDaten ? `. ${e.ungueltigeDaten} ${e.ungueltigeDaten === 1 ? 'Datum ist' : 'Daten sind'} nicht lesbar` : '') +
		'.'
	);
}
