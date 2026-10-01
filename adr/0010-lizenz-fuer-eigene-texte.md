# 0010. Eigene Texte unter CC BY, nicht unter MIT

## Status

Angenommen — korrigiert einen Punkt aus [ADR-0008](0008-aufloesung-des-oss-hosted-splits.md)

## Datum

2026-10-01

## Kontext

README.md und ueber.mdx nennen bisher zwei Lizenzkategorien: Code (MIT) und
importierter Katalog-Inhalt (CC BY-SA, vom BSI vorgegeben). Beim
Überarbeiten des READMEs fiel auf, dass eine dritte Kategorie unter keiner
von beiden steht: die eigenen Texte dieses Projekts — das Befunde-Register
(ADR-0009), allen voran Analysen wie der GC.5.1.1-Fund, sowie die ADRs
selbst. Ohne explizite Lizenz gilt dafür rechtlich „alle Rechte
vorbehalten" — ein Widerspruch zum sonst durchgehend offenen Charakter des
Repos, der schlicht niemandem aufgefallen war.

ADR-0008 hat die naheliegende Lösung bereits geprüft und verworfen: unter
„Alternativen" steht dort „Dual-Lizenz (Code MIT, Annotationen/Kritik CC BY
unter eigenem Namen)", mit der Begründung, eine Doppellizenz signalisiere
„mehr Schutzbedürfnis, als sie tatsächlich schützt". Diese Begründung
beantwortet aber eine andere Frage, als hier vorliegt: ADR-0008 hat
geprüft, ob eine Lizenztrennung nötig ist, um Code und Kritik
*voneinander abzugrenzen* (im Kontext des damals noch bestehenden
Hosted-Splits). Hier geht es nicht um Abgrenzung oder Schutz, sondern
schlicht darum, welche Lizenz zur Werkform passt — Software-Lizenz für
Software, Inhalts-Lizenz für Text.

## Entscheidung

Eigene Texte (Befunde-Register, ADRs) stehen unter **CC BY 4.0**, nicht
unter MIT. Code bleibt MIT. Importierter Katalog-Inhalt bleibt CC BY-SA.
Drei Lizenzen für drei tatsächlich unterschiedliche Inhaltskategorien im
Repo: eigener Code, eigener Text, fremder (lizenzierter) Text.

## Alternativen

- **MIT auch für eigene Texte**, um bei zwei Lizenzen statt dreien zu
  bleiben: verworfen. MIT ist für Software formuliert — Begriffe wie
  „sublicense" oder der Gewährleistungsausschluss für „the Software"
  passen nicht auf Fließtext. Dass sich Text über die „and associated
  documentation files"-Klausel notdürftig hineinlesen lässt, ist ein
  Workaround, kein sauberer Fit für einen Text mit eigener analytischer
  Aussage wie einem Befund.
- **Status quo belassen** (keine Lizenz für Befunde/ADRs): verworfen —
  bedeutet rechtlich „alle Rechte vorbehalten" und widerspricht dem Rest
  des Repos.
- **CC BY-SA statt CC BY**, konsistent zur Lizenz des Katalog-Inhalts:
  verworfen. Share-Alike ergibt beim BSI-Katalog Sinn, weil das BSI selbst
  so lizenziert hat und Kompatibilität mit der Quelle erhalten bleiben
  muss. Eigene Texte haben keine Quelle, zu der sie kompatibel bleiben
  müssten — Share-Alike würde nur Weiterverwendung erschweren, ohne dass
  ein Zweck dem gegenübersteht.

## Konsequenzen

### Positiv

- Jede Inhaltskategorie im Repo hat eine Lizenz, die zu ihrer Werkform
  passt, statt eine zu überdehnen.
- Schließt eine Lücke, die seit dem Befunde-Register (ADR-0009) bestand,
  ohne dass sie vorher irgendwo benannt war.

### Negativ / Trade-offs

- Dritte Lizenz im Repo statt „eine Lizenz für alles außer BSI-Content".
  Gerechtfertigt, weil die zusätzliche Kategorie (eigener Text) real
  existiert und nicht — anders als die in ADR-0008 verworfene Variante —
  einer Abgrenzung dient, die keinen erkennbaren Zweck hatte.
- README.md und ueber.mdx müssen beide um die dritte Kategorie ergänzt
  werden.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-10-01 | Erstellt | Bruno Deanoz |
