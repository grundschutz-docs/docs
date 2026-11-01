# 0014. Gefährdungs-Ansicht: je elementarer Gefährdung die Anforderungen, die der Katalog ihr zuordnet

## Status

Angenommen (Details dürfen sich mit begründetem Changelog-Eintrag ändern)

## Datum

2026-11-01

## Kontext

Jede Anforderung nennt im Katalog null bis mehrere der 47 elementaren Gefährdungen (G 0.1 bis G 0.47, Eigenschaft
`threats`). Auf der Seite stand das bisher nur als Pille an der einzelnen Anforderung („Gefährdungen: G 0.26, G 0.18"),
ohne Link und ohne die Gegenrichtung. Wer eine Risikoanalyse vorbereitet, fragt aber andersherum: „Welche Anforderungen
ordnet der Katalog der Gefährdung G 0.18 zu?" Dafür gab es keine Adresse, nur den Export (Spalte „Gefährdungen") und die
Suche.

Aus dem Katalog nachgerechnet (Commit `10f3c22`): 2009 Zuordnungen bei 1000 Anforderungen. G 0.18 („Fehlplanung oder
fehlende Anpassung") steht an 385 Anforderungen, G 0.23 an 142, G 0.30 an 130. `basethreats.csv` des BSI liefert zu
jeder der 47 Gefährdungen einen Begriff und eine Definition (CC BY-SA 4.0).

**Was die Daten nicht hergeben.** Die Zuordnung ist keine Risikobewertung. Dass G 0.18 an 385 Anforderungen steht, sagt
nichts darüber, wie wichtig die Gefährdung für eine Institution ist. Der Katalog sagt auch nicht, ob eine Anforderung die
Gefährdung ganz oder teilweise abdeckt.

## Entscheidung

- Eine Seite je Gefährdung unter `/gefaehrdungen/<id>/` (`g-0-18`) und eine Übersicht, vom Generator erzeugt wie die
  Zielobjekt- und Dokumentseiten (`render_gefaehrdung_pages()`).
- Jede Seite zeigt: Zahl der zugeordneten Anforderungen und ihre Verteilung auf MUSS, SOLLTE und KANN, die Definition des
  BSI wörtlich und mit Quelle, die Verteilung nach Praktik und die Tabelle der Anforderungen. Die Pille „Gefährdungen" an
  jeder Anforderung verlinkt auf diese Seiten.
- **Keine Bewertung.** Die Seiten sagen ausdrücklich, dass die Zuordnung keine Risikobewertung ist und die Risikoanalyse der
  Institution entscheidet. Keine Rangfolge, kein „wichtigste Gefährdungen", keine Empfehlung (rote Linie 1, siehe
  Marktanalyse Abschnitt 9). Die Übersicht sortiert nach der Nummer des BSI, nicht nach der Zahl der Anforderungen.
- Selbstprüfung: `check_gefaehrdungen()` liest die erzeugten Seiten zurück und rechnet gegen den Rohtext des Katalogs
  (nicht gegen den Code, der die Seiten erzeugt hat): welche Anforderungen je Gefährdung, wie viele MUSS, wie viele
  Zuordnungen insgesamt. `test_gefaehrdungen_seiten.py` rechnet zusätzlich gegen die Export-JSON.
- Neuer Ausgabeordner: `src/content/docs/gefaehrdungen/` steht im `add-paths` des Sync-PRs (`check_sync_paths()`).

## Folgen

- G 0.18 hat eine Seite mit 385 Zeilen (rund 190 KB HTML). Sie ist lang, aber sie ist die Antwort auf die Frage.
- Kommt beim BSI eine Gefährdung dazu oder fällt eine weg, ändert sich die Zahl der Seiten; der Generator bricht ab, wenn
  der Katalog eine Gefährdung nennt, die `basethreats.csv` nicht kennt.
- Die Adresse („G 0.18" → `g-0-18`) ist in `tag_slug()` (Generator) und `ControlMeta.astro` doppelt geschrieben. Eine
  Abweichung fängt der Link-Prüfer des Builds.
