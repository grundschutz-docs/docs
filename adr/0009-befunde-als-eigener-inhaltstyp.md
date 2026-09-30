# 0009. Befunde als eigener Inhaltstyp, eine Datei je Fund

## Status

Vorgeschlagen

## Datum

2026-10-01

## Kontext

Im Projekt entstehen beim Lesen des Katalogs und der Mapping-Dateien
regelmäßig Funde: Widersprüche im Anforderungstext, fehlende Querverweise,
offensichtlich falsche Zuordnungen in der offiziellen Mapping-Datei,
Reibungen zwischen BSI-Systematik und anderem Recht. Sechs solcher Funde
liegen aktuell in einer privaten Notizdatei außerhalb des Repos
(`OPS.1.1.5_Kritikpunkte.md`).

Diese Funde sind das, was die Seite von Wettbewerbern unterscheidet. Die
Katalogaufbereitung selbst kann jeder nachbauen, der OSCAL parsen kann — das
BSI veröffentlicht die Daten offen. Die Funde kann nur nachbauen, wer
Grundschutz-Systematik, DSGVO, WP248 und BSIG gleichzeitig im Kopf hat. Die
Wettbewerbsrecherche zu ADR-0007 fand drei Anbieter, die Kataloge
aufbereiten, und keinen, der ein Fundregister führt.

Drei Eigenschaften der vorhandenen Funde bestimmen das Format:

**Die Status laufen auseinander.** Ein Fund (fehlender Querverweis von A4 auf
OPS.1.2.6) ist klein, unstrittig und sofort meldereif. Ein anderer (Mapping
`OPS.1.1.5.A10-UA.1` → `DET.3.4`) soll erst nach der it-sa (27.–29.10.2026)
gegen den finalisierten Stand geprüft werden. Zwei weitere sind
Governance-Beobachtungen, die nie den Status "behoben" erreichen werden. In
einer gemeinsamen Datei kollidieren diese Lebenszyklen bereits jetzt.

**Die Belastbarkeit ist verschieden.** Der Mapping-Fehler ist an öffentlichen
Daten nachprüfbar: `DET.3.4` behandelt ausschließlich Speicherkapazität,
`A10-UA.1` hat genau diese eine Zuordnung, und der passende Zielkandidat
`DET.3.5` (Revisionssicherheit) nennt im Erläuterungstext wörtlich das Thema
Administrierenden-Zugriff — und hat auffällig keinen einzigen
OPS.1.1.5-Vorgänger. Das ist ein Defekt. Die Feststellung dagegen, dass die
BSI-Schutzbedarfskategorie und die Risikobewertung nach Art. 32 DSGVO
unabhängige Achsen sind, ist eine Auslegung. Beides gleich zu präsentieren
würde die Auslegung überhöhen und den Defekt entwerten.

**Funde verweisen auf Anforderungen, nicht auf Bausteine.** Ein Fund betrifft
typischerweise mehrere Controls quer über Praktiken hinweg — der
Mapping-Fehler oben berührt `DET.3.4`, `DET.3.5` und die alte
`OPS.1.1.5.A10`.

Hinzu kommt ein Zeitfenster: Die Pilotphase lief bis 30.9.2026, die
öffentliche Vorstellung auf der it-sa steht im Oktober 2026 an. Funde aus der
Pilotphase sind genau das, wofür eine Pilotphase da ist — nach ihrem Ende
verschiebt sich die Rolle vom Mitwirkenden zum Kommentator.

## Entscheidung

Wir führen **Befunde** als eigenen Inhaltstyp unter `/befunde/`, mit **einer
Datei je Fund**.

Jeder Befund trägt im Frontmatter:

```yaml
typ: fakt | auslegung | beobachtung
status: entwurf | offen | gemeldet | beantwortet | behoben | hinfaellig
gefunden: YYYY-MM-DD
betrifft: [DET.3.4, DET.3.5, OPS.1.1.5.A10]
quelle: <Datei, Dokument oder URL, an der der Fund nachprüfbar ist>
meldung:                # nur ab status: gemeldet
  kanal: <GitHub-Issue | E-Mail service-center@bsi.bund.de | …>
  datum: YYYY-MM-DD
  link: <URL, falls öffentlich>
```

Der Körper folgt der Struktur **Befund / Warum wichtig / Vorschlag**.

`typ` ist die wichtigste Angabe und wird sichtbar ausgewiesen, nicht nur
gespeichert:

