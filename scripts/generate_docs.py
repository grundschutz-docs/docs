#!/usr/bin/env python3
"""
Liest den Grundschutz++-resolved_catalog.json (OSCAL) und generiert daraus
lesbare Markdown-Seiten fuer Starlight.

Erneut ausfuehren nach jedem `git pull` im Grundschutz-PlusPlus-Repo, um die
Doku-Seite auf den aktuellen Stand zu bringen:

    cd Grundschutz-PlusPlus && git pull
    python3 ../Grundschutz-Docs/scripts/generate_docs.py
    cd ../Grundschutz-Docs && pnpm run build   # oder: pnpm run dev
"""
import json
import os
import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CATALOG_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "control_layer" / "Grundschutz++" / "Grundschutz++-resolved_catalog.json"
)
# Lokal: Grundschutz-PlusPlus liegt als Ordner neben diesem Repo. In CI gibt es
# diesen Nachbarordner nicht — dort wird der Pfad stattdessen über die Umgebungsvariable
# gesetzt (siehe .github/workflows/sync-catalog.yml).
CATALOG_FILE = Path(os.environ["GRUNDSCHUTZPP_CATALOG"]) if os.environ.get("GRUNDSCHUTZPP_CATALOG") else DEFAULT_CATALOG_FILE
DEFAULT_MAPPING_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "control_layer" / "Mappings" / "IT-GS2023-zu-GSpp" / "ITGS-to-GS++-mapping_collection.json"
)
MAPPING_FILE = Path(os.environ["GRUNDSCHUTZPP_MAPPING"]) if os.environ.get("GRUNDSCHUTZPP_MAPPING") else DEFAULT_MAPPING_FILE
# Grundschutz-Projekt/bsi-kompendium-2023-bausteine.json: eigene, einmal von
# BSIs Bausteine-Uebersichtsseite gescrapte Lookup-Tabelle (Baustein-ID -> PDF-URL),
# siehe adr/0005-vorgaenger-anforderung-alt-neu.md im Hosted-Repo. Liegt bewusst
# eine Ebene ueber beiden Repos (wie SYNC.md) -- externe Referenzdaten, nicht
# Eigentum eines der beiden Repos.
DEFAULT_BAUSTEINE_LINKS_FILE = REPO_ROOT / "bsi-kompendium-2023-bausteine.json"
BAUSTEINE_LINKS_FILE = (
    Path(os.environ["BSI_BAUSTEINE_LINKS"]) if os.environ.get("BSI_BAUSTEINE_LINKS") else DEFAULT_BAUSTEINE_LINKS_FILE
)
OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "grundschutzpp"
# Rollen-Seiten (ADR-0007 im Hosted-Repo, hier ohne eigenes ADR uebernommen --
# Inhalt/Struktur ist geteilt, nur der Toggle/das Kreisdiagramm bleiben
# Hosted-exklusiv, siehe SYNC.md).
ROLLEN_OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "rollen"
ASTRO_CONFIG = Path(__file__).resolve().parent.parent / "astro.config.mjs"

PARAM_RE = re.compile(r"\{\{\s*insert:\s*param,\s*([a-zA-Z0-9._-]+)\s*\}\}")

# Zeitplan laut BSI-Fahrplan (Pilotphase, it-sa-Termin) und Fachpublikationen
# (Übergangsfrist/Ablösung — vom BSI noch nicht mit einem fixen Datum bestätigt,
# daher als "geplant" ausgewiesen). Quellen siehe Commit-Historie/Konversation.
TIMELINE = [
    (date(2026, 4, 1), date(2026, 9, 30), "Pilotphase", "Grundschutz++ wird mit Pilotpartnern erprobt."),
    (date(2026, 10, 27), date(2026, 10, 29), "Vorstellung auf der it-sa", "Methodik und Kompendium werden öffentlich vorgestellt."),
    (date(2026, 4, 1), date(2029, 12, 31), "Übergangsphase", "Das bisherige IT-Grundschutz-Kompendium bleibt parallel gültig."),
    (date(2027, 1, 1), None, "Zertifizierung möglich (geplant)", "Eine Zertifizierung nach Grundschutz++ soll ab 2027 möglich sein."),
    (date(2029, 1, 1), None, "Vollständige Ablösung (geplant, Datum offen)", "Das bisherige Kompendium soll danach vollständig abgelöst werden."),
]

