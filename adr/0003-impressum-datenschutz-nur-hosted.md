# 0003. Echtes Impressum/Datenschutz nur im Hosted-Repo, OSS bekommt eine Vorlage

## Status

**Angenommen, Umsetzung geändert** (2026-09-30). Das Ziel gilt unverändert:
Dieses Repo darf nie die Daten seiner Maintainer ausliefern, und wer es
betreibt, braucht seine eigenen Angaben. Nur der *Ort* für die echten Daten
hat sich geändert — das Hosted-Repo aus ADR-0001 existiert seit
[ADR-0008](0008-aufloesung-des-oss-hosted-splits.md) nicht mehr.

Stattdessen kommen die Betreiberangaben aus der gitignorierten `.env`
(`OPERATOR_NAME`, `OPERATOR_ADDRESS`, `OPERATOR_EMAIL`, `OPERATOR_HOSTING`,
`OPERATOR_TRACKING`, `OPERATOR_AUTHORITY`, siehe `.env.example`), gelesen von
`OperatorDetails.astro`. Sind sie nicht gesetzt, zeigen beide Seiten
Platzhalter plus einen sichtbaren „noch nicht konfiguriert"-Hinweis
(`TemplateNotice.astro`); sind sie gesetzt, verschwindet der Hinweis und die
Seiten sind vollwertig. Echte Umgebungsvariablen gewinnen gegen die Datei,
damit eine Deployment-Plattform die Werte setzen kann, ohne dass eine `.env`
auf dem Server liegt.

Damit erreicht ein einzelnes Repo, was ursprünglich der Grund für zwei war:
öffentliche Vorlage und private Echtdaten aus derselben Quelle, ohne dass die
Echtdaten je in git landen.

## Datum

2026-09-29

## Kontext

Beim Port der UI vom OSS-Repo ins Hosted-Repo (siehe Commit
"Add MDX generator script, port full sidebar/UI, generate complete
catalog") fiel auf: `impressum.md` und `datenschutz.md` im OSS-Repo
enthielten Bruno Deanoz' echten Namen, seine c/o-Anschrift und E-Mail. Das
OSS-Repo ist aber laut `PLAN.md` explizit "fully self-hostable — jede:r
kann klonen, selbst hosten und produktiv damit arbeiten" (siehe auch
ADR-0002). Jede:r Self-Hoster:in hätte also unwissentlich Bruno Deanoz'
private Angaben auf der eigenen, komplett anderen Website ausgeliefert —
ein Datenschutz-Leck für den Maintainer und rechtlich falsch für den
Self-Hoster (Impressumspflicht nach § 5 DDG verlangt Angaben zum
*tatsächlichen* Betreiber der jeweiligen Website, nicht zum
Projekt-Maintainer). Geprüft: das OSS-Repo hat aktuell auch keinen eigenen
CI-Deploy-Schritt (`.github/workflows/`), betreibt also selbst keine Live-
Instanz, die ein eigenes Impressum bräuchte.

## Entscheidung

- **Hosted-Repo** bekommt die echten Rechtstexte (Name, Anschrift,
  E-Mail, Hosting-Standort) — das ist die tatsächliche Live-Deployment,
  die Bruno Deanoz selbst betreibt bzw. betreiben wird.
- **OSS-Repo** behält `impressum.md`/`datenschutz.md`, aber als
  ausdrücklich gekennzeichnete Vorlage mit Platzhaltern (`[Name]`,
  `[Anschrift]` etc.) und einem Hinweis-Absatz, der kurz erklärt, warum
  ein Self-Hoster ein eigenes Impressum braucht. Nicht ersatzlos
  gestrichen — sonst merkt eine self-hostende Person gar nicht, dass sie
  selbst rechtlich verpflichtet ist, eins zu haben.
- **`LICENSE` und `CODE_OF_CONDUCT.md` bleiben unverändert** mit Bruno
  Deanoz' echtem Namen im OSS-Repo — das sind Projekt-Identitäts-Dokumente
  (Urheber/Maintainer-Kontakt für das Projekt selbst), keine
  Website-Betreiber-Angaben für eine konkrete Deployment-Instanz. Andere
  Kategorie, andere Regel.

## Alternativen

- **Beide Repos bekommen die echten Daten:** verworfen — genau das
  Problem, das diese Entscheidung löst.
- **OSS-Repo streicht die Seiten ersatzlos:** verworfen — würde
  Self-Hoster:innen im Unklaren lassen, dass sie selbst ein Impressum
  brauchen, sobald sie öffentlich (geschäftsmäßig) live gehen.
- **OSS-Repo bekommt eine rein rechtliche Erklärung ohne Platzhalter-
  Struktur** (z. B. nur ein Absatz Fließtext): verworfen — eine Vorlage
  mit klar markierten Platzhaltern in derselben Struktur wie das echte
  Dokument ist für Self-Hoster:innen leichter zu befüllen als ein Text,
  den sie komplett neu schreiben müssten.

## Konsequenzen

### Positiv

- Kein Datenschutz-Leck für den Maintainer über Forks/Self-Hosting-Klone.
- Self-Hoster:innen werden aktiv auf die eigene Impressumspflicht
  hingewiesen, statt sie zu übersehen.
- Löst nebenbei eine damals offene Lücke: `Footer.astro` verlinkt auf
  tatsächlich existierende Seiten.

### Negativ / Trade-offs

- Zwei leicht unterschiedliche Versionen dieser Seiten zu pflegen (echte
  Daten vs. Vorlage) — bei inhaltlichen Änderungen (z. B. neue DSGVO-
  Pflichtangabe) müssen beide aktualisiert werden.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-09-29 | Erstellt | Bruno Deanoz |
| 2026-09-29 | Hosted-Repo aufgelöst (ADR-0008); Entscheidung gilt weiter, echte Daten jetzt in der Deployment-Konfiguration statt im Hosted-Repo | Bruno Deanoz |
| 2026-09-30 | Umsetzung auf .env-Variablen umgestellt (Hosted-Repo aufgelöst) | Bruno Deanoz |