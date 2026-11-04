// Regeln der Export-Bibliotheken (src/lib/export-query.ts und export-checkliste.ts): die Auswahl als Adresse
// lesen und schreiben, unbekannte Werte erkennen, Checkliste als Markdown und HTML.
// Aufruf: node --experimental-strip-types --test scripts/tests/export-libs.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { parseQuery, buildQuery, unknownMessage, GROUPS } from '../../src/lib/export-query.ts';
import { dokumentSlug, dokumenteDerAuswahl, toMarkdown, toHtml } from '../../src/lib/export-checkliste.ts';

const valid = {
	praktik: new Set(['GC', 'STM', 'KONF']),
	pflicht: new Set(['MUSS', 'SOLLTE', 'KANN']),
	stufe: new Set(['Standard-Sicherheitsstufe', 'Erhöhte Sicherheitsstufe']),
	aufwand: new Set(['0', '1', '2']),
	ziel: new Set(['Webserver', 'Interpersonelle Kommunikation']),
};

test('leere Adresse: nichts ausgewählt, Anforderungen ohne Kategorie bleiben an', () => {
	for (const s of ['', '?']) {
		const { state, unknown } = parseQuery(s, valid);
		assert.deepEqual(state.selected, { praktik: [], pflicht: [], stufe: [], aufwand: [], ziel: [] });
		assert.equal(state.ohne, true);
		assert.deepEqual(unknown, {});
	}
});

test('Adresse lesen: mit und ohne Fragezeichen, Leerzeichen, doppelte Werte', () => {
	const a = parseQuery('?praktik=GC,STM&pflicht=MUSS', valid).state.selected;
	const b = parseQuery('praktik= GC , STM ,GC&pflicht=MUSS', valid).state.selected;
	assert.deepEqual(a.praktik, ['GC', 'STM']);
	assert.deepEqual(b, a);
});

test('unbekannte Werte landen in unknown und nicht in der Auswahl', () => {
	const { state, unknown } = parseQuery('?praktik=GC,XYZ&ziel=Webserverr', valid);
	assert.deepEqual(state.selected.praktik, ['GC']);
	assert.deepEqual(unknown, { praktik: ['XYZ'], ziel: ['Webserverr'] });
});

test('ohne=nein schaltet nur genau diesen Wert ab', () => {
	assert.equal(parseQuery('?ohne=nein', valid).state.ohne, false);
	assert.equal(parseQuery('?ohne=ja', valid).state.ohne, true);
	assert.equal(parseQuery('?ohne=', valid).state.ohne, true);
});

test('schreiben und wieder lesen ergibt dieselbe Auswahl (auch mit Umlauten und Leerzeichen)', () => {
	const state = {
		selected: {
			praktik: ['GC', 'KONF'],
			pflicht: ['MUSS'],
			stufe: ['Erhöhte Sicherheitsstufe'],
			aufwand: ['0', '2'],
			ziel: ['Interpersonelle Kommunikation', 'Webserver'],
		},
		ohne: false,
	};
	const query = buildQuery(state);
	assert.match(query, /^\?/);
	assert.deepEqual(parseQuery(query, valid).state, state);
});

test('ohne=nein wird nur geschrieben, wenn eine Zielobjektkategorie gewählt ist', () => {
	const leer = { praktik: [], pflicht: [], stufe: [], aufwand: [], ziel: [] };
	assert.equal(buildQuery({ selected: leer, ohne: false }), '');
	assert.equal(buildQuery({ selected: { ...leer, ziel: ['Webserver'] }, ohne: false }), '?ziel=Webserver&ohne=nein');
	assert.equal(buildQuery({ selected: { ...leer, ziel: ['Webserver'] }, ohne: true }), '?ziel=Webserver');
});

test('GROUPS ist die Reihenfolge der Adresse', () => {
	assert.deepEqual([...GROUPS], ['praktik', 'pflicht', 'stufe', 'aufwand', 'ziel']);
});

test('unbekannter Wert ohne weitere Auswahl: der Link liefert still alles, die Meldung sagt es', () => {
	// Der Fall, für den die Funktion da ist: eine Kategorie wurde beim BSI umbenannt.
	const { state, unknown } = parseQuery('?ziel=Webserverr', valid);
	const text = unknownMessage(unknown, state);
	assert.match(text, /„Webserverr“/);
	assert.match(text, /alle Anforderungen/);
	assert.match(text, /Ohne gültige Zielobjektkategorie/);
});

