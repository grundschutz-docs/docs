# 0007. Rollenbasierte Einstiegsseiten (Geschäftsführung/ISB/Devs) statt einheitlicher Startseite

## Status

Angenommen

## Datum

2026-09-29

## Kontext

Die bisherige Startseite (`src/content/docs/index.mdx`) erklärt, was OSCAL
ist, warum es für Maschinen statt Menschen geschrieben ist, und wie der
Katalog strukturiert ist — im Kern eine Projekt-Vorstellung, wie man sie von
einem OSS-README erwartet. Drei tatsächliche Zielgruppen lesen diese Seite
aber mit völlig unterschiedlichen Fragen: Geschäftsführung will wissen, wo
Pflicht und persönliches Haftungsrisiko liegen; ISBs betreiben den
PDCA-Zyklus als Tagesgeschäft; Devs wollen direkt zur technischen Umsetzung.
Eine einzige Seite für alle drei bedient keine davon gut.

Eine Recherche zur Positionierung (2026-09-29, siehe Projekt-Memory) ergab:
mindestens drei echte Wettbewerber existieren bereits (ISW Grundschutz++
Cockpit, grc-tools.de, johanneskresse.com/bsi-mapping), aber **keiner** von
ihnen bietet einen nach Zielgruppe sortierten Einstieg — das ist eine echte
Lücke, kein Nice-to-have.

Der Katalog selbst liefert dafür bereits eine passende Struktur, ohne dass
etwas Neues erfunden werden muss: sechs PDCA-Management-Praktiken
(GC/STM/UMS/PERF/VRB/RISK, `MANAGEMENT_CYCLE_IDS` in
`scripts/generate_docs.py`) und vierzehn operative Themenfelder, dazu
Pflicht (`modal_verb`) und Sicherheitsstufe (`sec_level`) pro Anforderung.

Für die Geschäftsführungs-Perspektive wurde zusätzlich am 2026-09-29 direkt
per `curl` aus den Primärquellen recherchiert (nicht aus einer
Zusammenfassung übernommen):

- **§ 28 BSIG** (Fassung seit 2.12.2025,
  https://www.gesetze-im-internet.de/bsig_2025/BJNR12D0B0025.html): exakte
  Schwellenwerte für "besonders wichtige Einrichtung" / "wichtige
  Einrichtung" (Mitarbeiterzahl, Jahresumsatz, Jahresbilanzsumme, Sektor
  nach Anlage 1/2).
- **§ 38 BSIG**: Umsetzungs-, Überwachungs- und Schulungspflicht der
  Geschäftsleitung; Haftung bei Pflichtverletzung ist primär Innenhaftung
  gegenüber der eigenen Einrichtung, nach dem jeweils anwendbaren
  Gesellschaftsrecht.
