# 0013. Das Anforderungspaket als teilbarer Link und als Datei

## Status

Vorgeschlagen

## Datum

2026-10-29

## Kontext

Der Schritt, an dem ein ISB im BSI-Standard 300-1 wirklich arbeitet, ist das **Anforderungspaket**:
Für die Assets der eigenen Institution (Webserver, Cloud-Dienste, Hostsysteme, ...) stellt er
zusammen, was gilt. Die Seite unterstützt das heute an drei Stellen, und keine davon lässt sich
weitergeben oder maschinell abholen:

- die Seiten je Zielobjektkategorie (ADR-0011) listen direkt zugeordnete, geerbte und die
  Anforderungen ohne Kategorie, aber ohne Link auf den Export und ohne Datei;
- der Export (`/export/`) filtert im Browser und erzeugt Excel oder CSV. Er liest aus der Adresse
  schon `?praktik=`, `?pflicht=`, `?stufe=`, `?aufwand=` und `?ziel=` (zum Beispiel
  `?ziel=Webserver,Cloud-Dienste`). Er **schreibt** die Auswahl aber nicht zurück in die Adresse, und
  „ohne Zielobjektkategorie" gibt es als Parameter nicht;
- die große JSON (`grundschutzpp-anforderungen.json`) enthält alles, aber wer sie nutzt, muss die
  **Vererbung selbst nachbauen**. Genau dort ist am 28. Oktober 2026 der Fehler entstanden (Befund
  `zielobjekt-vererbung-export-und-suchfilter`): Wer nur die direkte Kategorie auswertet, übersieht
  81 von 87 Anforderungen beim Webserver.

Wer einem Kollegen „das Paket für unsere Webserver" schicken, in ein Ticket oder Wiki legen oder in ein
GRC-Werkzeug laden will, hat heute keinen Weg, der die Regel schon enthält.

Aus dem Katalog nachgerechnet (Commit `160c177`, Webserver als Beispiel):

- 87 Anforderungen sind kategoriespezifisch (6 direkt, 81 geerbt), dazu kommen **364 ohne Kategorie**, die
  nach Standard 300-1 (3.4.1) in jedes Paket gehören. Zusammen 451, wie der Export sie liefert.
- Alle 39 Kategorienamen sind frei von Komma und Semikolon, `?ziel=A,B` ist also eindeutig; 11 Namen
  haben Leerzeichen oder Umlaute und brauchen URL-Kodierung.
- **Größe:** Ein in sich geschlossenes Paket je Kategorie wiederholt die 364 Anforderungen ohne Kategorie
  39-mal (83 % des Inhalts). Als CSV wären das 9,4 MB, als JSON 12,5 MB für alle Kategorien. Nur die
  kategoriespezifischen Zeilen plus eine gemeinsame Datei sind 2,2 MB CSV und 2,8 MB JSON. Alle Downloads
  zusammen sind heute 2,3 MB. Die erzeugten Dateien stehen im Repository, jede Katalogänderung des BSI
  schreibt sie neu.
- nginx komprimiert heute weder CSV noch Markdown (`gzip_types`).

## Entscheidung

Wir machen das Paket auf drei Wegen zugänglich, und zwar so, dass **die Regel (Vererbung, immer-im-Paket)
einmal im Generator steckt und nicht bei jedem Nutzer neu gebaut wird**.

1. **Auswahl als Link.** Der Export schreibt jede Änderung der Auswahl in die Adresse
   (`history.replaceState`, kein neuer Eintrag im Verlauf) und hat eine Schaltfläche „Link kopieren".
   Neu ist der Parameter `ohne=nein` (die Anforderungen ohne Kategorie weglassen; Standard ist, dass sie
   dabei sind). Der Link bildet jede Kombination ab, auch mehrere Kategorien (`?ziel=Webserver,Cloud-Dienste`),
   und jede Anforderung zählt dabei einmal (STM.2.1.4.2), weil der Filter Zeilen auswählt.
2. **Ein Block „Paket" auf jeder Kategorieseite** mit dem Link auf den Export (`/export/?ziel=<Kategorie>`),
   dem Hinweis „mit weiteren Kategorien kombinieren" und den Dateien (3).
3. **Dateien je Kategorie** unter stabilen Adressen im bestehenden Download-Ordner:
   `/downloads/pakete/<kategorie>.csv`, `.json` und `.md`. Dazu **eine gemeinsame Datei** für die
   Anforderungen ohne Kategorie: `/downloads/pakete/ohne-zielobjektkategorie.csv` und `.json`.
   - **CSV und JSON** sind kategoriespezifisch: direkt zugeordnete und geerbte Anforderungen, mit einer
     Spalte „Grund" (`direkt` oder `geerbt von <Kategorie>`). Wer das ganze Paket will, nimmt beide Dateien.
     Das bildet die Struktur des BSI ab (STM.2.1.4 und STM.2.1.5) und hält das Repository klein. Die JSON
     trägt in `meta` den Verweis auf die gemeinsame Datei und die Zahlen.
   - **Markdown** ist dagegen **vollständig** (kategoriespezifisch plus ohne Kategorie) und eine
     **Checkliste**: `- [ ] KONF.6.8 · Berechtigungen des Webserver-Prozesses · SOLLTE`, gruppiert nach Praktik,
     mit Link auf die Seite der Anforderung, ohne den Volltext. Sie ist zum Einfügen in ein Ticket, einen
     GitHub-Issue oder ein Wiki gedacht, wo man das Paket als Aufgabenliste abhaken will. Ohne Volltext bleibt
     sie klein (geschätzt rund 65 KB je Datei, 451 Zeilen zu je etwa 140 Zeichen; noch nicht gemessen). Am Ende steht, welche Dokumenttypen die Anforderungen nennen (ADR-0012).
   - **Jede Datei** trägt die Quellenzeile (BSI, CC BY-SA 4.0, Stand, bearbeitet von grundschutz-docs.de) wie der
     Export, und im Ordner liegt die `LIZENZ.txt`.