# Der Katalog selbst benennt diese sechs Praktiken als PDCA-Managementzyklus
# (z. B. VRB: "schließt den PDCA-Zyklus ab", PERF: "Check-Phase im
# PDCA-Zyklus") — keine eigene Erfindung, sondern in den Gruppentexten
# explizit so beschrieben. Alle anderen Gruppen sind operative Themenfelder.
MANAGEMENT_CYCLE_IDS = {"GC", "STM", "UMS", "VRB", "PERF", "RISK"}


def prop(node, name):
    for p in node.get("props", []):
        if p.get("name") == name:
            return p
    return None


def prop_value(node, name):
    p = prop(node, name)
    return p.get("value") if p else None


def group_description(group):
    label_prop = prop(group, "label")
    if label_prop:
        return label_prop.get("remarks")
    return None


def substitute_params(text, params_by_id):
    if not text:
        return text

    def repl(m):
        pid = m.group(1)
        label = params_by_id.get(pid, pid)
        return f"*[{label}]*"

    return PARAM_RE.sub(repl, text)


def part_text(control, name):
    for part in control.get("parts", []):
        if part.get("name") == name:
            return part.get("prose", "")
    return None


def part_prop_value(control, part_name, prop_name):
    for part in control.get("parts", []):
        if part.get("name") == part_name:
            for p in part.get("props", []):
                if p.get("name") == prop_name:
                    return p.get("value")
    return None


def build_predecessor_index(mapping_data):
    index = {}
    for group in mapping_data["mapping-collection"]["mappings"]:
        for m in group.get("maps", []):
            rel = m.get("relationship")
            sources = m.get("sources", [])
            targets = m.get("targets", [])
            if not sources or not targets or not rel:
                continue
            old_id = sources[0].get("id-ref")
            new_id = targets[0].get("id-ref")
            if not old_id or not new_id:
                continue
            index.setdefault(new_id, []).append((old_id, rel))
    return index


def baustein_id_from_itgs_id(itgs_id):
    # "OPS.1.1.5.A3-UA.1" -> "OPS.1.1.5" (Baustein-Teil vor der ersten Anforderungsnummer)
    m = re.match(r"^([A-Z]+(?:\.[0-9]+)+)\.A", itgs_id)
    return m.group(1) if m else None


# OSCAL-Beziehungstypen aus der Mapping-Datei sind englisches
# Standard-Vokabular (internationales Format) -- auf einer sonst
# durchgehend deutschen Seite übersetzt anzeigen. Interner Wert (für
# Sortierung o. ä.) bleibt englisch, nur die Anzeige wird übersetzt.
# Richtung nach der offiziellen OSCAL-Mapping-Spezifikation (NIST, $schema
# in der Mapping-Datei): "source [relationship] target" -- hier ist die
# Quelle immer die alte, das Ziel die neue Anforderung. subset-of: die
# alte ist Teilbereich der neuen (neue deckt mehr ab). superset-of: die
# alte deckte mehr ab als die neue (neue ist enger gefasst).
RELATIONSHIP_LABELS = {
    "equivalent-to": "entspricht",
    "subset-of": "Teilbereich von",
    "superset-of": "umfasst",
    "intersects-with": "überschneidet sich mit",
}


def relationship_label(rel):
    return RELATIONSHIP_LABELS.get(rel, rel)


def predecessor_line(control_id, predecessor_index, baustein_links):
    entries = predecessor_index.get(control_id)
    if not entries:
        return None
    parts = []
    for old_id, rel in entries:
        baustein_id = baustein_id_from_itgs_id(old_id)
        link = baustein_links.get(baustein_id) if baustein_id else None
        label = f"[{old_id}]({link})" if link else old_id
        parts.append(f"{label} ({relationship_label(rel)})")
    return "**Vorgänger:** " + " · ".join(parts) + "\n"


