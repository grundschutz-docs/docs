# 0002. OSS als Basisversion, Hosted als kostenloser Mehrwert ohne Self-Hosting

## Status

Angenommen

## Datum

2026-09-29

## Kontext

Nach der Entscheidung, ein zweites, privates Repo für die Hosted-Version
anzulegen (ADR-0001), musste geklärt werden, wie sich OSS- und
Hosted-Version inhaltlich zueinander verhalten sollen — nicht nur
technisch (getrennte Repos), sondern für Nutzer:innen sichtbar: Was
bekommt man womit, und was nicht? Ohne diese Klärung droht entweder ein
OSS-Repo, das nur als Teaser für die Hosted-Version dient (schlecht für
Vertrauen/Transparenz, siehe `OPS.1.1.5_Kritikpunkte.md` Punkt 5 zu
"claims openness, delivers less"), oder eine Hosted-Version ohne klaren
Mehrwert-Grund.

## Entscheidung

- **OSS-Repo ist die vollwertige Basisversion.** Kein verkrüppelter
  Teaser — jede:r kann es klonen, selbst hosten und produktiv damit
  arbeiten. Das ist der Sinn der MIT-Lizenz.
- **Hosted-Version bietet mehr** (aktuell geplant: echte
  Badge-/Tooltip-Komponenten für Stufe/Aufwand, perspektivisch
  MUSS/SOLLTE/KANN und weitere Features), **bleibt aber kostenlos
  nutzbar** — kein Paywall, keine Zugangsschranke.
- **Der Unterschied ist ausschließlich Self-Hosting:** die Hosted-Version
  läuft nur auf meiner eigenen Domain, ihr Quellcode bleibt geschlossen.
- **Ausnahme-Klausel:** wer ernsthaftes Interesse an Self-Hosting der
  Hosted-Features hat, kann das direkt mit mir persönlich besprechen. Das
  ist eine Einzelfall-Absprache, kein automatisierter/dokumentierter
  Prozess — muss aber öffentlich auffindbar sein, sobald die Hosted-Version
  live geht (siehe TODO in `PLAN.md` des OSS-Repos).

## Alternativen

- **Paywall für die Hosted-Version:** verworfen — widerspricht der
  expliziten Anforderung "frei nutzbar" und würde das Projekt von einem
  nicht-kommerziellen Transparenz-Projekt zu einem Produkt
  verschieben, was nicht das Ziel ist.
- **Feature-Parität mit Verzögerung** (Hosted-Features wandern nach N
  Monaten ins OSS-Repo): verworfen — unnötige Komplexität, kein klarer
  Vorteil gegenüber "Hosted-Features bleiben dauerhaft hosted-only,
  Self-Hosting nur per Absprache".
- **Komplett geschlossen, keine Ausnahme-Klausel:** verworfen — zu starr
  für ein nicht-kommerzielles Projekt ohne Umsatzdruck; eine
  persönliche Absprache-Option kostet nichts und hält die Tür offen, ohne
  einen formalen Support-/SLA-Prozess aufbauen zu müssen.
- **OSS-Repo bewusst unvollständig lassen, um Hosted attraktiver zu
  machen:** verworfen — genau das Muster, das die eigene Kritik an BSIs
  Kommunikation (`OPS.1.1.5_Kritikpunkte.md`) anprangert; würde die
  Glaubwürdigkeit des ganzen Projekts untergraben.

## Konsequenzen

### Positiv

- Klare, für Außenstehende sofort verständliche Regel: "self-hostbar vs.
  nicht self-hostbar", keine verschwommene Feature-Matrix nötig.
- OSS-Repo bleibt aus eigenem Recht nützlich — Vertrauen wird nicht durch
  künstliche Beschränkung erkauft.
- Ausnahme-Klausel hält das Projekt offen für Einzelfälle, ohne einen
  Prozess pflegen zu müssen, für den es keinen Bedarf gibt.

### Negativ / Trade-offs

- Die Ausnahme-Klausel ist informell — skaliert nicht, wenn mehrfach
  gleichzeitig angefragt wird (aktuell kein Problem, da noch niemand
  überhaupt von der Hosted-Version weiß).
- Muss aktiv gepflegt/kommuniziert werden (README/CONTRIBUTING), sonst
  verpufft sie ungenutzt — siehe offenes TODO in `PLAN.md`.

## Changelog

| Datum      | Änderung | Von     |
|------------|----------|---------|
| 2026-09-29 | Erstellt | bruno   |