test('unbekannter Wert neben einer gültigen Auswahl: kein "alle Anforderungen"', () => {
	const { state, unknown } = parseQuery('?praktik=GC&pflicht=NIE', valid);
	const text = unknownMessage(unknown, state);
	assert.match(text, /Pflichtgrad „NIE“/);
	assert.doesNotMatch(text, /alle Anforderungen/);
});

test('alles bekannt: keine Meldung', () => {
	const { state, unknown } = parseQuery('?praktik=GC', valid);
	assert.equal(unknownMessage(unknown, state), '');
});

test('dokumentSlug schreibt Umlaute aus wie der Generator', () => {
	assert.equal(dokumentSlug('Detektions-Konzept'), 'detektions-konzept');
	assert.equal(dokumentSlug('Übergabe für Größe'), 'uebergabe-fuer-groesse');
	assert.equal(dokumentSlug('  Sonder  Zeichen! '), 'sonder-zeichen');
});

const rows = [
	{ id: 'GC.1.1', titel: 'ISMS *errichten*', praktik_id: 'GC', pflichtgrad: 'MUSS', seite: 'https://x.test/grundschutzpp/gc/#GC.1.1', dokument: 'ISMS-Regelwerk' },
	{ id: 'GC.1.2', titel: 'Freigabe <b>', praktik_id: 'GC', pflichtgrad: 'SOLLTE', seite: 'https://x.test/grundschutzpp/gc/#GC.1.2', dokument: 'ISMS-Regelwerk' },
	{ id: 'ZZZ.1.1', titel: 'Unbekannte Praktik', praktik_id: 'ZZZ', pflichtgrad: 'KANN', seite: 'https://x.test/grundschutzpp/zzz/#ZZZ.1.1', dokument: '' },
];
const ctx = {
	auswahl: 'Praktik GC',
	link: 'https://x.test/export/?praktik=GC',
	stand: '29.10.2026',
	quelle: 'BSI, CC BY-SA 4.0',
	praktiken: [{ id: 'GC', titel: 'Governance und Compliance' }],
	siteUrl: 'https://x.test',
};

test('Dokumente der Auswahl: gezählt, häufigste zuerst, leere Namen ausgelassen', () => {
	assert.deepEqual(dokumenteDerAuswahl(rows), [{ name: 'ISMS-Regelwerk', slug: 'isms-regelwerk', anzahl: 2 }]);
});

test('Markdown: Links, Pflichtgrad, Maskierung, Quelle; unbekannte Praktik geht nicht verloren', () => {
	const text = toMarkdown(rows, ctx);
	assert.match(text, /3 Anforderungen · Stand 29\.10\.2026/);
	assert.match(text, /\[Diese Auswahl öffnen\]\(https:\/\/x\.test\/export\/\?praktik=GC\)/);
	assert.match(text, /- \[ \] \[GC\.1\.1\]\(https:\/\/x\.test\/grundschutzpp\/gc\/#GC\.1\.1\) · ISMS \\\*errichten\\\* · \*\*MUSS\*\*/);
	assert.match(text, /Freigabe \\<b\\>/);
	assert.match(text, /### ZZZ \(1\)/);
	assert.match(text, /\(https:\/\/x\.test\/dokumente\/isms-regelwerk\/\) \(2\)/);
	assert.match(text, /Quelle: BSI, CC BY-SA 4\.0/);
});

test('HTML: Sonderzeichen sind maskiert, nichts aus den Daten wird zu Markup', () => {
	const text = toHtml(rows, ctx);
	assert.match(text, /Freigabe &lt;b&gt;/);
	assert.doesNotMatch(text, /<b>/);
	assert.match(text, /<strong>MUSS<\/strong>/);
	assert.match(text, /<a href="https:\/\/x\.test\/export\/\?praktik=GC">/);
});

test('eine Anforderung heißt "1 Anforderung"', () => {
	assert.match(toMarkdown(rows.slice(0, 1), ctx), /^1 Anforderung · Stand/m);
});
