# 0005. Vorgänger-Anforderung (altes Kompendium → Grundschutz++): Links statt Volltext

> Entstanden, als das Projekt noch auf zwei Repos aufgeteilt war (ADR-0001/0002).
> Diese Trennung wurde mit [ADR-0008](0008-aufloesung-des-oss-hosted-splits.md) aufgelöst; die hier
> getroffene Entscheidung gilt unverändert, sie betrifft heute nur ein Repo.

## Status

Angenommen

## Datum

2026-09-29

## Kontext

`ROADMAP.md` (OSS) hatte als offenen Short-term-Punkt: "Previous requirement"
references from the official IT-GS2023-to-GS++ mapping file — old control
ID, title, and a link to BSI's own page, not the full old text". Das
sollte konkretisiert werden.

Zwei Datenquellen wurden geprüft:

1. **Die Mapping-Datei** `Grundschutz-PlusPlus/control_layer/Mappings/IT-GS2023-zu-GSpp/ITGS-to-GS++-mapping_collection.json`
   — 1185 einzelne Zuordnungen alt→neu (`itgs_id`, `relationship`
   [`equivalent-to`/`subset-of`/`superset-of`/`intersects-with`],
   Ziel-Control-ID). Liegt im selben offiziell offen lizenzierten
   BSI-Repo, das wir schon für den ganzen Katalog nutzen.
2. **Das alte IT-Grundschutz-Kompendium selbst** (Edition 2023, 111
   Bausteine) — offiziell von BSI als DocBook-XML bereitgestellt
   (`bsi.bund.de/.../XML_Kompendium_2023.html`), **aber**: anders als der
   neue Grundschutz++-Katalog (explizit CC BY-SA 4.0) ist die Lizenzlage
   fürs alte Kompendium unklar — BSI erlaubt freie Nutzung nur für
   nicht-kommerzielle Zwecke zur eigenen Umsetzung, und es gibt einen
   Hinweis, dass Tool-Anbieter, die Kompendium-Daten *verarbeiten*, einen
   Lizenzvertrag mit BSI (`it-grundschutz@bsi.bund.de`) brauchen. Genau
   das wäre der Fall, wenn wir den Volltext einlesen und auf unserer
   Seite neu darstellen. Zwei geprüfte Drittanbieter-JSON-Quellen
   (`nfelger/it-grundschutz-bausteine`, `gockelhahn/grundschmutz-tools`)
   lösen das nicht: erste ist falsche Edition (2022 statt 2023) und
   archiviert, zweite nur ein Tool unklarer Aktualität gegen dieselbe
   Quelle.

Wichtige Erkenntnis: **das Dateiformat ändert an der Lizenzfrage nichts**
— ob wir PDF, XML oder JSON verarbeiten, der geschützte Inhalt bleibt
derselbe. Eine Konvertierung würde die Lizenzfrage nicht umgehen.

Zusätzlich geprüft und bestätigt: BSI stellt jeden der 111 Bausteine auch
einzeln als PDF bereit, mit vorhersagbarer, aber nicht ratbarer URL (der
Kategorie-Ordner-Präfix 01–10 lässt sich nicht algorithmisch ableiten).
Einmal deterministisch aus der offiziellen Bausteine-Übersichtsseite
extrahiert (aus dem PDF-Dateinamen, nicht aus dem uneinheitlich
formatierten Linktext) — alle 111 Bausteine sauber aufgelöst, keine
Duplikate, Zahl deckt sich mit BSIs eigener Angabe. Gespeichert in
`Grundschutz-Projekt/bsi-kompendium-2023-bausteine.json` (Baustein-Ebene,
nicht Einzelanforderungs-Ebene — für Anforderungs-ID wie `OPS.1.1.5.A3-UA.1`
wird auf den Baustein `OPS.1.1.5` verwiesen, nicht auf eine Anker-Position
im PDF).

## Entscheidung

- **Kein alter Volltext.** Nur strukturelle Information: alte
  Anforderungs-ID(s), Beziehungstyp, und ein echter Link zum
  entsprechenden Baustein-PDF bei BSI selbst (aus der oben genannten,
  verifizierten Lookup-Datei — keine geratenen URLs).
- Reine Verlinkung ist unproblematisch unabhängig von der
  Kompendium-Lizenzfrage — wir verarbeiten/verbreiten keinen Inhalt,
  nur Navigation.
- **OSS:** eigene Text-Zeile (`**Vorgänger:** OPS.1.1.5.A3-UA.1 ·
  superset-of · [Baustein-PDF]`), analog zu Pflicht/Stufe/Aufwand.
- **Hosted:** farbige Pills pro Beziehungstyp mit Tooltip, der erklärt,
  was `equivalent-to`/`subset-of`/`superset-of`/`intersects-with`
  bedeuten (diese OSCAL-Begriffe sind nicht selbsterklärend).
- Ein Control kann mehrere alte IDs haben (viele-zu-eins/eins-zu-viele
  laut Mapping-Datei) — alle anzeigen, nicht nur die erste.

## Alternativen

- **Vollständiger alter Text neben dem neuen (Side-by-Side):** verworfen
  für jetzt — Lizenzfrage ungeklärt, siehe Kontext. Für später: BSI direkt
  fragen (`it-grundschutz@bsi.bund.de`), falls das Projekt wächst oder
  Nutzer:innen das explizit wollen — nicht implementieren und hoffen, dass
  es niemand bemerkt.
- **Alte Kompendium-PDFs selbst hosten/spiegeln:** verworfen — dasselbe
  Lizenzproblem wie Volltext-Rendering, zusätzlich unnötig (BSI hostet
  sie ja schon erreichbar).
- **PDF→JSON-Konvertierung als Umgehung:** verworfen — Formatkonvertierung
  ändert nichts an der Lizenzlage des zugrunde liegenden Inhalts.
- **Drittanbieter-Datensatz nutzen** (`nfelger/it-grundschutz-bausteine`):
  verworfen — falsche Edition (2022), archiviert, keine verlässliche
  Quelle für "gilt noch"-Genauigkeit.

## Konsequenzen

### Positiv

- Löst den offenen ROADMAP-Punkt, ohne rechtliches Risiko einzugehen.
- Nutzt ausschließlich bereits offen lizenzierte (Mapping-Datei) oder
  gar nicht "genutzte" (reine Links) Quellen.
- Echte, verifizierte Links statt geratener URLs.

### Negativ / Trade-offs

- Kein echter "Seite an Seite"-Vergleich — nur ID+Beziehung+Link, weniger
  eindrucksvoll als ursprünglich angedacht.
- `bsi-kompendium-2023-bausteine.json` muss bei jeder neuen
  Kompendium-Edition (jährlich) neu gescraped werden — manueller Schritt,
  nicht automatisiert (Akamai-Bot-Schutz verhindert einfaches
  Skript-Scraping ohne echten Browser).

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-09-29 | Erstellt | Bruno Deanoz |