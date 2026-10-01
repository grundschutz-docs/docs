# 0008. Auflösung des OSS/Hosted-Splits — ein Repo, alles MIT

## Status

Angenommen — ersetzt ADR-0001 und ADR-0002

**Ein Punkt korrigiert durch [ADR-0010](0010-lizenz-fuer-eigene-texte.md)**
(2026-10-01): Die unten unter „Alternativen" verworfene Dual-Lizenz
(Code MIT, Text CC BY) wurde aus dem Blickwinkel des Repo-Splits beurteilt,
den diese ADR auflöst — nicht aus dem der Werkform. Für eigene Texte
(Befunde-Register, ADRs) gilt seither CC BY 4.0, nicht MIT. Die
eigentliche Entscheidung dieser ADR (ein Repo, keine Feature-Trennung)
bleibt unverändert.

## Datum

2026-09-29

## Kontext

ADR-0001 hat ein zweites, privates Repo für eine Hosted-Version
eingeführt, ADR-0002 hat deren Verhältnis zum OSS-Repo festgelegt: OSS als
vollwertige Basis, Hosted kostenlos nutzbar, aber nicht self-hostbar.
Beide Entscheidungen sind am selben Tag entstanden, an dem auch die
Hosted-Komponenten gebaut wurden.

Nach einem Tag Betrieb dieses Modells lässt sich der Preis beziffern:

- Zwei Generator-Skripte (645 und 758 Zeilen), von denen **~545 Zeilen
  byte-identisch** waren — 85 % des OSS-Skripts wurden doppelt von Hand
  gepflegt.
- Eine `SYNC.md` von 157 Zeilen, deren einziger Zweck das Buchhalten
  gewollter Divergenz war.
- Eine Sync-Checkliste, die bei **jedem** Upstream-Katalog-Update zweimal
  abgearbeitet werden musste — dauerhaft, nicht einmalig.

Dem stand kein Nutzen gegenüber, der die Kosten trägt:

- **Kein wirtschaftlicher:** die Hosted-Version sollte laut ADR-0002
  ausdrücklich kostenlos bleiben.
- **Kein Kontroll-Nutzen:** die Basis ist MIT-lizenziert, der Code also
  ohnehin frei. Exklusiv blieb nur das Recht, die Badge-Komponenten
  selbst zu hosten — eine Einschränkung ohne erkennbaren Zweck.
- **Kein Schutz-Nutzen:** der Unterschied sollte vor allem in Design und
  Funktionsumfang liegen. Design ist aber genau das, was Closed Source
  nicht schützt — CSS steht im Browser.

Dazu zwei Befunde, die die Entscheidung gekippt haben:

1. **Die Alternative „gar nicht splitten" wurde in ADR-0002 nie geprüft.**
   Abgewogen wurden Paywall, verzögerte Parität, vollständig geschlossen
   und bewusst unvollständiges OSS — alles Varianten von *wie* man
   splittet, keine von *ob*.
2. **Der Split hat bereits Schaden angerichtet.** Auslöser des ersten
   Hosted-Features war die Frage einer echten Nutzerin bzw. eines echten
   Nutzers, was „Aufwand: 0" bedeutet (148 von 1000 Anforderungen, Skala
   nirgends erklärt). Der Hosted-Fix wurde gebaut; der OSS-Fix steht in
   `PLAN.md` als „still TODO, see ROADMAP.md" — und taucht in `ROADMAP.md`
   nie auf. Das Feedback landete in der Version, die niemand benutzen
   kann, und verschwand aus der, die es könnte.

Hinzu kommt der eigentliche Zweck des öffentlichen Repos: Es soll zeigen,
was hier gebaut wurde. Genau die aussagekräftigste Arbeit
(`ControlMeta.astro`, 456 Zeilen; `PdcaCycle.astro`, 188 Zeilen; die
Filter-Komponenten) lag im Repo, das niemand öffnen kann.

## Entscheidung

- **Ein Repo.** `Grundschutz-Docs-Hosted` wird in `grundschutz-docs/docs`
  zusammengeführt und danach nicht weitergeführt.
- **Ein Generator.** Das Hosted-Skript ist eine echte Obermenge des
  OSS-Skripts und ersetzt es vollständig. Alle Katalogseiten werden als
  `.mdx` erzeugt, `@astrojs/mdx` wird Projektabhängigkeit.