- **fakt** — an öffentlich zugänglichen Daten nachprüfbar. Wer will, kann es
  gegenlesen.
- **auslegung** — folgt aus mehreren Regelwerken, ist aber eine Einschätzung.
  Keine Rechtsberatung, und als solche erkennbar.
- **beobachtung** — Widerspruch oder Lücke, aber kein Fehler im engeren Sinn.

Wo eine Meldung vorgesehen ist, gilt: **erst melden, dann veröffentlichen.**
Ein Eintrag mit `status: gemeldet` und Datum ist Pilotphasen-Feedback.
Derselbe Text ohne Meldung ist ein Beitrag darüber, dass das BSI einen Fehler
gemacht hat. Gleicher Inhalt, andere Rolle.

Der Rückverweis von der Katalogseite auf zugehörige Befunde wird **jetzt noch
nicht gebaut** (siehe Konsequenzen).

## Alternativen

**Eine Datei je Baustein**, wie die bisherige Notizdatei. Verworfen: Die
Status divergieren schon bei sechs Funden, und ein Fund betrifft in der Regel
mehrere Anforderungen aus verschiedenen Praktiken. Der Baustein ist die
Fundstelle, nicht die Einheit.

**Blog- oder News-Format.** Verworfen: Ein Befund ist keine Nachricht. Er hat
einen Zustand, der sich ändert, und muss nach einer Katalogänderung
nachgeprüft und aktualisiert werden. Ein Beitrag mit Datum lädt dazu ein, ihn
stehenzulassen.

**Anmerkungen direkt in den Katalogseiten.** Verworfen: Die Seiten unter
`src/content/docs/grundschutzpp/` werden von `scripts/generate_docs.py`
erzeugt und bei jedem Lauf überschrieben. Handgeschriebener Inhalt dort wäre
bei der nächsten Katalogaktualisierung weg.

**Keine Typisierung der Aussagen.** Verworfen: Ein nachprüfbarer Defekt und
eine rechtliche Einschätzung im selben Format nebeneinander schadet beiden.
Die Einschätzung wirkt fester, als sie ist, und der Defekt wird zur Meinung.

## Konsequenzen

### Positiv

- Das Unterscheidungsmerkmal des Projekts wird öffentlich, verlinkbar und
  zitierbar, statt in einer lokalen Datei zu liegen.
- Der Statuslauf belegt Mitwirkung statt Kritik. Ein Register, das "gefunden,
  gemeldet am X, behoben am Y" zeigt, weist Kompetenz besser nach als der
  Befund allein.
- Die Typisierung schützt vor dem Vorwurf der Rechtsberatung und macht die
  nachprüfbaren Funde zugleich glaubwürdiger.
- `betrifft` legt den Schlüssel für die spätere Verknüpfung mit den
  Katalogseiten schon jetzt an, ohne dass sie gebaut sein muss.

### Negativ / Trade-offs

- **Wartungslast.** Jeder Befund bezieht sich auf einen Katalogstand. Ändert
  das BSI den Katalog oder die Mapping-Datei, muss jeder Befund neu geprüft
  werden. `status: hinfaellig` fängt das ab, aber jemand muss nachsehen.
- **Positionierung.** Funde zur Governance des BSI (Zugangshürde in
  `CONTRIBUTING.md`, GitHub statt openCode.de) sind inhaltlich fair, stellen
  das Projekt aber sichtbar auf. Das ist eine Entscheidung mit Folgen, keine
  rein redaktionelle.
- **Der Rückverweis fehlt vorerst.** Reizvoll wäre, dass `DET.3.4` im Katalog
  anzeigt, dass es dazu einen Befund gibt. Technisch sauber über `betrifft`
  und eine Collection-Abfrage, aber bei einer Handvoll Befunden lohnt der
  Aufwand nicht. Richtung Befund → Anforderung ist ein gewöhnlicher Link und
  genügt, bis genug Inhalt da ist.
- **Ein Register verpflichtet.** Ein Fundregister, das ein halbes Jahr lang
  keinen neuen Eintrag bekommt, wirkt schlechter als gar keins.

## Offen

- Welche der sechs vorhandenen Funde öffentlich werden (insbesondere die
  beiden Governance-Beobachtungen).
- Ob der Bereich zunächst vollständig auf `status: entwurf` läuft, bis die
  jeweiligen Meldungen raus sind.

## Changelog

| Datum      | Änderung | Von          |
|------------|----------|--------------|
| 2026-10-01 | Erstellt | giordano137  |
