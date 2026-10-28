# 0012. Dokumenten-Landkarte: welche Dokumente der Katalog verlangt

## Status

Angenommen (Details dürfen sich mit begründetem Changelog-Eintrag ändern)

## Datum

2026-10-28

## Kontext

Wer vor einem Audit steht oder ein ISMS aufbaut, fragt nicht zuerst „Was muss ich tun?",
sondern „Welche Dokumente muss ich haben, und was gehört hinein?" Der Katalog beantwortet
das zum Teil. Bei 961 von 1.000 Anforderungen nennt das Feld `documentation` den
Dokumenttyp, in dem das Ergebnis festzuhalten ist (62 verschiedene Typen). Zu 66 Begriffen
liefert das BSI in `documentation_guidelines.csv` eine Definition, eine Kategorie und eine
Zielgruppe. Die Definitionen sind inhaltlich stark: Die für das Datensicherungskonzept nennt
Backup-Frequenz, Aufbewahrungsfristen, RTO und RPO, im Median sind sie 451 Zeichen lang.

Heute taucht das nur im Export auf (Blatt „Dokumente", 62 Zeilen). Auf der Seite selbst
steht es nirgends, und es gibt keine Adresse, die man weitergeben kann.

**Was die Daten nicht hergeben.** Das Feld `result` ist **kein Nachweis**. Es ist der
Gegenstand des Anforderungssatzes (NOT.4.10: „die Datensicherung getrennt von den
Originaldaten", nicht „Protokoll des Wiederanlauftests"). Eine Fachperson hat es als
Nachweis erwartet; die Daten sagen das nicht, und wir erfinden es nicht. Die Spalte
„bisher im IT-Grundschutz" der BSI-Tabelle trägt nur 4 von 66 Einträge, einer davon
„(todo)"; sie taugt nicht für eine Zuordnung alt nach neu.

Aus dem Katalog nachgerechnet (Commit `160c177`):

- 62 Dokumenttypen im Katalog; 31 davon hängen an mindestens einer MUSS-Anforderung,
  21 an nur ein oder zwei Anforderungen.
- 7 Dokumenttypen, die der Katalog nennt, fehlen in der BSI-Tabelle (zum Beispiel
  „Risikobetrachtung", „Beschaffungskriterien"); 2 stimmen nur in der Schreibweise
  überein, 53 exakt.
- Das ganze Paket für Webserver (451 Anforderungen) berührt 52 der 62 Dokumenttypen. Das
  unterscheidet kaum. Das, was die Kategorie selbst verlangt (87 Anforderungen, direkt
  und geerbt), nennt nur **13**. Cloud-Dienste: 15, Hostsysteme: 14, Gebäude: 9.

## Entscheidung

Wir bauen eine **Dokumenten-Landkarte** aus den BSI-Daten, ohne eigene Vorgaben:

1. **`/dokumente/`:** alle 62 Dokumenttypen, nach der Kategorie des BSI gruppiert, mit
   Zielgruppe, Zahl der Anforderungen und davon MUSS. Typen ohne Eintrag in der BSI-Tabelle
   stehen in einer eigenen Gruppe und sagen offen: „Zu diesem Dokumenttyp liefert das BSI
   keine Beschreibung."
2. **`/dokumente/<typ>/`:** die Definition des BSI wörtlich und mit Quelle, die Zielgruppe,
   und die Anforderungen, die das Dokument nennen (ID und Titel mit Link, Pflichtgrad,
   Stufe, Zielobjektkategorie), MUSS zuerst.
3. **An der Anforderung** eine Pille „Dokumentiert in: X" mit Link auf die Seite des Typs.
   Der Text der Definition wird nicht kopiert (er stünde bei „Konfigurationshistorie" bis
   zu 183-mal im Text).
4. **Auf jeder Zielobjekt-Seite** (ADR-0011) eine Tabelle „Dokumente zu diesen
   Anforderungen": die Typen, die die Anforderungen **dieser Kategorie** (direkt und
   geerbt) nennen, mit Anzahl. Dazu ein Satz, dass die Anforderungen ohne Kategorie und die
   Methodik-Praktiken weitere Dokumente nennen, mit Link auf `/dokumente/`.

Die Seiten sagen an prominenter Stelle, was „Dokumentiert in" bedeutet: der Dokumenttyp, in
dem das Ergebnis festzuhalten ist, **kein Nachweis und keine Prüfvorgabe**.

