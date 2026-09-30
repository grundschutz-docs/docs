# 0004. Sichtbarer Druck/PDF-Export-Button — geteiltes Feature, nicht Hosted-only

> Entstanden, als das Projekt noch auf zwei Repos aufgeteilt war (ADR-0001/0002).
> Diese Trennung wurde mit [ADR-0008](0008-aufloesung-des-oss-hosted-splits.md) aufgelöst; die hier
> getroffene Entscheidung gilt unverändert, sie betrifft heute nur ein Repo.

## Status

Angenommen

## Datum

2026-09-29

## Kontext

Beide Homepages (OSS und Hosted) behaupten: "Jede Gruppenseite lässt sich
direkt über die Browser-Druckfunktion als PDF exportieren." Beim Nachprüfen
dieser Zusage kamen zwei Probleme heraus:

1. **Unentdeckbar:** Die Funktion existiert nur implizit über Cmd+P/Strg+P
   — niemand liest die Startseite genau genug, um das zu wissen. Ein Text-
   Hinweis ist keine UI.
2. **Ungetestet/kaputt für Hosted:** Starlights eigenes `print.css` deckt
   nur Starlight-eigene Komponenten ab (`.sl-badge`, Sidebar, etc.). Unsere
   Eigenbauten — `ControlMeta`s `--pill-*`-Farben (Hosted) und die
   schwebende Glas-Chrome (`position: fixed`, `backdrop-filter`, in
   beiden Repos identisch, da `custom.css` von OSS nach Hosted kopiert
   wurde) — werden von keinem `@media print`-Block erfasst.

## Entscheidung

- Ein echter, sichtbarer Druck/Export-Button (Icon im Header, `download`-
  Icon aus Starlights Icon-Set, `onclick="window.print()"`) — **in
  beiden Repos**, nicht nur Hosted.
- Dazu in beiden Repos ein `@media print`-Block für die schwebende Glas-
  Chrome (Header/Sidebar per `display: none`, Banner ausblenden).
- Zusätzlich in Hosted: `@media print`-Regeln für `ControlMeta`s Pills
  (druckbare, kontrastreiche Farben statt der Bildschirm-OKLCH-Töne,
  `print-color-adjust: exact`, Tooltip-Overlay ohnehin durch fehlenden
  `:hover` im Druck automatisch inaktiv).

## Alternativen

- **Nur die CSS-Lücke stillschweigend fixen, ohne Button** (Cmd+P bleibt
  einzige Zugangsart): verworfen — löst nicht das Kernproblem
  Unentdeckbarkeit, nur die Optik für die wenigen, die es sowieso schon
  über Cmd+P versucht hätten.
- **Druck/Export-Button nur in Hosted** (als "Mehrwert"-Feature): verworfen
  — Drucken/PDF-Export ist Basis-Nutzbarkeit, keine Zusatzfunktion. Würde
  gegen die eigene Positionierung aus ADR-0002 verstoßen ("OSS = die echte,
  vollständige Version").
- **Eigener PDF-Generator** (z. B. serverseitig mit Puppeteer statt
  Browser-eigenem Druckdialog): verworfen — deutlich mehr Komplexität
  (Server/Build-Pipeline, die aktuell in keinem der beiden Repos existiert)
  für etwas, das der Browser-Druckdialog schon kostenlos kann.

## Konsequenzen

### Positiv

- Die Startseiten-Behauptung wird tatsächlich wahr statt nur behauptet.
- Konsistentes Feature über beide Repos — kein Fall, in dem OSS
  "schlechter" wirkt, obwohl der Unterschied nur ein fehlender Button ist.

### Negativ / Trade-offs

- Zwei separate Implementierungen (kein Code-Sharing zwischen den Repos,
  siehe ADR-0001) — beide müssen bei künftigen Layout-Änderungen an der
  Glas-Chrome synchron nachgezogen werden. In `SYNC.md` vermerkt.
  **Entfallen mit [ADR-0008](0008-aufloesung-des-oss-hosted-splits.md):**
  es gibt nur noch ein Repo und eine Implementierung.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-09-29 | Erstellt | Bruno Deanoz |