- **§ 43 GmbHG** (https://www.gesetze-im-internet.de/gmbhg/__43.html) und
  **§ 93 AktG** (https://www.gesetze-im-internet.de/aktg/__93.html): die
  gesellschaftsrechtlichen Haftungsnormen, auf die § 38 BSIG verweist,
  inklusive der Business-Judgment-Rule in § 93 Abs. 1 Satz 2 AktG.

Diese Quellen sind Gesetzestext, keine Rechtsberatung — die Seite muss das
auch so behandeln (siehe Entscheidung unten), sonst entsteht ein echtes
Haftungsrisiko für den Betreiber dieser Seite selbst, nicht nur ein
Positionierungsproblem.

## Entscheidung

Wir bauen drei rollenbasierte Einstiegsseiten
(`/rollen/geschaeftsfuehrung/`, `/rollen/isb/`, `/rollen/devs/`),
automatisch generiert wie `index.mdx`/`zeitplan.mdx`/`vergleich.mdx`, aus
Feldern, die im Katalog bereits existieren — keine neue, frei erfundene
Zielgruppen-Einstufung pro Control.

- **Für Geschäftsführung**: die MUSS-Anforderungen des gesamten Katalogs,
  gruppiert nach Bereich, mit einer errechneten Kennzahl ("X von Y
  Anforderungen sind MUSS"). Ergänzt um einen Rechtskontext-Abschnitt
  (§ 28/§ 38 BSIG, § 43 GmbHG, § 93 AktG) und ein KPI-Rahmenwerk als
  Erklärung, nicht als Live-Tracking. Ein Toggle
  (`normal-SdT`/`erhöht`/beide) filtert die MUSS-Liste clientseitig — der
  Besucher wählt seine eigene, bereits bekannte Einstufung selbst aus; die
  Seite stuft nicht automatisch ein.
- **Für ISB**: die sechs PDCA-Phasen als Zyklus dargestellt, plus Verweise
  auf die beiden Werkzeuge, die diese Zielgruppe konkret braucht
  (Vorgänger-Mapping, Gefährdungen-Auflösung). Die heutige
  OSCAL/BSI-Backstory der Startseite zieht hierher um, wo sie fachlich
  hingehört, statt jedem Besucher aufgedrängt zu werden.
- **Für Devs**: die vierzehn operativen Themenfelder mit Anforderungs-Anzahl
  je Bereich, sortiert wie im Katalog — bewusst keine erfundene
  Unterkategorisierung ohne Quelle.
- Die Startseite wird umgebaut: statt "Was hier passiert" eine kurze
  Rollen-Auswahl, die auf die drei Seiten verweist.
- **Rechtlicher Rahmen, explizit als Konstruktionsregel**: die Seite gibt
  keine Rechts- oder Haftungsberatung und stuft niemanden automatisch in
  eine Kategorie ein. Jede rechtsnahe Aussage ist als Wiedergabe von
  Gesetzestext gekennzeichnet, mit Primärquellen-Link, und mit einem
  sichtbaren Disclaimer versehen. "Welche Gruppe bin ich" wird als
  **Kriterienerklärung** umgesetzt (die Schwellenwerte aus § 28 BSIG), nicht
  als automatischer Klassifikator.
- Kein Live-KPI-Tracking, kein Speichern von Nutzer-/Compliance-Daten —
  diese Seite bleibt eine Dokumentations-, keine GRC-Tracking-Anwendung.

## Alternativen

- **Automatischer Einstufungs-Assistent** ("beantworte 3 Fragen, wir sagen
  dir deine Kategorie") — verworfen. Eine falsche automatische Einstufung
  wäre ein echtes Haftungsrisiko für den Seitenbetreiber, nicht nur ein
  Komfortverlust. Stattdessen: die Kriterien erklären, der Besucher gleicht
  selbst mit seinen eigenen Zahlen ab.
- **Live-KPI-/Compliance-Tracking-Dashboard** — verworfen. Würde bedeuten,
  tatsächliche Compliance-Daten von Nutzer:innen zu speichern und für
  richtig zu garantieren — ein anderes Produkt mit einer anderen
  Haftungsklasse als eine Dokumentationsseite.
- **Per-Control-Zielgruppen-Tagging** (jedes Control redaktionell als
  "relevant für X" markieren) — verworfen. BSI liefert keine
  Zielgruppen-Klassifikation; das wäre reine redaktionelle Einschätzung,
  die bei jedem Katalog-Update manuell nachgepflegt werden müsste. Die
  bestehende Gruppen-/Pflicht-/Stufen-Struktur reicht aus und bleibt
  wartungsfrei bei Katalog-Updates.
- **Einheitliche Startseite beibehalten** — verworfen. Bedient keine der
  drei Zielgruppen gut und lässt die in der Recherche gefundene Lücke
  ungenutzt.

## Konsequenzen

### Positiv

- Füllt eine in der Wettbewerbsrecherche bestätigte echte Lücke.
- Nutzt zu 100 % bereits vorhandene Katalogfelder (Pflicht, Stufe, Gruppen)
  — kein neuer redaktioneller Pflegeaufwand bei Katalog-Updates.
- Rechtsnahe Inhalte sind direkt aus aktuellem Primärrecht belegt (BSIG in
  Kraft seit 2.12.2025), nicht aus einer sekundären Zusammenfassung.
- Die heutige Projekt-Backstory findet mit der ISB-Seite einen fachlich
  passenden Ort, statt jedem Erstbesucher aufgedrängt zu werden.

### Negativ / Trade-offs

- Rechtsnahe Inhalte erhöhen die Sorgfaltsanforderung an Formulierungen
  spürbar gegenüber dem Rest der Seite — Wortwahl muss bei jeder Änderung
  bewusst konservativ bleiben (Beschreibung von Gesetzestext, keine
  Bewertung des Einzelfalls).
- BSIG/GmbHG/AktG können sich ändern — die zitierten Paragraphen müssen bei
  Gesetzesänderungen erneut geprüft werden (kein automatischer Sync wie
  beim Grundschutz++-Katalog selbst).
- Größerer Eingriff in die Site-Navigation als bisherige Änderungen — Banner
  Quick-Nav, Sidebar und Startseite ändern sich gleichzeitig.
- Nur Hosted in dieser ersten Umsetzung; OSS-Variante (statisch, ohne
  Toggle) folgt als separater Schritt.

## Changelog

| Datum | Änderung | Von |
|-------|----------|-----|
| 2026-09-29 | Erstellt | Bruno |