Zahlen werden erzeugt und auf einem zweiten Weg geprüft (CONTRIBUTING, „Numbers on the
site"): Anzahl und IDs je Dokumenttyp aus dem Rohtext des Katalogs, nachgerechnet gegen
die Export-CSV (Spalte „Dokumentiert in", Blatt „Dokumente"); die Tabellen auf den
Zielobjekt-Seiten gegen die Hierarchie der BSI-Tabelle. Ein absichtlich falscher Lauf muss
den Generator abbrechen lassen.

Die Listen auf den Seiten der Typen sind vom Suchindex ausgenommen (sonst stünde jede
Anforderung noch einmal im Index), die Definitionen des BSI nicht: Wer „RTO" oder
„Wiederanlauf" sucht, soll das Datensicherungskonzept finden.

## Alternativen

**Aufklappbar an jeder Anforderung: Dokument und Definition.** Das wäre die wörtliche
Umsetzung der Idee. Es wiederholt dieselbe Definition bis zu 183-mal, bläht Seiten und
Index, und es beantwortet nicht die Frage des ISB („Welche Dokumente brauche ich?"),
sondern nur „Wo steht diese Anforderung?".

**`result` als „Nachweis" anzeigen.** Verworfen: Die Daten sagen das nicht (siehe Kontext).
Wir würden eine Auslegung als Fakt ausgeben, und ein Prüfer, der sich darauf beruft, hätte
keine Quelle.

**Eigene „typische Nachweise" für alle Anforderungen.** Verworfen aus demselben Grund, dazu
wäre es unsere Auslegung in Händen von Menschen, die sie für eine Vorgabe halten.

**Nur den Export erweitern.** Das Blatt „Dokumente" gibt es schon. Es hat keine Adresse, die
man in einem Ticket oder einer Mail nennen kann, und es lässt sich nicht finden.

## Konsequenzen

### Positiv

- Eine Adresse für „Welche Dokumente brauche ich?", weitergebbar, mit der Definition des BSI
  und den Anforderungen dahinter.
- Auf den Zielobjekt-Seiten wird aus „Was muss ich für meinen Webserver tun?" auch „und was
  muss ich dazu dokumentieren?" (13 Dokumenttypen, nicht 52).
- Die Lücken des BSI werden sichtbar, ohne zu bewerten: 7 Dokumenttypen im Katalog, zu denen
  die Tabelle nichts sagt. Das passt zum Befund-Entwurf `dokumenttypen-katalog-und-csv`.
- 62 + 1 Seiten sind rein generiert und brauchen keine Pflege von Hand.

### Negativ / Trade-offs

- Die Seiten legen nahe, dass ein Dokument pro Typ gemeint ist. Der Katalog sagt nur, **in
  welchem Dokumenttyp** festzuhalten ist, nicht, dass jeder Typ ein eigenes Dokument sein
  muss. Die Seite sagt das ausdrücklich.
- Bis zu 183 Anforderungen auf einer Seite („Konfigurationshistorie"): lang, aber MUSS
  zuerst, und die Liste ist nicht im Suchindex.
- Die Definitionen sind Text des BSI. Es gilt dieselbe Quellenangabe und Lizenzlage wie für
  den Export (siehe Hinweis in den Download-Dateien).

## Ausblick (nicht entschieden)

Zwei Schritte, die auf dieser ADR aufbauen und eigene ADRs verdienen:

- **Pakete als Dateien:** je Zielobjektkategorie die Anforderungen als CSV, JSON und
  Markdown unter einer stabilen Adresse (zum Beispiel `/zielobjekte/webserver.csv`), mit
  den Spalten des Exports. Jira-Importe, GRC-Werkzeuge und Wikis könnten „das Webserver-
  Paket" direkt abholen.
- **Umsetzungsstand im Browser:** Wer die Excel-Datei mit Status, Zuständigen und Fristen
  ausgefüllt hat, lädt sie zurück und sieht, wo er steht: je Praktik, je Dokumenttyp, je
  Kategorie, welche MUSS-Anforderungen offen sind. Berechnet im Browser, die Daten
  verlassen den Rechner nicht. Das wäre der Schritt von einem Nachschlagewerk zu einem
  Werkzeug für die tägliche Arbeit.

## Festlegungen im Detail

1. **Adresse:** `/dokumente/` und `/dokumente/<typ>/`, kurz und weitergebbar wie
   `/zielobjekte/`.
2. **Reihenfolge auf der Übersicht:** nach der BSI-Kategorie, darin nach Zahl der
   MUSS-Anforderungen (das Verbindliche zuerst), dann alphabetisch.
3. **Typen ohne BSI-Beschreibung:** eigene Gruppe am Ende, mit dem offenen Satz „Zu diesem
   Dokumenttyp liefert das BSI keine Beschreibung." Sie unter die anderen zu mischen würde
   die Lücke verstecken.
4. **Zielobjekt auf den Dokument-Seiten:** als kleine Zeile unter dem Titel der Anforderung,
   nicht als eigene Spalte. Breite Spalten haben bei ADR-0011 auf dem Handy über den Rand
   geragt; Tabellen werden vor dem Deploy auch bei 320 px Zelle für Zelle geprüft.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-10-28 | Erstellt | giordano137  |
| 2026-10-28 | Status Angenommen; die vier offenen Punkte sind festgelegt (Adresse, Reihenfolge, Typen ohne Beschreibung, Zielobjekt als Zeile) | giordano137  |
| 2026-10-28 | Beim Bauen ergänzt: Typen ohne Kategorie und Typen ohne Beschreibung stehen in zwei getrennten Endgruppen (3 bzw. 7). Die Dokument-Seite hat eine Zeile „Nach Zielobjekt“ mit Links auf die Kategorieseiten, damit Dokumente und Zielobjekte sich gegenseitig verweisen. Die Stufe steht auf dem Handy als „Standard“/„Erhöht“, weil das volle Wort die Spalte auf 320 px in vier Zeilen zerlegt. | giordano137  |