def render_control(control, level, params_by_id, predecessor_index, baustein_links):
    heading = "#" * min(level, 6)
    lines = [f"{heading} {control['id']} – {control['title']}\n"]

    modal_verb = part_prop_value(control, "statement", "modal_verb")
    sec_level = prop_value(control, "sec_level")
    effort = prop_value(control, "effort_level")
    threats = prop_value(control, "threats")
    badges = []
    if modal_verb:
        badges.append(f"**Pflicht:** {modal_verb}")
    if sec_level:
        badges.append(f"**Stufe:** `{sec_level}`")
    if effort:
        badges.append(f"**Aufwand:** {effort}")
    if threats:
        badges.append(f"**Gefährdungen:** {threats}")
    if badges:
        lines.append(" · ".join(badges) + "\n")

    predecessors = predecessor_line(control["id"], predecessor_index, baustein_links)
    if predecessors:
        lines.append(predecessors)

    statement = substitute_params(part_text(control, "statement"), params_by_id)
    if statement:
        lines.append(f"> {statement}\n")

    guidance = substitute_params(part_text(control, "guidance"), params_by_id)
    if guidance:
        lines.append(f"{guidance}\n")

    for sub in control.get("controls", []):
        lines.append(render_control(sub, level + 1, params_by_id, predecessor_index, baustein_links))

    return "\n".join(lines)


def render_group(group, level, params_by_id, predecessor_index, baustein_links, include_heading=True):
    lines = []
    if include_heading:
        heading = "#" * min(level, 6)
        lines.append(f"{heading} {group['id']} {group['title']}\n")

    desc = group_description(group)
    if desc:
        lines.append(f"{desc}\n")

    for control in group.get("controls", []):
        lines.append(render_control(control, level + 1, params_by_id, predecessor_index, baustein_links))

    for sub in group.get("groups", []):
        lines.append(render_group(sub, level + 1, params_by_id, predecessor_index, baustein_links))

    return "\n".join(lines)


def build_params_index(catalog):
    index = {}
    def walk(node):
        for p in node.get("params", []):
            index[p["id"]] = p.get("label", p["id"])
        for c in node.get("controls", []):
            walk(c)
        for g in node.get("groups", []):
            walk(g)
    for g in catalog["groups"]:
        walk(g)
    return index


