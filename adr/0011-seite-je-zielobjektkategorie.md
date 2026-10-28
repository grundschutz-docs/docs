# 0011. Eine Seite je Zielobjektkategorie

## Status

Angenommen (Details dürfen sich mit begründetem Changelog-Eintrag ändern)

## Datum

2026-10-28

## Kontext

Wer ein Asset betreibt, fragt nicht nach einer Praktik, sondern nach seinem
System: „Was muss ich für meinen Webserver tun?" Der Katalog beantwortet das über
das Feld `target_object_categories` (Standard 300-1, 3.4) und die Hierarchie der
39 Zielobjektkategorien. Die Seite bietet das heute an drei Stellen an, und keine
beantwortet die Frage als Liste:

- die Pille „Gilt für: Webserver" an der einzelnen Anforderung,
- den Zielobjekt-Filter der Suche,
- den Filter im [Export](/export/).

Der Filter der Suche arbeitet mit **Seiten**, nicht mit Anforderungen. Wer
„Webserver" wählt, bekommt 8 Seiten, auf denen irgendwo eine passende Anforderung
steht (gemessen am Suchindex vom 28. Oktober 2026). Die Anforderungen selbst muss er
suchen. Der Export liefert die Liste, aber als Datei und nicht als Adresse, die man
einer Kollegin schicken kann.

Die Vererbung (STM.2.1.4.1, MUSS) macht die Liste größer, als die direkte Angabe
vermuten lässt. Am 28. Oktober 2026 ist das in Export und Suchfilter falsch
gewesen und korrigiert worden (Befund
[Die Zielobjekt-Auswahl ignorierte die Vererbung der Kategorien](/befunde/zielobjekt-vererbung-export-und-suchfilter/)).
Aus dem Katalog nachgerechnet (Commit `160c177`, 1.000 Anforderungen):

- **39 Kategorien**, in 7 Wurzeln, bis zu 4 Ebenen tief. Jede hat mindestens eine direkt
  zugeordnete Anforderung.
- Mit Vererbung kommen die Kategorien auf **5 bis 108 Anforderungen**. Webserver hat
  6 direkte und 87 mit Vererbung, Cloud-Dienste 9 und 108.
- **23 Kategorien haben weniger als 10 direkte Anforderungen.** Ohne die geerbten
  wären ihre Seiten dünn und irreführend.
- **364 Anforderungen haben keine Kategorie.** Nach Standard 300-1 (3.4.1) gehören sie
  in jedes Anforderungspaket.
- **39 Anforderungen haben zwei Kategorien**, keine mehr als zwei, und nie beide im
  selben Ast der Hierarchie. Der Katalog sagt nicht, ob „oder" oder „und" gemeint
  ist (Frage 3 in Mail 3 an das BSI, noch offen).

Eine Rückmeldung aus der Praxis (Ranking der fünf Ideen vom 28. Oktober 2026) stellt
diese Seite an die erste Stelle: eine dedizierte Adresse, die „direkte Anforderungen
und geerbte aus übergeordneten Kategorien sauber aufdröselt".

## Entscheidung

Wir erzeugen im Generator **eine Seite je Zielobjektkategorie** unter
`/zielobjekte/<kategorie>/` und eine Übersichtsseite `/zielobjekte/` mit den 39
Kategorien in ihrer Hierarchie.

Jede Kategorieseite hat drei Teile:

1. **Direkt zugeordnet:** die Anforderungen, die der Katalog für genau diese
   Kategorie nennt.
2. **Geerbt:** die Anforderungen der übergeordneten Kategorien (STM.2.1.4.1), je
   Elternkategorie gruppiert, mit dem Hinweis, warum sie gelten.
3. **Ohne Zielobjektkategorie:** ein Satz mit Verweis auf die 364 Anforderungen, die
   immer im Paket sind. Sie werden nicht aufgelistet, sondern nur gezählt und
   verlinkt.

Die Anforderungen erscheinen als **kompakte Zeile** (ID, Titel, Pflichtgrad,
Sicherheitsstufe) mit Link auf den Anker an der Praktikseite. Den Volltext der
Anforderung gibt es weiter nur an einer Stelle. Die Pille „Gilt für: Webserver" an der
Anforderung verlinkt auf die Kategorieseite.

