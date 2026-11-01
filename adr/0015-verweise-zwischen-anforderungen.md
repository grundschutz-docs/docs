# 0015. Verweise zwischen Anforderungen: Voraussetzung und verwandt

## Status

Angenommen (Details dürfen sich mit begründetem Changelog-Eintrag ändern)

## Datum

2026-11-01

## Kontext

Der Katalog verknüpft Anforderungen untereinander (OSCAL `links`): `required` nennt eine Voraussetzung, `related` eine
verwandte Anforderung. Aus dem Katalog nachgerechnet (Commit `10f3c22`): 67 Voraussetzungs-Verweise bei 59 Anforderungen
und 210 Verwandt-Verweise bei 171, zusammen betreffen sie 216 Anforderungen. Alle Ziele gibt es im Katalog, es gibt keine
Selbstverweise. Die Seite zeigte davon bisher nichts.

**Was die Daten nicht hergeben.** Der Katalog erklärt nicht, was „verwandt" genau heißt, und er sagt nichts über eine
Reihenfolge der Umsetzung. „Voraussetzung" ist die Angabe des BSI und keine Planungsempfehlung dieser Seite. Von den
210 Verwandt-Verweisen steht nur etwa die Hälfte (96) auch in der Gegenrichtung.

## Entscheidung

- Unter den Kennzeichen jeder Anforderung stehen bis zu drei Zeilen mit Links: **Voraussetzung laut Katalog**, **Ist
  Voraussetzung für** (die Gegenrichtung von `required`) und **Verwandt laut Katalog**. Die ID ist der Linktext, der
  Titel steht als Tooltip. Die Zeilen stehen nicht im Suchindex.
- „Verwandt" zeigt **beide Richtungen** der Verweise. Verwandtschaft ist ihrer Natur nach gegenseitig, und eine
  Anforderung soll auch dann auf ihre Verwandte zeigen, wenn nur die andere Seite im Katalog darauf verweist. Das ist eine
  Darstellungsentscheidung, keine Aussage des BSI. Die Zeile sagt deshalb „laut Katalog".
- Keine Reihenfolge, keine Umsetzungsplanung, keine Bewertung. Die Seite zeigt, was im Katalog steht.
- Selbstprüfung: `check_zusammenhang()` liest die Praktikseiten zurück und rechnet je Anforderung gegen den Rohtext des
  Katalogs nach (eigener Code, nicht der, der die Seiten erzeugt). `test_zusammenhang.py` prüft ohne Katalog, dass jeder
  Verweis auf einen vorhandenen Anker der richtigen Seite zeigt.

## Folgen

- Die generierten Praktikseiten werden länger: 333 Verweiszeilen insgesamt.
- Die Verweise stehen noch nicht im Export (CSV, Excel, JSON). Eine Spalte „Voraussetzungen" wäre für die Planung der
  nächste Schritt.
