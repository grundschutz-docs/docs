# 0006. Vergleichsseite alt↔neu + Quick-Nav im Header

> Entstanden, als das Projekt noch auf zwei Repos aufgeteilt war (ADR-0001/0002).
> Diese Trennung wurde mit [ADR-0008](0008-aufloesung-des-oss-hosted-splits.md) aufgelöst; die hier
> getroffene Entscheidung gilt unverändert, sie betrifft heute nur ein Repo.

## Status

Angenommen

## Datum

2026-09-29

## Kontext

ADR-0005 brachte "Vorgänger"-Referenzen direkt an einzelnen
Grundschutz++-Controls — aber nur einseitig: man findet den alten Bezug,
wenn man schon auf der neuen Seite ist. Der eigentliche Use Case ist oft
umgekehrt: jemand kennt eine alte ID (z. B. `OPS.1.1.5`, weil sie/er sie
gerade in der eigenen Dokumentation vor sich hat) und will wissen, was
Grundschutz++ dazu sagt — ohne vorher zu wissen, in welcher der 20
Themenfeld-Seiten das steht.

Zusätzlich wurde gewünscht, die wichtigsten Seiten (Übersicht, Zeitplan,
jetzt auch die Vergleichsseite) prominenter im Header statt nur in der
Sidebar zu verlinken. Starlights `Header.astro` hat dafür keinen
Erweiterungspunkt — das Layout ist ein fein abgestimmtes Grid
(Titel/Suche/Icons), in das sich kein zusätzlicher Link einfügen lässt,
ohne das Grid zu brechen. Ein Full-Override von `Header.astro` wäre
möglich, aber riskant (responsive Grid-Mathematik nachbauen).

## Entscheidung

- **Neue Seite `/vergleich/`** — alle 1185 Zuordnungen aus
  `ITGS-to-GS++-mapping_collection.json`, gruppiert nach
  Grundschutz++-Themenfeld (wie die Katalog-Übersicht), Tabelle
  Alte-ID / Beziehung / Neue-ID (verlinkt zur echten Control-Seite).
- **OSS:** statische Tabelle. Pagefind (schon integriert) durchsucht die
  Seite automatisch mit — Suche nach "OPS.1.1.5" im normalen Suchfeld
  findet die Vergleichsseite.
- **Hosted:** zusätzlich ein Live-Filter-Eingabefeld oben auf der Seite
  (Vanilla JS, kein Framework/Hydration nötig) — filtert Tabellenzeilen
  client-seitig. **Muss gegen beide ID-Spalten gleichzeitig matchen**
  (Substring, nicht nur exakt), damit "OPS.1.1.5" eingetippt alle
  `OPS.1.1.5.A*`-Unteranforderungen zeigt, unabhängig davon, ob man von
  der alten oder neuen Seite kommt.
- **Quick-Nav im Header:** kein Header-Override — stattdessen die
  bestehende `Banner.astro` (einziger sitewide-fest-verdrahteter
  Erweiterungspunkt, schon `position: fixed`, schon in `--banner-height`
  eingerechnet) um eine zweite Zeile mit Links (Übersicht · Status &
  Zeitplan · Vergleich) ergänzt, unter der bestehenden Pilotphase-Meldung.
  `--banner-height` entsprechend für zwei Zeilen angepasst.

## Alternativen

- **`Header.astro` komplett überschreiben, um Nav-Links einzubauen:**
  verworfen — deutlich höheres Risiko (responsive Grid-Berechnungen
  nachbauen), für einen reinen Zusatz-Link unverhältnismäßig.
- **Neue eigene fixed-position Nav-Leiste statt Banner-Erweiterung:**
  verworfen — hätte eine komplett neue Höhen-Variable und eigene
  Anpassungen an allen Stellen gebraucht, die schon `--banner-height`
  nutzen (Sidebar, Main-Frame, Right-Sidebar) — die bestehende Variable
  zu erweitern ist weniger Angriffsfläche für Fehler.
- **Vergleichsseite nach altem Baustein statt neuem Themenfeld gruppieren:**
  verworfen — die neue Themenfeld-Struktur ist die primäre Navigation
  dieser Seite, alte IDs sind der Fremdkörper hier, nicht umgekehrt.
- **Hosted-Filter nur gegen die alte ID-Spalte matchen** (da das der
  Haupt-Use-Case ist): verworfen — matcht auch gegen die neue ID, kostet
  nichts extra und deckt den Fall "ich kenne schon die neue ID, will alle
  Vorgänger sehen" gleich mit ab.

## Konsequenzen

### Positiv

- Löst den eigentlichen Use Case (von alter ID zu neuer Anforderung
  springen), nicht nur die einseitige Vorgänger-Anzeige aus ADR-0005.
- Kein Eingriff in Starlights Header-Interna — geringeres Risiko für
  Layout-Brüche bei künftigen Starlight-Updates.
- Wiederverwendung der schon vorhandenen, korrekt positionierten
  Banner-Infrastruktur statt einer zweiten eigenen Lösung.

### Negativ / Trade-offs

- Banner trägt jetzt zwei unterschiedliche Zwecke (Status-Meldung +
  Navigation) statt eines — vertretbar angesichts der Alternative (Risiko
  am Header), aber architektonisch nicht ganz sauber getrennt.
- Zwei unabhängige Implementierungen (OSS statisch, Hosted mit JS-Filter)
  müssen bei Strukturänderungen der Vergleichsseite synchron gehalten
  werden — wie immer bei diesem Repo-Split (ADR-0001), in `SYNC.md`
  vermerken. **Entfallen mit [ADR-0008](0008-aufloesung-des-oss-hosted-splits.md):**
  eine Implementierung, kein Abgleich mehr nötig.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-09-29 | Erstellt | Bruno Deanoz |
| 2026-09-29 | Korrektur (später am selben Tag): die Quick-Nav-Zweitzeile im Banner wurde doch in eine eigene `Header.astro`-Überschreibung ausgezogen (gleicher Overrides-Mechanismus wie `ThemeSelect`/`Hero`/`Footer`/`Banner`/`SocialIcons`, kein Sonderfall). Grund: Banner ist für eine temporäre Statusmeldung gedacht, permanente Navigation gehört semantisch nicht dorthin — der oben unter "Negativ/Trade-offs" genannte Punkt ("zwei Zwecke in einem Banner") wurde als real genug bewertet, um die ursprüngliche Risikoabwägung zu revidieren. Beim tatsächlichen Lesen von Starlights `Header.astro`-Quellcode stellte sich zudem heraus, dass das Risiko geringer war als angenommen: die mittlere Grid-Spalte (Suche) füllt nicht die volle Breite, Nav-Links passen dort hinein, ohne die für die Sidebar-Ausrichtung kritische `grid-template-columns`-Formel anzufassen. Banner zeigt jetzt nur noch die Pilotphase-Meldung. | Bruno Deanoz |