def yaml_quote(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def first_sentence(text):
    if not text:
        return ""
    match = re.search(r"(.+?[.!?])(\s|$)", text)
    return match.group(1) if match else text


def format_range(start, end):
    if end is None:
        return f"ab {start.strftime('%m/%Y')}"
    if start.year == end.year and start.month == end.month:
        return f"{start.day}.–{end.day}.{start.strftime('%m.%Y')}"
    return f"{start.strftime('%m/%Y')} – {end.strftime('%m/%Y')}"


def render_timeline():
    today = date.today()
    lines = ['<ul class="status-timeline">']
    for start, end, label, detail in TIMELINE:
        is_current = start <= today and (end is None or today <= end)
        status = ' data-current="true"' if is_current else ""
        badge = '<span class="status-badge">läuft</span>' if is_current else ""
        lines.append(
            f'<li{status}><span class="status-range">{format_range(start, end)}</span>'
            f"<strong>{label}</strong>{badge}<p>{detail}</p></li>"
        )
    lines.append("</ul>\n")
    return "\n".join(lines)


def collect_leaf_controls(node):
    """Alle Anforderungen ohne eigene Unter-Anforderungen unter einem Control-
    oder Gruppen-Knoten, rekursiv. Funktioniert fuer beide Knotentypen, weil
    beide optionale "controls"/"groups"-Listen haben (OSCAL-Struktur)."""
    for c in node.get("controls", []):
        if c.get("controls"):
            yield from collect_leaf_controls(c)
        else:
            yield c
    for g in node.get("groups", []):
        yield from collect_leaf_controls(g)


def is_muss(control):
    return part_prop_value(control, "statement", "modal_verb") == "MUSS"


# Quelle: Grundschutz-PlusPlus/documentation/namespaces/security_level.csv --
# nur diese zwei Werte existieren im Katalog (kein Basis/Standard/Kern wie im
# alten Kompendium).
SEC_LEVEL_LABELS = {"normal-SdT": "Standard-Sicherheitsstufe", "erhöht": "Erhöhte Sicherheitsstufe"}


def render_muss_table_md(group_id, group_title, slug, muss_controls):
    lines = [f"### {group_id} {group_title}\n\n"]
    lines.append("| Anforderung | Stufe |\n|---|---|\n")
    for control in muss_controls:
        sec_level = prop_value(control, "sec_level") or ""
        sec_label = SEC_LEVEL_LABELS.get(sec_level, sec_level)
        lines.append(f"| [{control['id']} – {control['title']}](/grundschutzpp/{slug}/) | {sec_label} |\n")
    lines.append("\n")
    return "".join(lines)


def render_geschaeftsfuehrung_page(management, themenfelder, groups_by_id):
    all_groups = management + themenfelder
    total = 0
    total_muss = 0
    sections = []
    for gid, title, slug, _ in all_groups:
        leaves = list(collect_leaf_controls(groups_by_id[gid]))
        muss = [c for c in leaves if is_muss(c)]
        total += len(leaves)
        total_muss += len(muss)
        if muss:
            sections.append(render_muss_table_md(gid, title, slug, muss))

    lines = [
        "---\n",
        f"title: {yaml_quote('Für Geschäftsführung')}\n",
        f"description: {yaml_quote('Pflicht-Anforderungen, Einstufungskriterien und Haftungsrahmen auf einen Blick.')}\n",
        "---\n\n",
        "> Diese Seite ersetzt keine Rechts- oder Haftungsberatung. Sie ordnet "
        "öffentliche Quellen ein (den BSI-Katalog und geltendes Gesetzesrecht) "
        "— eine Bewertung des Einzelfalls kann nur eine Rechtsanwältin, ein "
        "Rechtsanwalt oder eine Wirtschaftsprüfung vornehmen.\n\n",
        f"## Auf einen Blick\n\n"
        f"**{total_muss} von {total} Anforderungen im gesamten Katalog sind "
        f"MUSS** — uneingeschränkt zu erfüllen, unabhängig vom individuellen "
        f"Risikoappetit (RFC2119 / DIN 820-2:2022, Anhang H). Das ist die "
        f"Teilmenge, die aus Governance-Sicht zuerst zählt.\n\n",
        "## Bin ich überhaupt betroffen?\n\n"
        "Das BSI-Gesetz (BSIG, Fassung seit 2.12.2025) unterscheidet zwei "
        "Kategorien nach § 28 BSIG:\n\n"
        "- **Besonders wichtige Einrichtung**: unabhängig von der Größe, wenn "
        "du Betreiber:in einer kritischen Anlage (KRITIS), qualifizierter "
        "Vertrauensdiensteanbieter, Top-Level-Domain-Registry oder "
        "DNS-Diensteanbieter bist. Sonst: mind. 250 Mitarbeitende **oder** "
        "über 50 Mio. € Jahresumsatz **und** über 43 Mio. € Jahresbilanzsumme, "
        "in einem Sektor nach Anlage 1 BSIG.\n"
        "- **Wichtige Einrichtung**: mind. 50 Mitarbeitende **oder** über "
        "10 Mio. € Jahresumsatz **und** über 10 Mio. € Jahresbilanzsumme, in "
        "einem Sektor nach Anlage 1 oder 2 BSIG.\n\n"
        "Kleinere Einrichtungen außerhalb kritischer Sektoren fallen in der "
        "Regel nicht darunter. Diese Kriterien ersetzen keine "
        "Schutzbedarfsfeststellung — sie helfen nur bei der ersten "
        "Einordnung mit euren eigenen Zahlen.\n\n"
        "*Primärquelle: [§ 28 BSIG](https://www.gesetze-im-internet.de/bsig_2025/BJNR12D0B0025.html).*\n\n",
        "## Was schreibt das Gesetz meiner Geschäftsleitung vor?\n\n"
        "Nach § 38 BSIG muss die Geschäftsleitung besonders wichtiger und "
        "wichtiger Einrichtungen die Risikomanagementmaßnahmen (§ 30 BSIG) "
        "**umsetzen und ihre Umsetzung überwachen** — und **regelmäßig an "
        "Schulungen** zu IT-Sicherheits-Risikomanagement teilnehmen. Diese "
        "Schulungspflicht ist konkret und wenig bekannt.\n\n"
        "*Primärquelle: [§ 38 BSIG](https://www.gesetze-im-internet.de/bsig_2025/BJNR12D0B0025.html).*\n\n",
        "## Wie sieht die Haftung konkret aus?\n\n"
        "§ 38 Abs. 2 BSIG verweist auf das jeweils geltende Gesellschaftsrecht: "
        "Haftung bei Pflichtverletzung ist zunächst **Innenhaftung gegenüber "
        "der eigenen Einrichtung**, nicht automatisch gegenüber Dritten. Für "
        "die GmbH gilt § 43 GmbHG (\"Sorgfalt eines ordentlichen "
        "Geschäftsmannes\", gesamtschuldnerische Haftung, Verjährung 5 "
        "Jahre), für die AG § 93 AktG mit einem entlastenden Detail: keine "
        "Pflichtverletzung liegt vor, wenn \"vernünftigerweise angenommen "
        "werden durfte, auf Grundlage angemessener Information zum Wohle der "
        "Gesellschaft zu handeln\" (Business Judgment Rule, § 93 Abs. 1 Satz "
        "2 AktG) — eine dokumentierte, informierte Entscheidung schützt. Ein "
        "nachvollziehbarer, öffentlich anerkannter Katalog wie Grundschutz++ "
        "ist genau das: ein Beleg für eine solche informierte Entscheidung, "
        "keine Garantie gegen Haftung.\n\n"
        "*Primärquellen: [§ 43 GmbHG](https://www.gesetze-im-internet.de/gmbhg/__43.html), "
        "[§ 93 AktG](https://www.gesetze-im-internet.de/aktg/__93.html).*\n\n",
        "## Sinnvolle Kennzahlen\n\n"
        "Diese Seite berechnet keinen Umsetzungsstatus für eure Organisation "
        "— dafür bräuchte es eine tatsächliche Bestandsaufnahme, keine "
        "statische Katalogseite. Als Rahmen für die eigene Berichterstattung "
        "eignen sich üblicherweise:\n\n"
        "- Anteil umgesetzter MUSS-Anforderungen (Zähler/Nenner wie oben, "
        "aber mit eurem tatsächlichen Stand)\n"
        "- Anzahl offener SOLLTE-Empfehlungen mit dokumentierter Begründung, "
        "falls nicht umgesetzt\n"
        "- Alter der letzten Schutzbedarfsfeststellung bzw. Risikobewertung\n"
        "- Datum der letzten Schulungsteilnahme der Geschäftsleitung (§ 38 "
        "Abs. 3 BSIG)\n\n",
        "## Die MUSS-Anforderungen nach Bereich\n\n",
        *sections,
    ]
    ROLLEN_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (ROLLEN_OUT_DIR / "geschaeftsfuehrung.md").write_text("".join(lines))


def render_isb_page(management, groups_by_id):
    entries = []
    for gid, title, slug, summary in management:
        count = len(list(collect_leaf_controls(groups_by_id[gid])))
        entries.append((gid, title, slug, f"{summary} ({count} Anforderungen)"))

    lines = [
        "---\ntitle: " + yaml_quote("Für ISB") + "\n---\n\n",
        "Der BSI-OSCAL-Katalog (`Grundschutz++-resolved_catalog.json`, CC "
        "BY-SA 4.0, BSI-Bund) ist für Maschinen geschrieben – SSP-Generierung, "
        "Tooling, Validierung. OSCAL selbst stammt von NIST, nicht vom BSI: "
        "ein bereits etablierter, international genutzter Standard, den das "
        "BSI bewusst übernommen hat, statt eine eigene Lösung zu bauen.\n\n"
        "Diese Seite übersetzt denselben Katalog in etwas, das man als ISB im "
        "Tagesgeschäft tatsächlich liest.\n\n",
        "## Der PDCA-Zyklus\n\n"
        "[Governance & Compliance](/grundschutzpp/gc/) → "
        "[Strukturmodellierung](/grundschutzpp/stm/) → "
        "[Umsetzung](/grundschutzpp/ums/) → "
        "[Monitoring-Evaluation](/grundschutzpp/perf/) → "
        "[Verbesserung](/grundschutzpp/vrb/) — und schließt sich von dort "
        "wieder zu Governance & Compliance. Ein echter Kreislauf, kein "
        "linearer Ablauf. [Risikomanagement](/grundschutzpp/risk/) begleitet "
        "alle fünf Phasen durchgehend, statt eine eigene Phase zu sein.\n\n",
        render_index_section(
            "Die sechs Praktiken im Detail",
            "",
            entries,
        ),
        "## Werkzeuge für den Alltag\n\n"
        "- **[Vergleich: Altes Kompendium ↔ Grundschutz++](/vergleich/)** — "
        "jede Zuordnung zwischen alter und neuer Anforderung, mit "
        "Beziehungstyp (entspricht/Teilbereich von/umfasst/überschneidet "
        "sich mit) und echten Links zu BSI's Baustein-PDFs.\n"
        "- **[Status & Zeitplan](/grundschutzpp/zeitplan/)** — Pilotphase, "
        "Übergangsfrist, geplante Zertifizierung.\n\n"
        "Diese Seite ist kein offizielles BSI-Angebot.\n",
    ]
    ROLLEN_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (ROLLEN_OUT_DIR / "isb.md").write_text("".join(lines))


# Redaktionelle Zweiteilung der 14 operativen Themenfelder (keine BSI-eigene
# Kategorie -- deshalb auf der Seite selbst als Einordnung gekennzeichnet).
# Kriterium: setzt ein Dev/eine Dev-nahe Rolle das direkt um (Code, Config,
# Systeme), oder ist es Prozess/Personal/Einkauf/Gebäude, das nur indirekt
# betrifft. ASST ist ein Grenzfall -- Datenklassifizierung wirkt sich direkt
# auf den Umgang mit Daten im Code aus, daher hier bei "technisch" einsortiert.
# Identisch mit Grundschutz-Docs-Hosted/scripts/generate_docs.py (kein
# Code-Sharing zwischen den Repos, siehe ADR-0001 im Hosted-Repo).
DEV_TECHNICAL_GROUPS = ["ARCH", "KONF", "DEV", "BER", "DET", "NOT", "REA", "TEST", "ASST"]
DEV_ORG_GROUPS = ["PERS", "BES", "DLS", "GEB", "SENS"]


def render_devs_page(themenfelder, groups_by_id):
    by_id = {gid: (title, slug, summary) for gid, title, slug, summary in themenfelder}

    def entries_for(group_ids):
        out = []
        for gid in group_ids:
            title, slug, summary = by_id[gid]
            count = len(list(collect_leaf_controls(groups_by_id[gid])))
            out.append((gid, title, slug, f"{summary} ({count} Anforderungen)"))
        return out

    lines = [
        "---\ntitle: " + yaml_quote("Für Devs") + "\n---\n\n",
        "Jede Anforderung zeigt Pflichtgrad, Sicherheitsstufe, "
        "Aufwandsschätzung und zugeordnete Basisgefährdungen direkt am "
        "Text — keine ISMS-Prozess-Erklärung davor, kein Umweg über das "
        "Managementsystem.\n\n",
        render_index_section(
            "Technische Umsetzung",
            "Das betrifft dich direkt — Architektur, Konfiguration, Code, Zugriffe, Betrieb.",
            entries_for(DEV_TECHNICAL_GROUPS),
        ),
        render_index_section(
            "Organisatorisch",
            "Betrifft dich eher indirekt (z. B. wenn ein Dienstleister Zugriff "
            "auf dein System bekommt) — der Vollständigkeit halber trotzdem aufgeführt.",
            entries_for(DEV_ORG_GROUPS),
        ),
        "Die Zweiteilung oben ist eine redaktionelle Einordnung dieser "
        "Seite, keine offizielle BSI-Kategorie — der Katalog selbst kennt "
        "nur die 14 Themenfelder ohne diese Unterscheidung.\n",
    ]
    ROLLEN_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (ROLLEN_OUT_DIR / "devs.md").write_text("".join(lines))


def build_all_mappings(mapping_data):
    mappings = []
    for group in mapping_data["mapping-collection"]["mappings"]:
        for m in group.get("maps", []):
            rel = m.get("relationship")
            sources = m.get("sources", [])
            targets = m.get("targets", [])
            if not sources or not targets or not rel:
                continue
            old_id = sources[0].get("id-ref")
            new_id = targets[0].get("id-ref")
            if not old_id or not new_id:
                continue
            mappings.append((old_id, rel, new_id))
    return mappings


def render_vergleich_page(all_mappings, group_titles, baustein_links):
    by_group = {}
    for old_id, rel, new_id in all_mappings:
        group_id = new_id.split(".")[0]
        by_group.setdefault(group_id, []).append((old_id, rel, new_id))

    lines = [
        "---\n",
        f"title: {yaml_quote('Vergleich: Altes Kompendium ↔ Grundschutz++')}\n",
        f"description: {yaml_quote('Alle Zuordnungen zwischen dem alten IT-Grundschutz-Kompendium (Edition 2023) und dem neuen Grundschutz++-Katalog.')}\n",
        "---\n",
        "\n",
        "Alle Zuordnungen aus der offiziellen BSI-Mapping-Datei "
        "(`ITGS-to-GS++-mapping_collection.json`) — kein alter Volltext, nur "
        "Struktur und echte Links zu BSI's eigenen Baustein-PDFs (siehe "
        "ADR-0005 im Hosted-Repo). Mit Strg+F/Cmd+F nach einer bekannten "
        "alten ID suchen, z. B. `OPS.1.1.5`.\n",
        "\n",
    ]
    for group_id in sorted(by_group, key=lambda gid: group_titles.get(gid, gid)):
        entries = by_group[group_id]
        title = group_titles.get(group_id, group_id)
        slug = group_id.lower()
        lines.append(f"## {group_id} {title}\n")
        lines.append("\n")
        lines.append("| Alte Anforderung | Beziehung | Neue Anforderung |\n")
        lines.append("|---|---|---|\n")
        for old_id, rel, new_id in sorted(entries, key=lambda e: e[2]):
            baustein_id = baustein_id_from_itgs_id(old_id)
            link = baustein_links.get(baustein_id) if baustein_id else None
            old_cell = f"[{old_id}]({link})" if link else old_id
            new_cell = f"[{new_id}](/grundschutzpp/{slug}/)"
            lines.append(f"| {old_cell} | {relationship_label(rel)} | {new_cell} |\n")
        lines.append("\n")
    return "".join(lines)


def render_index_section(heading, intro, entries):
    lines = [f"## {heading}\n", f"{intro}\n", '<ul class="practice-index">']
    for gid, title, slug, summary in entries:
        lines.append(
            f'<li><a href="/grundschutzpp/{slug}/"><span class="practice-id">{gid}</span> {title}</a>'
            f"<p>{summary}</p></li>"
        )
    lines.append("</ul>\n")
    return "\n".join(lines)


def main():
    data = json.loads(CATALOG_FILE.read_text())
    catalog = data["catalog"]
    params_by_id = build_params_index(catalog)
    mapping_data = json.loads(MAPPING_FILE.read_text())
    predecessor_index = build_predecessor_index(mapping_data)
    baustein_links = json.loads(BAUSTEINE_LINKS_FILE.read_text())["bausteine"]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()
    ROLLEN_OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in ROLLEN_OUT_DIR.glob("*.md"):
        old.unlink()

    management, themenfelder = [], []
    group_titles = {}
    groups_by_id = {group["id"]: group for group in catalog["groups"]}
    for group in catalog["groups"]:
        slug = group["id"].lower()
        group_titles[group["id"]] = group["title"]
        # include_heading=False: Starlight rendert die Seiten-Überschrift bereits
        # automatisch aus der Frontmatter — sonst stünde sie doppelt auf der Seite.
        body = render_group(
            group,
            level=1,
            params_by_id=params_by_id,
            predecessor_index=predecessor_index,
            baustein_links=baustein_links,
            include_heading=False,
        )
        summary = first_sentence(group_description(group))
        page_title = f"{group['id']} – {group['title']}"
        frontmatter = (
            "---\n"
            f"title: {yaml_quote(page_title)}\n"
            f"description: {yaml_quote(summary)}\n"
            "---\n\n"
        )
        (OUT_DIR / f"{slug}.md").write_text(frontmatter + body)

        entry = (group["id"], group["title"], slug, summary)
        (management if group["id"] in MANAGEMENT_CYCLE_IDS else themenfelder).append(entry)

    index_lines = [
        "---\ntitle: Start\n---\n\n",
        "Automatisch generiert aus dem OSCAL-Katalog. "
        "Nicht Teil des offiziellen BSI-Materials — eigene lesbare Aufbereitung.\n\n",
        render_index_section(
            "Managementsystem",
            "Diese sechs Praktiken bilden den PDCA-Zyklus des ISMS — von der "
            "strategischen Vorgabe bis zur kontinuierlichen Verbesserung.",
            management,
        ),
        render_index_section(
            "Themenfelder",
            "Operative Sicherheitspraktiken, die im Rahmen des Managementsystems umgesetzt werden.",
            themenfelder,
        ),
    ]
    (OUT_DIR / "index.md").write_text("\n".join(index_lines))

    zeitplan_lines = [
        "---\ntitle: Status & Zeitplan\n---\n\n",
        "Grundschutz++ ersetzt das bisherige IT-Grundschutz-Kompendium nicht von "
        "heute auf morgen. Stand nach BSI-Fahrplan und Fachpublikationen "
        "(nicht offiziell von der BSI in jedem Detail bestätigt):\n",
        render_timeline(),
    ]
    (OUT_DIR / "zeitplan.md").write_text("\n".join(zeitplan_lines))

    all_mappings = build_all_mappings(mapping_data)
    vergleich_body = render_vergleich_page(all_mappings, group_titles, baustein_links)
    (OUT_DIR.parent / "vergleich.md").write_text(vergleich_body)

    render_geschaeftsfuehrung_page(management, themenfelder, groups_by_id)
    render_isb_page(management, groups_by_id)
    render_devs_page(themenfelder, groups_by_id)

    total = len(management) + len(themenfelder)
    print(f"{total} Gruppen-Seiten erzeugt in {OUT_DIR}")
    print(f"3 Rollen-Seiten erzeugt in {ROLLEN_OUT_DIR}")

    def sidebar_group(label, entries):
        items = ",\n\t\t\t\t\t\t".join(
            f'{{ label: "{gid} {title}", slug: "grundschutzpp/{slug}" }}' for gid, title, slug, _ in entries
        )
        return f'{{\n\t\t\t\t\tlabel: "{label}",\n\t\t\t\t\titems: [\n\t\t\t\t\t\t{items},\n\t\t\t\t\t],\n\t\t\t\t}}'

    print("\nastro.config.mjs Sidebar-Snippet (manuell einfügen falls gewünscht):\n")
    print(sidebar_group("Managementsystem", management) + ",\n" + sidebar_group("Themenfelder", themenfelder))


if __name__ == "__main__":
    main()
