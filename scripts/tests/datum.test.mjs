// Datumsdarstellung (src/lib/datum.ts): nur der Datumsteil zählt, keine Zeitzonenumrechnung.
// Aufruf: node --experimental-strip-types --test scripts/tests/datum.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { tag, datumDe } from '../../src/lib/datum.ts';
import { datumDe as ausIdCheck } from '../../src/lib/id-check.ts';

test('tag schneidet den Datumsteil ab', () => {
	assert.equal(tag('2026-10-30T09:59:42Z'), '2026-10-30');
	assert.equal(tag('2026-10-30'), '2026-10-30');
});

test('datumDe: Monatsname, kein führende Null, Tag bleibt der Tag', () => {
	assert.equal(datumDe('2026-03-05T23:59:59Z'), '5. März 2026');
	assert.equal(datumDe('2026-12-31T23:59:59-11:00'), '31. Dezember 2026');
	assert.equal(datumDe('2026-01-01'), '1. Januar 2026');
});

test('id-check.ts gibt dieselbe Funktion weiter', () => {
	assert.equal(ausIdCheck, datumDe);
});
