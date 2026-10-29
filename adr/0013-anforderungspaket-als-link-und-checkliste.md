# 0013. Das Anforderungspaket als sicherer Link und als Checkliste aus der Auswahl

## Status

Angenommen (Details dürfen sich mit begründetem Changelog-Eintrag ändern)

## Datum

2026-10-29

## Kontext

Der Schritt, an dem ein ISB im BSI-Standard 300-1 wirklich arbeitet, ist das **Anforderungspaket**:
Für die Assets der eigenen Institution (Webserver, Cloud-Dienste, Hostsysteme, ...) stellt er
zusammen, was gilt. Die Seiten je Zielobjektkategorie (ADR-0011) zeigen das je Kategorie, der Export
(`/export/`) filtert beliebige Kombinationen im Browser und erzeugt Excel oder CSV. Was fehlt, ist der
Weg **aus der Seite heraus**: das Paket einem Kollegen schicken, in ein Ticket oder Wiki legen.

Zwei Befunde aus dem Code und der Praxis bestimmen den Umfang:

**Die Export-Seite liest Adress-Parameter, schreibt sie aber nicht, und ein falscher Wert wirkt stumm.**
Sie versteht `?praktik=`, `?pflicht=`, `?stufe=`, `?aufwand=` und `?ziel=` (zum Beispiel
`?ziel=Webserver,Cloud-Dienste`). Nennt ein Link eine Kategorie, die es nicht (mehr) gibt, bleibt kein Kästchen
angehakt, der Filter greift nicht, und die Seite zeigt „Alle 1000 Anforderungen", ohne Hinweis. Wer einen Link
auf „das Webserver-Paket" aufbewahrt und das BSI die Kategorie umbenennt, bekommt unbemerkt den ganzen Katalog.
Das ist die Art „sieht richtig aus, ist falsch", die uns am 28. Oktober 2026 schon einen Befund gekostet hat.
Bevor Links ein Weg zum Teilen werden, muss das sicher sein. Dazu fehlt der Parameter für „ohne
Zielobjektkategorie" (der Zustand des Kästchens geht beim Teilen verloren), und alle 39 Kategorienamen sind frei
von Komma und Semikolon, 11 brauchen nur URL-Kodierung.

**Der belegte Bedarf ist ein Markdown für Tickets und Wikis.** Eine Praxisstimme (Rangliste vom 28. Oktober 2026)
wünscht sich ein Control als sauberes Markdown für Jira, GitHub-Issues und Confluence, mit ID, Pflichtgrad,
Titel und Permalink. Für CSV oder JSON je Kategorie, die Werkzeuge abholen, gibt es **keinen** belegten Bedarf,
das war eine Annahme (siehe Alternativen).

