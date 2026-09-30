---
title: Über diese Seite
description: Was diese Aufbereitung des Grundschutz++-Katalogs ist, wie sie aktuell bleibt, und unter welchen Lizenzen Inhalt und Code stehen.
---

Eine eigene, lesbare Aufbereitung des BSI-OSCAL-Katalogs
(`Grundschutz++-resolved_catalog.json`) — **kein offizielles BSI-Angebot**
und in keiner Weise mit dem Bundesamt für Sicherheit in der
Informationstechnik verbunden. Maßgeblich ist immer das offizielle Original.

Der Katalog befindet sich aktuell in der **Pilotphase**, siehe
[Status & Zeitplan](/grundschutzpp/zeitplan/).

## Warum es diese Seite gibt

Das BSI liefert Grundschutz++ als OSCAL-JSON aus — ein Format, das für
Werkzeuge und die Erzeugung von Sicherheitskonzepten gebaut ist, nicht zum
Lesen. Wer nur wissen will, was eine Anforderung verlangt, findet sich in
einer mehrere zehntausend Zeilen langen JSON-Datei wieder.

Diese Seite rendert denselben Katalog als Text, den man tatsächlich lesen
kann: mit Volltextsuche, einem Sprungziel je Anforderung, Pflichtgrad,
Stufe, Aufwand und Gefährdungen direkt am Text, und dem Mapping zurück auf
das alte IT-Grundschutz-Kompendium.

## Wie die Seite aktuell bleibt

Die Katalogseiten sind **generiert, nicht abgeschrieben**. Nach einer
Änderung am BSI-Katalog erzeugt ein Skript sie neu; ein täglicher
CI-Durchlauf prüft die Quelle und öffnet bei Abweichungen einen Pull
Request. Es gibt also keinen einmalig übertragenen Stand, der langsam
veraltet.

## Andere Aufbereitungen

Es gibt bereits ein Werkzeug, das den OSCAL-Katalog visuell aufbereitet —
mit mehr Darstellungsmöglichkeiten (Graphen, Diagramme) als diese Seite
anstrebt. Diese Seite verfolgt ein anderes Ziel: ruhiges, durchsuchbares
Lesen mit dauerhaften Links.

Ein Unterschied betrifft die Lizenzierung. Jenes Werkzeug steht unter einer
Inhalts-Lizenz (CC BY-SA) statt unter einer Software-Lizenz — wovon
Creative Commons für Quellcode ausdrücklich abrät (kein Patentschutz, nie
von der OSI als Open-Source-Lizenz anerkannt).

## Lizenzen

Diese Seite trennt beides bewusst:

- **Katalog-Inhalt** (alles unter `/grundschutzpp/`): CC BY-SA 4.0,
  © BSI-Bund — so, wie das BSI ihn selbst lizenziert hat.
- **Code** dieser Website: MIT.

Das alte IT-Grundschutz-Kompendium wird hier bewusst **nicht** im Volltext
wiedergegeben. Die Vergleichsseiten zeigen nur Struktur — alte
Anforderungs-ID, Beziehungstyp, neue Anforderung — und verlinken für den
Originaltext auf die PDFs des BSI.

## Druck und Export

Jede Gruppenseite lässt sich über die Druckfunktion des Browsers als PDF
exportieren; das Layout ist dafür eingerichtet.