- **Alles MIT.** Die bisher hosted-exklusiven Komponenten werden Teil des
  öffentlichen Repos. Es gibt keine Feature-Differenzierung mehr zwischen
  einer offenen und einer gehosteten Variante.
- **Die ADRs wandern mit** ins öffentliche Repo. Sie dokumentieren die
  Überlegungen hinter dem Projekt und gehören damit zu dem, was das Repo
  zeigen soll — auch diese hier, die eine frühere Entscheidung zurücknimmt.
- **Eine gehostete Instanz bleibt geplant** (`grundschutz-docs.de`), aber
  als *Betriebs*-Angebot, nicht als Feature-Stufe: immer aktueller Stand,
  kein Setup nötig. Wer will, hostet dieselbe Version selbst.

## Alternativen

- **Split beibehalten, nur besser dokumentieren:** verworfen — löst die
  laufenden Kosten nicht, und das Dokumentieren war bereits der teure
  Teil (`SYNC.md`).
- **Code-Sharing zwischen zwei Repos** (Submodul, npm-Paket für die
  Komponenten): verworfen — hätte die Duplikation reduziert, aber die
  Grundfrage nicht beantwortet, wozu die Trennung überhaupt dient. Mehr
  Mechanik für dasselbe Ziel.
- **Umgekehrt zusammenführen** (Hosted-Repo wird zum neuen öffentlichen
  Repo, `grundschutz-docs/docs` gelöscht): verworfen — hätte CI-Workflows,
  den täglichen Katalog-Sync, `LICENSE`, `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md` und die gesamte Commit-Historie gekostet, die das
  Hosted-Repo alle nicht hat. Es wäre außerdem die dritte Löschung dieses
  Repos gewesen, diesmal ohne zwingenden Grund.
- **Dual-Lizenz** (Code MIT, Annotationen/Kritik CC BY unter eigenem
  Namen): verworfen — eine Doppellizenz auf einem Projekt dieser Größe
  signalisiert mehr Schutzbedürfnis, als sie tatsächlich schützt.

## Konsequenzen

### Positiv

- ~545 doppelt gepflegte Zeilen und eine komplette Sync-Pflicht entfallen.
- Das öffentliche Repo zeigt die tatsächliche Arbeit statt einer
  reduzierten Variante davon.
- Kein Widerspruch mehr zur eigenen Kritik an BSIs Kommunikation
  („claims openness, delivers less", `OPS.1.1.5_Kritikpunkte.md` Punkt 5).
  Die Transparenz-Verpflichtung aus `HOSTED.md` wird damit gegenstandslos
  und die Datei entfernt — es gibt nichts mehr offenzulegen.
- Die Sync-Checkliste aus `SYNC.md` wandert nach `CONTRIBUTING.md` und
  gilt dort nur noch einmal statt zweimal.

### Negativ / Trade-offs

- Die Entscheidung gibt einen möglichen Differenzierungshebel auf: Es wird
  künftig kein Feature geben, das ausschließlich die gehostete Instanz hat.
  Differenzierung muss über Betrieb und Inhalt entstehen — über die laufende
  Instanz (immer aktueller Stand, kein Setup) und über die Annotations- und
  Kritik-Ebene, die inhaltlich niemand sonst liefert. Beides lässt sich
  ohnehin nicht durch geschlossenen Quellcode absichern; Design schon gar
  nicht, das steht im Browser.
- `.mdx` statt `.md` macht die generierten Seiten etwas
  anfälliger — Katalog-Prosa mit `{`, `}` oder `<` bricht sonst den Build.
  `mdx_safe()` fängt das ab, muss aber bei neuen Katalog-Editionen
  mitgeprüft werden (siehe Checkliste in `CONTRIBUTING.md`).
- ADR-0003 (Impressum/Datenschutz) verliert seinen ursprünglichen
  Adressaten. Die Entscheidung selbst gilt weiter: das Repo liefert
  Vorlagen, echte Betreiberdaten gehören in die Deployment-Konfiguration
  der laufenden Instanz, nicht ins Repo.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-09-29 | Erstellt | Bruno Deanoz |