**Was Jira und Confluence mit Markdown tun** (offizielle Atlassian-Seiten, abgerufen am 29. Oktober 2026):
Beim **Tippen** wandelt der Editor `[]` plus Leerzeichen in eine Aufgabe („action item") um, dazu Listen,
Überschriften und Markdown-Links ([Jira Cloud](https://support.atlassian.com/jira-software-cloud/docs/markdown-and-keyboard-shortcuts/),
[Confluence Cloud](https://support.atlassian.com/confluence-cloud/docs/available-markdown-commands/)).
Was beim **Einfügen** von fertigem Markdown passiert, steht auf keiner der Seiten (Jira: „you can copy raw
markdown into the Atlassian editor", ohne Aussage zur Umwandlung). GitHub unterstützt `- [ ]`-Aufgabenlisten
ausdrücklich ([GFM-Spezifikation](https://github.github.com/gfm/),
[GitHub Docs](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-tasklists)).
Ob ein eingefügtes `- [ ]` in Jira oder Confluence zur Aufgabe wird, ist also **nicht belegt**, und wir
versprechen es nicht.

## Entscheidung

Wir bauen drei kleine Dinge, die **ohne neue erzeugte Dateien und ohne neue Versprechen** auskommen. Das
Paket entsteht aus der **Auswahl**, nicht aus Festdateien: Ein ISB hat selten genau eine Kategorie, er hat
Webserver plus Cloud-Dienste plus Hostsysteme, nur MUSS, nur Standardstufe.

1. **Auswahl als sicherer Link.** Der Export schreibt jede Änderung der Auswahl in die Adresse
   (`history.replaceState`, kein neuer Verlaufseintrag) und hat eine Schaltfläche „Link kopieren". Neu ist
   `ohne=nein` (die Anforderungen ohne Zielobjektkategorie weglassen; Standard ist, dass sie dabei sind).
   **Nennt ein Link einen Wert, den es nicht gibt, steht eine sichtbare Meldung** („Die Kategorie ‚X' gibt es
   nicht (mehr), sie wird ignoriert") und der Filter läuft nicht still über alles. Das gilt für alle fünf
   Parameter.
2. **Die Auswahl als Checkliste kopieren.** Drei ehrlich benannte Wege, weil das Verhalten beim Einfügen vom
   Ziel abhängt:
   - **„Markdown kopieren":** reiner Text, `- [ ] [KONF.6.8](https://…) · Berechtigungen des Webserver-Prozesses · SOLLTE`,
     nach Praktik gruppiert, in ID-Reihenfolge, ohne Volltext. Für GitHub-Issues und Markdown-Wikis.
   - **„Formatiert kopieren":** dieselbe Liste als HTML (Liste mit Links) **und** als reiner Text in der
     Zwischenablage. Das ist der übliche Weg in Rich-Text-Editoren (Jira, Confluence, Word, E-Mail). Ob die
     Atlassian-Editoren daraus Listen und Links machen, ist nicht dokumentiert und wird von der Praxis getestet.
   - **„Als .md speichern":** die Markdown-Datei als Download, und zugleich die Rückfallebene, wenn der Browser
     die Zwischenablage nicht freigibt.
   - **Inhalt:** oben die Auswahl in Worten, die Zahl und der **Link auf genau diese Auswahl**, damit der
     Empfänger sie live öffnen kann; unten die Dokumenttypen, die diese Anforderungen nennen (mit Zahl und Link auf
     die Seite des Typs, ADR-0012) und die Quellenzeile (BSI Grundschutz++, Stand, CC BY-SA 4.0, bearbeitet von
     grundschutz-docs.de). Kein Volltext der Anforderungen, damit die Liste in einem Ticket lesbar bleibt und
     nicht BSI-Text in Massen kopiert; der Link führt zum Text.
3. **Verlinkung.** Jede Kategorieseite bekommt einen Hinweis „Dieses Paket exportieren" mit dem Link
   `/export/?ziel=<Kategorie>` und „mit weiteren Kategorien kombinieren". Die Export-Seite bekommt einen kurzen
   Abschnitt **„Für Werkzeuge"**: Die JSON enthält je Anforderung `zielobjekte` und `unterkategorien`; wer eine
   Kategorie sucht, prüft beide, und die Vererbung ist damit schon richtig. Drei Zeilen Beispiel.

**Absicherung:** Es entstehen keine erzeugten Daten, also keine neue Generator-Prüfung. Die Auswahl und das
Markdown werden im Browser gegen den Katalog nachgerechnet (die ID-Menge einer Auswahl aus dem Rohkatalog und der
BSI-Hierarchie, unabhängig vom Filtercode), der Hin- und Rückweg des Links, die Meldung bei einem unbekannten Wert,
und eine Prüfung wird absichtlich gebrochen. Das Markdown entsteht in einer reinen Funktion, die ohne Seite testbar ist.

## Alternativen

**Dateien je Kategorie (CSV, JSON, Markdown) unter stabilen Adressen.** Zurückgestellt, bis jemand konkret sagt,
dass er sie abholt (siehe die interne Ideenliste). Gründe: kein belegter Bedarf; stabile Adressen sind ein
Versprechen, und benennt das BSI eine Kategorie um, bräuchten wir Weiterleitungen; rund 120 erzeugte Dateien
(bis 26 MB roh, wenn jedes Paket in sich geschlossen ist) würden jede Katalogänderung des BSI im Repository-Diff
mitschleppen; und die Auswahl bildet Kombinationen ab, die Festdateien nicht abbilden können.

**Nur ein Markdown-Knopf je Anforderung (die Praxis-Idee wörtlich).** Hilft bei einer Anforderung, nicht beim Paket.
Bleibt als kleine spätere Ergänzung denkbar, wenn jemand sie vermisst.

**Eine Schnittstelle (API).** Die Seite ist statisch und soll es bleiben (leichtgewichtig, selbst hostbar).
Der Link mit Parametern ist die statische Entsprechung.

**Markdown mit Volltext.** In einem Ticket unlesbar und kopiert BSI-Text in Massen. Der Link führt zum Text.

**Kein Tracking, um die Nutzung zu messen.** Qualität statt Traffic. Ob die Funktion hilft, fragen wir die
Praxis, wir zählen es nicht.

## Konsequenzen

### Positiv

- Das Paket wird zu einem Link, den man verschickt und der richtig bleibt, und zu einer Checkliste, die man in
  Ticket, Wiki oder Mail einfügt. Alles aus der Auswahl, also für jede Kombination.
- Die stille Falle (falscher Wert wirkt wie „alles") ist geschlossen und gilt für alle Parameter.
- Es entstehen weder neue Dateien noch neue Adress-Versprechen, das Repository wächst nicht.
- Die Vererbung steckt weiter an einer Stelle (Filter plus `unterkategorien`), und der Hinweis „Für Werkzeuge"
  zeigt, wie man sie richtig benutzt.

### Negativ / Trade-offs

- Das Einfügen in Jira und Confluence ist nicht belegt. Wir sagen es offen und lassen die Praxis testen;
  schlimmstenfalls wird aus `- [ ]` eine Aufzählung mit „[ ]", das ist lesbar.
- Die Zwischenablage verhält sich je Browser unterschiedlich (`ClipboardItem` mit zwei Formaten ist nicht überall
  gleich verfügbar). Rückfallebene: nur Text, dann der Download.
- Links tragen Kategorienamen. Benennt das BSI eine Kategorie um, meldet der Link es sichtbar, liefert aber nicht
  mehr die alte Auswahl.
- Bei Anforderungen mit zwei Kategorien (39) gilt die Lesart „eine genügt", wie überall (unsere Lesart, nicht
  die des BSI).

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-10-29 | Erstellt (zuerst mit Dateien je Kategorie vorgeschlagen) | giordano137  |
| 2026-10-29 | Umfang verkleinert und angenommen: Festdateien je Kategorie zurückgestellt (kein belegter Bedarf, Adress-Versprechen, bis 26 MB Repository-Last), stattdessen sicherer Link aus der Auswahl und Checkliste. Grund: Beim Prüfen des Codes fiel die stille Falle bei unbekannten Parametern auf, und die Recherche zu Jira und Confluence zeigte, dass das Einfügen von Markdown nicht dokumentiert ist, daher zwei benannte Kopierwege statt eines. | giordano137  |
