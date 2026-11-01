// Prüft die Regeln des ID-Checks (src/lib/id-check.ts): IDs finden, Daten lesen, je Zeile ab dem eigenen Datum prüfen.
// Aufruf: node --experimental-strip-types --test scripts/tests/id-check.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { parseIds, parseDatum, parseEingabe, pruefe, letzteAenderung, beschreibeEingabe } from '../../src/lib/id-check.ts';

const daten = {
	stand: { commit: 'x', veroeffentlicht: '2026-10-30T09:59:42Z' },
	beginn: '2026-07-27',
	ids: ['GC.1.1', 'BES.7.4.12', 'DLS.1.1.1'],
	aenderungen: {
		'BES.7.4.12': [
			{ datum: '2026-08-20', commit: 'aaaaaaa', titel: 'T', praktik: 'BES', felder: ['Titel'] },
			{ datum: '2026-10-30', commit: 'bbbbbbb', titel: 'T', praktik: 'BES', felder: ['Erläuterung'] },
		],
	},
	neu: {},
	entfernt: { 'OLD.1.1': [{ datum: '2026-09-03', commit: 'ccccccc' }] },
};

test('IDs werden im Text gefunden, ohne Doppelte, in Großschreibung', () => {
	assert.deepEqual(parseIds('bes.7.4.12, GC.1.1;\nBES.7.4.12 Text 1.2'), ['BES.7.4.12', 'GC.1.1']);
});

test('Datum: ISO und deutsch, ungültige Angaben werden abgelehnt', () => {
	assert.equal(parseDatum('2026-08-01'), '2026-08-01');
	assert.equal(parseDatum('01.08.2026'), '2026-08-01');
	assert.equal(parseDatum('1.8.26'), '2026-08-01');
	assert.equal(parseDatum('8/1/2026'), undefined);
	assert.equal(parseDatum('31.02.2026'), undefined);
	assert.equal(parseDatum(''), undefined);
});

test('Tabelle mit ID und "Bewertet am": Datum je Zeile, frühestes bei Duplikaten', () => {
	const csv = '﻿ID;Titel;Umsetzungsstatus;Bewertet am;Bemerkung\r\nBES.7.4.12;x;Erfüllt;01.09.2026;\r\nGC.1.1;y;;;\r\nBES.7.4.12;x;;15.08.2026;\r\nDLS.1.1.1;z;;kaputt;';
	const e = parseEingabe(csv);
	assert.equal(e.mitDatum, true);
	assert.equal(e.ungueltigeDaten, 1);
	assert.deepEqual(e.eintraege, [
		{ id: 'BES.7.4.12', seit: '2026-08-15' },
		{ id: 'GC.1.1', seit: undefined },
		{ id: 'DLS.1.1.1', seit: undefined },
	]);
});

test('Ohne Spalte "Bewertet am" werden die IDs gesucht und gemeinsam geprüft', () => {
	const e = parseEingabe('ID;Status\nGC.1.1;ok\nBES.7.4.12;offen');
	assert.equal(e.mitDatum, false);
	assert.deepEqual(e.eintraege.map((x) => x.id), ['GC.1.1', 'BES.7.4.12']);
});

test('Prüfung: eigenes Datum je Zeile, sonst das allgemeine; Datum zählt einschließlich', () => {
	const r = pruefe(daten, [{ id: 'BES.7.4.12', seit: '2026-09-01' }, { id: 'BES.7.4.12', seit: '2026-10-30' }, { id: 'BES.7.4.12', seit: '2026-10-31' }, 'GC.1.1', 'NOPE.1.1', 'OLD.1.1'], '2026-07-27');
	assert.deepEqual(r.map((x) => x.art), ['geaendert', 'geaendert', 'unveraendert', 'unveraendert', 'unbekannt', 'entfernt']);
	assert.equal(r[0].aenderungen.length, 1);
	assert.equal(r[0].eigenesDatum, true);
	assert.equal(r[3].eigenesDatum, false);
});

test('Jüngste Änderung einer Anforderung', () => {
	assert.equal(letzteAenderung(daten, 'BES.7.4.12').datum, '2026-10-30');
	assert.equal(letzteAenderung(daten, 'GC.1.1'), undefined);
});

test('Beschreibung der erkannten Eingabe', () => {
	assert.equal(beschreibeEingabe(parseEingabe('')), 'Noch keine Anforderungs-IDs erkannt.');
	assert.equal(beschreibeEingabe(parseEingabe('GC.1.1')), '1 ID erkannt, alle werden ab dem Datum oben geprüft.');
	const csv = 'ID;Bewertet am\nGC.1.1;01.08.2026\nBES.7.4.12;\nDLS.1.1.1;kaputt';
	assert.equal(
		beschreibeEingabe(parseEingabe(csv)),
		'3 IDs erkannt, 1 mit eigenem Datum aus „Bewertet am“, 2 ohne (sie werden ab dem Datum oben geprüft). 1 Datum ist nicht lesbar.',
	);
});

test('CSV wie Excel sie schreibt: Felder mit Trennzeichen in Anführungszeichen verschieben keine Spalten', () => {
	const csv = '\uFEFFID;Titel;Zielobjekte;Bewertet am;Bemerkung\r\n' +
		'GC.1.1;"Ein Titel; mit Semikolon";"A; B; C";01.08.2026;ok\r\n' +
		'BES.7.4.12;"Mit ""Anführungszeichen"" und\nZeilenumbruch";"X; Y";2026-09-15;\r\n';
	const e = parseEingabe(csv);
	assert.deepEqual(e.eintraege, [{ id: 'GC.1.1', seit: '2026-08-01' }, { id: 'BES.7.4.12', seit: '2026-09-15' }]);
	assert.equal(e.ungueltigeDaten, 0);
});

test('Trennzeichen Komma und Tabulator werden aus der Kopfzeile erkannt', () => {
	assert.deepEqual(parseEingabe('ID,Bewertet am,Notiz\nGC.1.1,01.08.2026,"a, b"').eintraege, [{ id: 'GC.1.1', seit: '2026-08-01' }]);
	assert.deepEqual(parseEingabe('ID\tBewertet am\nGC.1.1\t01.08.2026').eintraege, [{ id: 'GC.1.1', seit: '2026-08-01' }]);
});

test('Der echte Export dieser Seite wird Zeile für Zeile richtig gelesen', async () => {
	const { readFileSync } = await import('node:fs');
	const csv = readFileSync(new URL('../../public/downloads/grundschutzpp-anforderungen-bes.csv', import.meta.url), 'utf8');
	const e = parseEingabe(csv);
	assert.equal(e.eintraege.length, csv.split('\r\n').filter(Boolean).length - 1);
	assert.equal(e.ungueltigeDaten, 0);
	assert.equal(e.mitDatum, false); // die Spalte "Bewertet am" ist im Export leer
});
