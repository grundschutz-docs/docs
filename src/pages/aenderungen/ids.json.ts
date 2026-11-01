import type { APIRoute } from 'astro';
import changelog from '../../data/changelog.json';
import katalog from '../../../public/downloads/grundschutzpp-anforderungen.json';
import type { Aenderung, IdDaten, Markierung } from '../../lib/id-check';

// Die Daten für den ID-Check (/id-check/): je Anforderung, was das BSI wann geändert hat. Alles stammt aus
// src/data/changelog.json und dem Katalog-Export, nichts wird gerechnet oder bewertet. Der Check selbst
// läuft im Browser; diese Datei ist der einzige Abruf, und sie enthält keine Angaben der Nutzenden.
type Eintrag = {
	commit: string;
	veroeffentlicht: string;
	aenderungen: { id: string; titel: string; praktik: string; felder: { name: string }[] }[];
	neu: (string | { id: string })[];
	entfernt: (string | { id: string })[];
};

const idVon = (x: string | { id: string }) => (typeof x === 'string' ? x : x.id);

export const GET: APIRoute = () => {
	const daten: IdDaten = {
		stand: changelog.stand,
		beginn: changelog.basis.veroeffentlicht.slice(0, 10),
		ids: (katalog.anforderungen as { id: string }[]).map((a) => a.id),
		aenderungen: {},
		neu: {},
		entfernt: {},
	};
	const merke = (ziel: Record<string, Markierung[]>, id: string, e: Eintrag) =>
		(ziel[id] ??= []).push({ datum: e.veroeffentlicht.slice(0, 10), commit: e.commit.slice(0, 7) });

	for (const e of changelog.eintraege as unknown as Eintrag[]) {
		for (const a of e.aenderungen) {
			const eintrag: Aenderung = {
				datum: e.veroeffentlicht.slice(0, 10),
				commit: e.commit.slice(0, 7),
				titel: a.titel,
				praktik: a.praktik,
				felder: a.felder.map((f) => f.name),
			};
			(daten.aenderungen[a.id] ??= []).push(eintrag);
		}
		e.neu.forEach((x) => merke(daten.neu, idVon(x), e));
		e.entfernt.forEach((x) => merke(daten.entfernt, idVon(x), e));
	}
	return new Response(JSON.stringify(daten), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};
