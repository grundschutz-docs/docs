# 0001. Separates privates Repo statt Ordner im OSS-Repo

## Status

**Überholt durch [ADR-0008](0008-aufloesung-des-oss-hosted-splits.md)**
(2026-09-29) — das zweite Repo wurde nach einem Tag wieder aufgelöst. Die
hier dokumentierte GitLab-CE/EE-Recherche und die Begründung gegen einen
`special/`-Ordner bleiben inhaltlich gültig; nur die Prämisse, dass es
überhaupt eine getrennte Hosted-Version geben soll, ist entfallen.

## Datum

2026-09-29

## Kontext

Grundschutz-Docs (OSS-Repo `grundschutz-docs/docs`) generiert Katalogseiten
aus `Grundschutz++-resolved_catalog.json` als reines `.md`. Metadaten wie
`sec_level`/`effort_level` (Stufe/Aufwand) und perspektivisch
MUSS/SOLLTE/KANN werden dort nur als Fettschrift-Text dargestellt, nicht als
echte UI (Badges, Tooltips). Für die geplante Hosted-Version soll das
sauber und interaktiv dargestellt werden ("jeder ISB/Compliance Officer
sieht sofort: das ist nötig"), was echte Astro/UI-Komponenten braucht —
also `.mdx` statt `.md`.

Der Zwei-Stufen-Plan für dieses Projekt (siehe `PLAN.md` im OSS-Repo) sieht
vor: OSS-Version frei nutzbar und selbst hostbar, Hosted-Version frei
nutzbar aber mit closed-source Zusatzschicht. Es musste entschieden werden,
wie diese Zusatzschicht technisch vom OSS-Repo getrennt wird.

## Entscheidung

Wir legen für die Hosted-Version ein zweites, privates GitHub-Repo an
(`grundschutz-docs/hosted`, lokal `Grundschutz-Docs-Hosted/`), das
unabhängig vom OSS-Repo aus derselben Upstream-Quelle
(`Grundschutz++-resolved_catalog.json`) generiert und `.mdx` mit echten
Badge-/Tooltip-Komponenten produziert. Dieses Repo darf ausschließlich neue
Dateien hinzufügen und niemals Dateien des OSS-Repos verändern.

## Alternativen

- **Ordner/Unterverzeichnis im bestehenden OSS-Repo** (z. B. `hosted/`):
  verworfen — technisch unmöglich, closed source zu bleiben, sobald der
  Ordner in einem öffentlichen Repo committet wird. GitHub kennt keine
  privaten Unterordner in einem public Repo.
- **GitLab-CE/EE-Stil**: zwei Repos, wobei die Enterprise-Seite Dateien der
  Community-Seite direkt verändert/erweitert: verworfen — GitLab selbst
  hatte damit jahrelang Merge-Konflikte, bevor sie zu einem Repo mit
  separatem `/ee`-Ordner (andere Lizenz, aber weiterhin öffentlich)
  zurückgewechselt sind. Passt ohnehin nicht, da unser Fall echten
  closed-source Code erfordert, nicht nur eine andere Lizenz auf sichtbarem
  Code.
- **Alles im OSS-Repo lassen, keine Hosted-Zusatzschicht**: verworfen —
  die gewünschte Badge-/Tooltip-UI braucht MDX/Komponenten, die den
  OSS-Zielen (einfach, `.md`, jederzeit selbst hostbar) widersprechen
  würden, wenn man sie dort einbaut.
- **Zugangsbeschränkung/Paywall für die Hosted-Version**: verworfen —
  widerspricht der expliziten Anforderung "frei nutzbar, nur Quellcode
  bleibt geschlossen" aus `PLAN.md`.

## Konsequenzen

### Positiv

- OSS-Repo bleibt minimal, portabel, ohne UI-Framework-Ballast.
- Hosted-Repo kann frei mit Astro-Komponenten, MDX, Tooltips etc.
  experimentieren, ohne das OSS-Repo zu gefährden.
- Vermeidet GitLabs bekannten Merge-Schmerz strukturell von Anfang an.
- Erfüllt die Transparenz-Verpflichtung sauber: eine README-Zeile im
  OSS-Repo reicht, um auf den Unterschied hinzuweisen.

### Negativ / Trade-offs

- Zwei Generator-Skripte (OSS: `.md`, Hosted: `.mdx`), die beide bei
  Änderungen am Katalog-Schema synchron gehalten werden müssen.
- Hosted-Repo hat aktuell noch kein Deploy-Ziel (Domain/Hosting ungeklärt)
  — bleibt vorerst unverbunden liegen.
- Geteilte, nicht-geheime Assets (z. B. Rechtstexte, Sidebar-Struktur)
  müssen dupliziert statt geteilt werden, um die "nur hinzufügen"-Regel
  einzuhalten.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-09-29 | Erstellt | Bruno Deanoz |
| 2026-09-29 | Überholt durch ADR-0008 | Bruno Deanoz |