Die Zahlen auf diesen Seiten sind **erzeugt und auf einem zweiten Weg geprüft**
(CONTRIBUTING, „Numbers on the site"):

- Die Anzahl je Kategorie und Teil wird aus den geschriebenen Seiten zurückgelesen und
  gegen eine Nachrechnung aus dem Rohtext des Katalogs und der Hierarchie der BSI-Tabelle
  (über UUID/ChildOfUUID) verglichen. Das ist dieselbe Nachrechnung wie bei der
  Export-Spalte „Gilt auch für Unterkategorien" und bei den Suchfilter-Marken.
- Zusätzlich muss „direkt + geerbt" je Kategorie der Zahl entsprechen, die der Export
  für die Auswahl ohne das Häkchen „ohne Zielobjektkategorie" liefert (Webserver 87).
  Das ist ein dritter, unabhängiger Weg.
- Der Generator bricht ab, wenn eine dieser Zahlen abweicht. Ob die Prüfung wirklich
  greift, wird einmal mit absichtlich falschem Code getestet.

**Anforderungen mit zwei Kategorien** stehen auf der Seite jeder ihrer beiden
Kategorien, mit dem Hinweis „gilt auch für …". Das entspricht der Auswahl im Export
(eine Kategorie genügt). Es ist **unsere Lesart** des Katalogs, nicht eine Aussage des
BSI, und die Seite sagt das, solange das BSI die Frage nicht beantwortet hat.

**Suchindex:** Die Listen auf den Kategorieseiten werden mit `data-pagefind-ignore`
vom Suchindex ausgenommen. Sonst stünde jede Anforderung mehrfach im Index: eine
Anforderung für „Anwendungen" erschiene auf der Seite jeder Unterkategorie. Das wäre
ein Mehrfaches an Treffern für denselben Text, und Kategorieseiten könnten die
Praktikseiten als Treffer verdrängen (letzteres ist eine Annahme, nicht gemessen). Titel und Beschreibung der Seite bleiben durchsuchbar, damit
„Webserver" die Kategorieseite findet.

Die Seiten sind deutsch, wie der Katalog. Eine englische Fassung gibt es nicht (siehe
Stand der englischen Seiten).

## Alternativen

**Nur der Filter (Zustand seit dem 28. Oktober 2026).** Behebt die Vererbung, aber
nicht das Finden: Treffer sind Seiten, nicht Anforderungen, und es gibt keine Adresse
zum Weitergeben. Bleibt als Ergänzung bestehen.

**Den Volltext der Anforderungen auf jeder Kategorieseite.** Bequemer zum Lesen,
aber bis zu 108 Anforderungen je Seite und jede Anforderung an mehreren Orten. Das
verdoppelt Inhalt, bläht den Index auf und macht jede Katalogänderung zu einer
Änderung an mehreren Stellen. Der Link auf den Anker genügt.

**Eine Seite mit clientseitigem Auswahlwerkzeug („Anforderungspaket").** Das ist der
Export, der schon existiert. Eine reine Adresse ohne JavaScript ist teilbar,
druckbar und von Suchmaschinen lesbar, und sie braucht keine neue Abhängigkeit
(CONTRIBUTING, „Keep it lightweight").

**Unter `/grundschutzpp/zielobjekte/` statt `/zielobjekte/`.** Konsistent mit
`/grundschutzpp/themen/`, aber länger. Die Rollenseiten liegen auch auf oberster
Ebene (`/rollen/`), und die Adresse soll in Gesprächen genannt werden. Offene
Entscheidung, siehe unten.

**Nur Umbenennen des Filters („direkt zugeordnet") und erklären.** Behebt die
Irreführung, nicht den Nutzen.

## Konsequenzen

### Positiv

- Eine teilbare Adresse beantwortet „Was muss ich für mein System tun?" mit direkten
  und geerbten Anforderungen, ohne Praktiken kennen zu müssen.
- Die Regel STM.2.1.4.1 wird sichtbar und prüfbar statt versteckt.
- Auffindbarkeit: Begriffe wie „Anforderungen Webserver" treffen eine Seite, die genau
  das beantwortet.
- Die Zahlen sind in drei Wegen abgesichert (Seite, Nachrechnung, Export).

### Negativ / Trade-offs

- 40 neue Seiten (39 + Übersicht) im Generator, die bei jedem Katalog-Sync
  überschrieben werden. Handänderungen dort gehen verloren (siehe README, „How the
  docs are generated").
- Die Lesart für Anforderungen mit zwei Kategorien ist unsere. Antwortet das BSI
  anders („und" statt „oder"), ändern sich die Listen von bis zu 39 Anforderungen.
- Die Seite enthält die Vererbung **nicht** für die in 67 Fällen genannten
  `required`-Abhängigkeiten zwischen Anforderungen. Wer die Pakete vollständig
  zusammenstellen will, folgt weiter den Links an den Anforderungen.
- Die Kategorieseiten sind nicht im Suchindex. Wer nach dem Wortlaut einer Anforderung
  sucht, landet weiter auf der Praktikseite, was gewollt ist.

## Festlegungen im Detail

1. **Adresse:** `/zielobjekte/<kategorie>/`, wie `/rollen/` auf oberster Ebene.
   Die Adresse wird in Gesprächen und Tickets weitergegeben und soll kurz bleiben.
2. **Kennung:** Name der Kategorie in Kleinbuchstaben, Umlaute ausgeschrieben,
   Leerzeichen als Bindestrich (`it-systeme`, `einkaeufe`). Ein „ä" in der Adresse
   wird beim Kopieren zu `%C3%A4`. Der Generator bricht ab, wenn zwei Kategorien
   dieselbe Kennung bekommen. *Risiko:* Benennt das BSI eine Kategorie um, ändert
   sich die Adresse. Der tägliche Sync zeigt das im PR, dann wird eine Weiterleitung
   angelegt. Eine feste ID wäre stabiler, aber nicht weitergebbar.
3. **Reihenfolge innerhalb eines Teils:** nach Pflichtgrad (MUSS, SOLLTE, KANN), dann
   nach ID. Wer die Liste abarbeitet oder auf ein Audit vorbereitet, will das
   Verbindliche zuerst. Eine Spalte „Praktik" zeigt die Herkunft. Das Tabellenformat
   folgt der MUSS-Tabelle der Geschäftsführungsseite.
4. **Übersichtsseite:** die Hierarchie mit drei Zahlen je Kategorie: *direkt*, *mit
   Vererbung* und *Paket gesamt* (mit Vererbung plus die 364 ohne Kategorie; für
   Webserver 6, 87 und 451, wie der Export). Oben stehen zwei, drei Sätze zur
   Vererbung mit dem Webserver als Beispiel und ein Link auf die Methodik. Auf den
   Kategorieseiten steht nur ein Einzeiler dazu.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-10-28 | Erstellt | giordano137  |
| 2026-10-28 | Status Angenommen; die vier offenen Punkte sind festgelegt (Adresse, Kennung, Reihenfolge, Übersichtsseite) | giordano137  |