nginx bekommt `text/csv` und `text/markdown` in `gzip_types`.

**Absicherung** (CONTRIBUTING, „Numbers on the site"): `check_pakete()` liest die geschriebenen Dateien zurück
und rechnet auf zwei anderen Wegen nach: die ID-Menge je Kategorie aus dem Rohkatalog und der BSI-Hierarchie
(UUID), die Zahlen gegen die Kategorieseite (direkt, mit Vererbung, Paket gesamt) und gegen die Export-CSV.
Die Markdown-Checkliste muss kategoriespezifisch plus gemeinsame Datei ergeben. Die gemeinsame Datei muss genau
die Anforderungen ohne Kategorie enthalten. Im Browser wird geprüft, dass `/export/?ziel=Webserver` „451 von
1000" zeigt und dass die Auswahl ihren Weg in die Adresse und zurück findet.

## Alternativen

**Nur die Verlinkung auf den Export (Schritt 1 und 2), keine Dateien.** Der Export läuft im Browser mit
JavaScript. Ein Jira-Import, ein Skript oder ein GRC-Werkzeug kann ihn nicht aufrufen. Für Menschen reicht es,
für die Weiterverwendung nicht.

**Die große JSON genügt, die Nutzer filtern selbst.** Sie existiert bereits. Aber dann baut jeder die Vererbung
nach, und der Fehler vom 28. Oktober 2026 wäre das erwartbare Ergebnis. Vorberechnete Pakete tragen die Regel
mit.

**Variante A: jedes Paket in sich geschlossen (CSV und JSON).** Bequemer, eine Datei statt zwei. Aber 9,4 und
12,5 MB im Repository, 83 % davon Wiederholung, und jede Katalogänderung schreibt sie neu. Für die Markdown-Checkliste
ist die Wiederholung unproblematisch, weil sie ohne Volltext klein ist, dort gilt A.

**Eine Schnittstelle (API) mit Parametern.** Die Seite ist statisch und soll es bleiben (leichtgewichtig,
selbst hostbar). Der Export-Link mit Parametern ist die statische Entsprechung.

**Pakete für beliebige Kombinationen vorberechnen.** Es gibt 39 Kategorien, die Kombinationen sind
unbegrenzt. Die Kombination ist Sache des Exports (Link), nicht der Dateien.

## Konsequenzen

### Positiv

- Das Paket wird zu einem Link, den man verschickt, und zu einer Datei, die Werkzeuge abholen, mit der Regel
  schon darin. Das ist der Schritt vom Nachschlagewerk zum Austauschformat.
- Die Markdown-Checkliste macht aus „das Paket für unsere Webserver" in einem Klick eine abhakbare Aufgabenliste.
- Der Fehler vom 28. Oktober 2026 kann in den Dateien nicht mehr unbemerkt entstehen, weil `check_pakete()` ihn
  auf zwei Wegen nachrechnet.
- CSV und Markdown werden beim Ausliefern komprimiert (die CSV-Dateien etwa 8-fach kleiner, gemessen an 9,4 auf 1,1 MB).

### Negativ / Trade-offs

- **Die Adressen sind ein Versprechen.** Benennt das BSI eine Kategorie um, ändert sich die Adresse (Kennung aus
  dem Namen, siehe ADR-0011), und alte Links liefern 404, bis eine Weiterleitung eingerichtet ist. Wer die Dateien
  in ein Werkzeug einbindet, erwartet, dass sie bleiben.
- 39 Kategorien mal 3 Formate mal die gemeinsame Datei sind rund 120 neue erzeugte Dateien im Repository
  (rund 8 MB: 5,0 MB CSV und JSON gemessen, dazu geschätzt 2,5 MB Markdown), und jeder Sync-PR bei einer Katalogänderung zeigt sie mit. Der Diff wird länger.
- Das Paket hat zwei Gesichter: CSV/JSON in zwei Dateien, Markdown in einer. Das ist erklärbar (Daten setzt man
  zusammen, Checklisten kopiert man), muss aber auf der Seite klar stehen.
- Bei Anforderungen mit zwei Kategorien (39) gilt die Lesart „eine genügt", wie überall (unsere Lesart, nicht
  die des BSI).

## Offene Entscheidungen

1. **CSV/JSON als B (zwei Dateien, 2,2 und 2,8 MB, Vorschlag) oder als A (je eine Datei, 9,4 und 12,5 MB).**
2. **Markdown als Checkliste** (`- [ ]`, Vorschlag) oder als Tabelle.
3. **Adresse** `/downloads/pakete/<kategorie>.<format>` (Vorschlag, wie die bestehenden Downloads) oder unter
   `/zielobjekte/<kategorie>/`.
4. **Link-Schaltfläche:** Auswahl bei jeder Änderung in die Adresse schreiben (Vorschlag) oder nur beim Klick
   auf „Link kopieren".
5. **Dokumente in der Markdown-Datei** (Abschnitt am Ende, Vorschlag) oder weglassen.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-10-29 | Erstellt | giordano137  |
