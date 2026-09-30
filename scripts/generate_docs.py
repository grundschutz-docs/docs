#!/usr/bin/env python3
"""
Liest den Grundschutz++-resolved_catalog.json (OSCAL) und generiert daraus
lesbare .mdx-Seiten fuer Starlight: eine Seite je Praktik, die drei
Rollen-Einstiegsseiten, und die Vergleichsseiten Altes Kompendium ↔
Grundschutz++ (eine Uebersicht plus eine Seite je altem Baustein).

.mdx statt .md, damit die generierten Seiten echte Komponenten nutzen
koennen (<ControlMeta> fuer Pflicht/Stufe/Aufwand, <PdcaCycle>, Filter).

Erneut ausfuehren nach jedem `git pull` im Grundschutz-PlusPlus-Repo — die
Checkliste dazu steht in CONTRIBUTING.md ("When the upstream catalog
changes"):

    cd Grundschutz-PlusPlus && git pull
    python3 ../Grundschutz-Docs/scripts/generate_docs.py
    cd ../Grundschutz-Docs && pnpm run build   # oder: pnpm run dev
"""
import csv
import json
import os
import re
import urllib.parse
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CATALOG_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "control_layer" / "Grundschutz++" / "Grundschutz++-resolved_catalog.json"
)
DEFAULT_BASETHREATS_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "documentation" / "namespaces" / "basethreats.csv"
)
# Lokal: Grundschutz-PlusPlus liegt als Ordner neben diesem Repo. In CI gibt es
# diesen Nachbarordner nicht — dort wird der Pfad stattdessen über die Umgebungsvariable
# gesetzt (siehe .github/workflows/sync-catalog.yml im OSS-Repo).
CATALOG_FILE = Path(os.environ["GRUNDSCHUTZPP_CATALOG"]) if os.environ.get("GRUNDSCHUTZPP_CATALOG") else DEFAULT_CATALOG_FILE
BASETHREATS_FILE = (
    Path(os.environ["GRUNDSCHUTZPP_BASETHREATS"]) if os.environ.get("GRUNDSCHUTZPP_BASETHREATS") else DEFAULT_BASETHREATS_FILE
)
DEFAULT_MAPPING_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "control_layer" / "Mappings" / "IT-GS2023-zu-GSpp" / "ITGS-to-GS++-mapping_collection.json"
)
MAPPING_FILE = Path(os.environ["GRUNDSCHUTZPP_MAPPING"]) if os.environ.get("GRUNDSCHUTZPP_MAPPING") else DEFAULT_MAPPING_FILE
# Grundschutz-Projekt/bsi-kompendium-2023-bausteine.json: eigene, einmal von
# BSIs Bausteine-Uebersichtsseite gescrapte Lookup-Tabelle (Baustein-ID -> PDF-URL),
# siehe adr/0005-vorgaenger-anforderung-alt-neu.md. Liegt bewusst eine Ebene
# ueber beiden Repos (wie SYNC.md) -- externe Referenzdaten, nicht Eigentum
# eines der beiden Repos.
DEFAULT_BAUSTEINE_LINKS_FILE = REPO_ROOT / "bsi-kompendium-2023-bausteine.json"
BAUSTEINE_LINKS_FILE = (
    Path(os.environ["BSI_BAUSTEINE_LINKS"]) if os.environ.get("BSI_BAUSTEINE_LINKS") else DEFAULT_BAUSTEINE_LINKS_FILE
)
OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "grundschutzpp"
# Rollen-Seiten (ADR-0007) liegen wie vergleich.mdx eine Ebene flacher als
# die Gruppen-Seiten, aber in einem eigenen Unterordner (eigene Sidebar-Gruppe).
ROLLEN_OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "rollen"
VERGLEICH_OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "vergleich"
DATA_OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "data"
CONTROL_META_IMPORT = "import ControlMeta from '../../../components/ControlMeta.astro';\n"
# vergleich.mdx liegt eine Ebene flacher (direkt in src/content/docs/), daher
# ein "../" weniger als CONTROL_META_IMPORT.
# Drei Ebenen hoch: src/content/docs/vergleich/index.mdx -> src/components/
VERGLEICH_FILTER_IMPORT = "import VergleichFilter from '../../../components/VergleichFilter.astro';\n"
# rollen/*.mdx liegt auf derselben Tiefe wie grundschutzpp/*.mdx (nicht wie
# vergleich.mdx), daher derselbe "../../../"-Pfad wie CONTROL_META_IMPORT.
GF_FILTER_IMPORT = "import GfFilter from '../../../components/GfFilter.astro';\n"
PDCA_CYCLE_IMPORT = "import PdcaCycle from '../../../components/PdcaCycle.astro';\n"

PARAM_RE = re.compile(r"\{\{\s*insert:\s*param,\s*([a-zA-Z0-9._-]+)\s*\}\}")

# Zeitplan laut BSI-Fahrplan (Pilotphase, it-sa-Termin) und Fachpublikationen
# (Übergangsfrist/Ablösung — vom BSI noch nicht mit einem fixen Datum bestätigt,
# daher als "geplant" ausgewiesen). Gleiche Quelle wie im OSS-Repo.
TIMELINE = [
    (date(2026, 4, 1), date(2026, 9, 30), "Pilotphase", "Grundschutz++ wird mit Pilotpartnern erprobt."),
    (date(2026, 10, 27), date(2026, 10, 29), "Vorstellung auf der it-sa", "Methodik und Kompendium werden öffentlich vorgestellt."),
    (date(2026, 4, 1), date(2029, 12, 31), "Übergangsphase", "Das bisherige IT-Grundschutz-Kompendium bleibt parallel gültig."),
    (date(2027, 1, 1), None, "Zertifizierung möglich (geplant)", "Eine Zertifizierung nach Grundschutz++ soll ab 2027 möglich sein."),
    (date(2029, 1, 1), None, "Vollständige Ablösung (geplant, Datum offen)", "Das bisherige Kompendium soll danach vollständig abgelöst werden."),
]

# Wie im OSS-Repo: der Katalog selbst nennt diese sechs Praktiken den
# PDCA-Managementzyklus (z. B. VRB: "schließt den PDCA-Zyklus ab").
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


def mdx_safe(text):
    if not text:
        return text
    # MDX interpretiert { und } als JS-Ausdruck-Grenzen und < als möglichen
    # JSX-Tag-Start (z. B. bricht "Latenz < Antwortzeit" sonst den Build,
    # siehe ARCH-Gruppe). Im Katalog kommt das aktuell selten vor (geprüft),
    # aber falls ein künftiges Upstream-Update mehr davon einführt, brechen
    # wir damit nicht den Build, sondern zeigen ein literales Zeichen.
    text = text.replace("{", "\\{").replace("}", "\\}")
    return text.replace("<", "&lt;")


def substitute_params(text, params_by_id):
    if not text:
        return text

    def repl(m):
        pid = m.group(1)
        label = params_by_id.get(pid, pid)
        return f"*[{label}]*"

    return mdx_safe(PARAM_RE.sub(repl, text))


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


def attr_escape(value):
    return value.replace("&", "&amp;").replace('"', "&quot;")


def load_basethreats():
    with BASETHREATS_FILE.open(newline="", encoding="utf-8") as f:
        return {row["ID"]: row["Begriff"] for row in csv.DictReader(f)}


def threats_hint(threats, basethreats_by_id):
    ids = [t.strip() for t in threats.split(",") if t.strip()]
    labeled = [f"{tid} – {basethreats_by_id[tid]}" for tid in ids if tid in basethreats_by_id]
    return " · ".join(labeled) if labeled else None


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


# Die zehn Schichten des alten IT-Grundschutz-Kompendiums. Nur zum Gruppieren
# der Baustein-Uebersicht -- das Kompendium selbst wird nirgends reproduziert.
KOMPENDIUM_LAYERS = {
    "ISMS": "Sicherheitsmanagement",
    "ORP": "Organisation und Personal",
    "CON": "Konzeption und Vorgehensweisen",
    "OPS": "Betrieb",
    "DER": "Detektion und Reaktion",
    "APP": "Anwendungen",
    "SYS": "IT-Systeme",
    "IND": "Industrielle IT",
    "NET": "Netze und Kommunikation",
    "INF": "Infrastruktur",
}


def baustein_slug(baustein_id):
    # "OPS.1.1.5" -> "ops-1-1-5"
    return baustein_id.lower().replace(".", "-")


def baustein_title(baustein_id, url):
    """Baustein-Titel aus dem BSI-PDF-Dateinamen ableiten.

    bsi-kompendium-2023-bausteine.json enthaelt nur ID -> PDF-URL, aber der
    Dateiname traegt den Titel mit ("OPS_1_1_5_Protokollierung_Edition_2023
    .pdf" -> "Protokollierung"). Fuer alle 111 Bausteine geprueft.

    Bekannte Grenze: Bindestriche zusammengesetzter Titel gehen im
    Dateinamen verloren. "Netzarchitektur und -design" laesst sich aus dem
    folgenden Kleinbuchstaben rekonstruieren, "Prozessleit- und
    Automatisierungstechnik" nicht -- dort haengt der Bindestrich am ersten
    Wort und ist spurlos weg.
    """
    if not url:
        return ""
    name = urllib.parse.urlparse(url).path.rsplit("/", 1)[-1]
    name = re.sub(r"(?:_Edition_\d{4})?\.pdf$", "", name)
    prefix = baustein_id.replace(".", "_") + "_"
    if name.startswith(prefix):
        name = name[len(prefix) :]
    title = name.replace("_", " ").strip()
    return re.sub(r"\bund ([a-zäöü])", r"und -\1", title)


# Beispiel-Control für den Startseiten-Vergleich "Rohes OSCAL ↔ gelesene
# Anforderung". Bewusst eine kurze Anforderung aus dem Managementsystem, deren
# Begriff jede:r ISB kennt. Verschwindet die ID aus dem Katalog, bricht der
# Generator mit einer Meldung ab, statt die Startseite still leerzulassen.
# Das Beispiel auf der Startseite ist das erste und oft einzige, das jemand
# von diesem Katalog sieht -- es muss ohne Vorwissen verstaendlich sein.
# Vorher UMS.1.2 ("Umsetzung SOLLTE das bestehende Restrisiko durch die nicht
# umgesetzten Anforderungen festlegen"), was durch das BSI-Satzmuster
# "[Praktikname] MUSS/SOLLTE [Verbphrase]" grammatisch schief wirkt: die
# Praktik ist Subjekt, aber "Umsetzung" ist kein Handelnder. Das betrifft alle
# Anforderungen, laesst sich also nicht wegaufbereiten -- aber das Schaufenster
# muss nicht ausgerechnet ein Exemplar zeigen, an dem es auffaellt.
LANDING_SAMPLE_ID = "NOT.4.10"


def find_control(catalog, control_id):
    def walk(node):
        for control in node.get("controls", []) or []:
            if control["id"] == control_id:
                return control
            hit = walk(control)
            if hit:
                return hit
        return None

    for group in catalog.get("groups", []) or []:
        hit = walk(group)
        if hit:
            return hit
        for subgroup in group.get("groups", []) or []:
            hit = walk(subgroup)
            if hit:
                return hit
    return None


def trim_prose(node, limit=150):
    """Kopie des Controls mit gekürzter Prosa — der Roh-JSON-Ausschnitt auf der
    Startseite soll die *Struktur* zeigen, nicht eine Textwand sein."""
    clone = json.loads(json.dumps(node))
    for part in clone.get("parts", []) or []:
        prose = part.get("prose")
        if prose and len(prose) > limit:
            part["prose"] = prose[:limit].rstrip() + " …"
    clone.pop("controls", None)
    return clone


def write_landing_data(catalog, control_index, by_baustein, all_mappings, params_by_id, baustein_links):
    """Zahlen und Beispiel für die Startseite (LandingStats/CatalogPreview).

    Wird generiert statt von Hand gepflegt, damit die Zahlen auf der
    Startseite nicht irgendwann etwas anderes behaupten als der Katalog.
    """
    sample = find_control(catalog, LANDING_SAMPLE_ID)
    if sample is None:
        raise SystemExit(
            f"Startseiten-Beispiel {LANDING_SAMPLE_ID} existiert im Katalog nicht mehr. "
            "LANDING_SAMPLE_ID in scripts/generate_docs.py auf eine aktuelle, kurze "
            "Anforderung setzen."
        )

    # Zaehler und Nenner muessen aus derselben Welt stammen: taucht ein
    # zugeordneter Baustein nicht in der Kompendium-Liste auf, waere die Quote
    # groesser als 100 % oder schlicht falsch.
    unbekannt = sorted(set(by_baustein) - set(baustein_links))
    if unbekannt:
        raise SystemExit(
            "Zugeordnete Bausteine fehlen in bsi-kompendium-2023-bausteine.json, "
            f"die Abdeckungsquote waere falsch: {', '.join(unbekannt)}"
        )

    data = {
        "stats": {
            "controls": len(control_index),
            "practices": len(catalog.get("groups", []) or []),
            "bausteine": len(by_baustein),
            # Ohne Nenner ist "94 Bausteine" keine Abdeckungsangabe, sondern
            # eine Zahl ohne Bezug -- man kann nicht einschaetzen, ob das viel
            # oder wenig ist. Der Nenner ist die Bausteinliste des Kompendiums
            # 2023, die hier ohnehin schon fuer die PDF-Links geladen wird.
            "bausteine_gesamt": len(baustein_links),
            # Bewusst die Zuordnungen, die auch wirklich auf einer Seite stehen,
            # nicht alle 1185 aus der Datei — ein paar davon haben keine
            # auswertbare Baustein-ID und tauchen nirgends auf. Eine Zahl auf
            # der Startseite muss zählen, was man tatsächlich findet.
            "mappings": sum(len(entries) for entries in by_baustein.values()),
        },
        "sample": {
            "id": sample["id"],
            "title": sample["title"],
            "statement": substitute_params(part_text(sample, "statement"), params_by_id),
            "modal_verb": part_prop_value(sample, "statement", "modal_verb") or "",
            "sec_level": prop_value(sample, "sec_level") or "",
            "effort_level": prop_value(sample, "effort_level") or "",
            "raw": json.dumps(trim_prose(sample), indent=2, ensure_ascii=False),
        },
    }
    DATA_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_OUT_DIR / "landing.json").write_text(
        json.dumps(data, indent="\t", ensure_ascii=False) + "\n"
    )
    return data["stats"]


def build_control_index(catalog):
    """control-id -> {slug, title} der Gruppenseite, auf der das Control steht.

    Basis fuer die Anker-Links: ohne das zeigen die Vergleichsseiten nur auf
    die Gruppenseite und man landet oben auf 150 KB Text.
    """
    index = {}

    def walk(node, slug):
        for control in node.get("controls", []) or []:
            index[control["id"]] = {"slug": slug, "title": control.get("title", "")}
            walk(control, slug)

    for group in catalog.get("groups", []) or []:
        slug = group["id"].lower()
        walk(group, slug)
        for subgroup in group.get("groups", []) or []:
            walk(subgroup, slug)
    return index


def control_link(control_id, control_index):
    """Link auf das Control selbst (Gruppenseite + Anker), mit Titel als Text."""
    entry = control_index.get(control_id)
    if not entry:
        return f'<span class="new-id">{control_id}</span>'
    href = f"/grundschutzpp/{entry['slug']}/#{control_id}"
    title = entry["title"]
    suffix = f" <span class=\"new-title\">{title}</span>" if title else ""
    return f'<a class="new-id" href="{href}">{control_id}</a>{suffix}'


# OSCAL-Beziehungstypen sind englisches Standard-Vokabular -- für die
# Vergleichsseite (Vergleich.mdx wird als reines HTML/Markdown geschrieben,
# nicht über ControlMeta.astro) übersetzt anzeigen, analog zu den
# deutschen Labels in ControlMeta.astro. `data-rel` bleibt englisch (CSS-
# Selektor-Matching gegen custom.css unverändert).
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


def jsx_string(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_predecessors_prop(control_id, predecessor_index, baustein_links):
    entries = predecessor_index.get(control_id)
    if not entries:
        return None
    items = []
    for old_id, rel in entries:
        baustein_id = baustein_id_from_itgs_id(old_id)
        link = baustein_links.get(baustein_id) if baustein_id else None
        obj = f"{{ oldId: {jsx_string(old_id)}, relationship: {jsx_string(rel)}"
        if link:
            obj += f", link: {jsx_string(link)}"
        obj += " }"
        items.append(obj)
    return "[" + ", ".join(items) + "]"


def render_control_meta(control, basethreats_by_id, predecessor_index, baustein_links):
    modal_verb = part_prop_value(control, "statement", "modal_verb")
    sec_level = prop_value(control, "sec_level")
    effort = prop_value(control, "effort_level")
    threats = prop_value(control, "threats")
    predecessors = render_predecessors_prop(control["id"], predecessor_index, baustein_links)
    if not (modal_verb or sec_level or effort or threats or predecessors):
        return None
    attrs = []
    if modal_verb:
        attrs.append(f'modalVerb="{attr_escape(modal_verb)}"')
    if sec_level:
        attrs.append(f'secLevel="{attr_escape(sec_level)}"')
    if effort:
        attrs.append(f'effort="{attr_escape(effort)}"')
    if threats:
        attrs.append(f'threats="{attr_escape(threats)}"')
        hint = threats_hint(threats, basethreats_by_id)
        if hint:
            attrs.append(f'threatsHint="{attr_escape(hint)}"')
    if predecessors:
        attrs.append(f"predecessors={{{predecessors}}}")
    return f"<ControlMeta {' '.join(attrs)} />\n"


def heading_anchor(id_):
    """{#id}-Ueberschriften-Attribut, nativ vom Satteri-Markdown-Prozessor
    geparst (markdown.processor in astro.config.mjs, features.headingAttributes).
    Satteri konsumiert die {}-Syntax vor MDX' eigenem Ausdrucks-Scanner --
    kein HTML-Entity-Escaping noetig, mit Build + Link-Validator bestaetigt."""
    return f"{{#{id_}}}"


def render_control(control, level, params_by_id, basethreats_by_id, predecessor_index, baustein_links):
    heading = "#" * min(level, 6)
    # {#...} setzt die Anker-ID explizit statt sie Starlights Auto-Slug zu
    # ueberlassen (der slugifiziert den ganzen Titel, z. B.
    # "det31--verfahren-und-regelungen") -- das aendert sich, sobald das BSI
    # eine Formulierung anfasst, und genau darauf zeigen die ~1200 Links der
    # Vergleichsseiten. Die Control-ID ist stabil, also ankern wir daran.
    # Satteris headingAttributes-Feature macht daraus die tatsaechliche
    # Element-ID, auch in Starlights eigener "Auf dieser Seite"-Navigation.
    lines = [
        f"{heading} {control['id']} – {control['title']} {heading_anchor(control['id'])}\n",
    ]

    meta = render_control_meta(control, basethreats_by_id, predecessor_index, baustein_links)
    if meta:
        lines.append(meta)

    statement = substitute_params(part_text(control, "statement"), params_by_id)
    if statement:
        lines.append(f"> {statement}\n")

    guidance = substitute_params(part_text(control, "guidance"), params_by_id)
    if guidance:
        lines.append(f"{guidance}\n")

    for sub in control.get("controls", []):
        lines.append(render_control(sub, level + 1, params_by_id, basethreats_by_id, predecessor_index, baustein_links))

    return "\n".join(lines)


def render_group(group, level, params_by_id, basethreats_by_id, predecessor_index, baustein_links, include_heading=True):
    lines = []
    if include_heading:
        heading = "#" * min(level, 6)
        # Gleicher Grund wie bei render_control: stabile ID statt Starlights
        # Auto-Slug aus dem Titeltext (siehe heading_anchor()).
        lines.append(f"{heading} {group['id']} {group['title']} {heading_anchor(group['id'])}\n")

    desc = mdx_safe(group_description(group))
    if desc:
        lines.append(f"{desc}\n")

    for control in group.get("controls", []):
        lines.append(render_control(control, level + 1, params_by_id, basethreats_by_id, predecessor_index, baustein_links))

    for sub in group.get("groups", []):
        lines.append(render_group(sub, level + 1, params_by_id, basethreats_by_id, predecessor_index, baustein_links))

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


# Abkürzungen, die auf einen Punkt enden, ohne einen Satz zu beenden. Ohne
# diese Liste bricht first_sentence() mitten im Satz ab und die
# Meta-Description der Seite landet als Fragment in der Google-Vorschau
# ("... Dokumentation von Anforderungen bzw." — UMS, 2026-09-29).
SENTENCE_ABBREVS = (
    "bzw.", "ggf.", "etc.", "ca.", "inkl.", "exkl.", "vgl.", "sog.", "evtl.",
    "insb.", "Nr.", "Abs.", "Art.", "Kap.", "ff.",
    "z. B.", "z.B.", "u. a.", "u.a.", "d. h.", "d.h.", "i. d. R.", "u. U.",
)
# Bewusst nicht in der Liste: "S." (Seite) und "max."/"min." — die würden
# auch das Ende echter Sätze verschlucken ("... und IDS.", "... auf ein
# Minimum.") und kosten mehr, als sie retten.

# Einzelbuchstabe + Punkt ("z.", "B.", "u.") — die Hälften gesperrter
# Abkürzungen, wenn der Text sie mit schmalem Leerzeichen schreibt.
SINGLE_LETTER_ABBREV_RE = re.compile(r"\b[A-Za-zÄÖÜäöü]\.$")


def first_sentence(text):
    if not text:
        return ""
    for match in re.finditer(r"[.!?](\s|$)", text):
        candidate = text[: match.end()].strip()
        if candidate.endswith(SENTENCE_ABBREVS):
            continue
        if SINGLE_LETTER_ABBREV_RE.search(candidate):
            continue
        return candidate
    return text


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


def render_index_section(heading, intro, entries):
    lines = [f"## {heading}\n", f"{intro}\n", '<ul class="practice-index">']
    for gid, title, slug, summary in entries:
        lines.append(
            f'<li><a href="/grundschutzpp/{slug}/"><span class="practice-id">{gid}</span> {title}</a>'
            f"<p>{summary}</p></li>"
        )
    lines.append("</ul>\n")
    return "\n".join(lines)


def check_invariants(catalog, control_index, muss_controls, by_baustein):
    """Bricht den Lauf ab, wenn eine Zahl auf der Seite nicht zur Quelle passt.

    Entstanden aus einem realen Fehler (2026-09-30): die Geschaeftsfuehrungs-
    Seite behauptete "123 von 874 Anforderungen sind MUSS", tatsaechlich sind
    es 149 von 1000 — 26 MUSS-Anforderungen fehlten in der Tabelle. Build und
    Link-Pruefung waren dabei durchgehend gruen.

    Warum es niemand merkte: Ueberschrift und Tabelle stammten aus **derselben**
    Funktion. Sie waren untereinander konsistent, also sah die Uebereinstimmung
    nach Bestaetigung aus — sie war aber nur der gemeinsame Fehler.

    Deshalb die Regel fuer alles hier drin: **jede Zahl auf zwei unabhaengigen
    Wegen ermitteln.** Die Pruefungen unten lesen die *fertig geschriebenen*
    Dateien zurueck und vergleichen sie mit den Katalogdaten. Eine Pruefung,
    die denselben Codepfad nimmt wie der Renderer, ist wertlos.
    """
    problems = []

    def count_in(path, needle):
        return path.read_text().count(needle) if path.exists() else -1

    all_controls = list(collect_controls(catalog))

    # 1. Gibt es Knoten ohne eigene Anforderung? Die Blatt-Logik von frueher
    #    beruhte auf der Annahme, Eltern-Knoten seien reine Container. Falls
    #    das BSI je echte Container einfuehrt, muss das eine Entscheidung
    #    ausloesen und nicht still die Zahlen verschieben.
    ohne_statement = [c["id"] for c in all_controls if not part_text(c, "statement")]
    if ohne_statement:
        problems.append(
            f"{len(ohne_statement)} Controls ohne eigenes statement "
            f"(z. B. {ohne_statement[:5]}). Bisher hatte jeder Knoten eine eigene "
            "Anforderung — wenn sich das aendert, muss entschieden werden, ob sie "
            "weiter mitgezaehlt werden."
        )

    # 2. Jede Anforderung hat genau ein Modalverb — sonst stimmt die
    #    MUSS/SOLLTE/KANN-Aufteilung nicht mehr mit der Gesamtzahl ueberein.
    modals = [part_prop_value(c, "statement", "modal_verb") for c in all_controls]
    ohne_modal = [c["id"] for c, m in zip(all_controls, modals) if not m]
    if ohne_modal:
        problems.append(f"{len(ohne_modal)} Controls ohne modal_verb (z. B. {ohne_modal[:5]})")

    # 3. Summe ueber die Gruppen == Gesamtzahl (unabhaengiger Zaehlweg).
    per_group = sum(
        len(list(collect_controls(g))) for g in catalog.get("groups", []) or []
    )
    if per_group != len(all_controls):
        problems.append(
            f"Summe je Gruppe ({per_group}) != Gesamtzahl Controls ({len(all_controls)})"
        )

    if len(control_index) != len(all_controls):
        problems.append(
            f"control_index ({len(control_index)}) != Controls im Katalog ({len(all_controls)})"
        )

    # 4. Aus den geschriebenen Katalogseiten zurueckgelesen: eine {#id}-Anker-
    #    Markierung je Control (Satteris headingAttributes-Feature macht
    #    daraus die tatsaechliche Element-ID). Pro ID geprueft statt nur als Gesamtzahl --
    #    sonst wuerden sich ein fehlender und ein doppelter Anker im
    #    Gesamtcount gegenseitig verstecken, wie im Vorfall oben beschrieben.
    catalog_text = "\n".join(p.read_text() for p in OUT_DIR.glob("*.mdx"))
    missing_anchors = [c["id"] for c in all_controls if heading_anchor(c["id"]) not in catalog_text]
    if missing_anchors:
        problems.append(
            f"{len(missing_anchors)} Controls ohne {{#id}}-Anker in den Katalogseiten "
            f"(z. B. {missing_anchors[:5]})"
        )

    # 5. Aus der geschriebenen GF-Seite zurueckgelesen: eine Zeile je MUSS.
    gf = ROLLEN_OUT_DIR / "geschaeftsfuehrung.mdx"
    gf_rows = count_in(gf, "<tr data-sec=")
    if gf_rows != len(muss_controls):
        problems.append(
            f"{gf_rows} MUSS-Zeilen auf der Geschaeftsfuehrungs-Seite, "
            f"aber {len(muss_controls)} MUSS-Anforderungen im Katalog"
        )
    if gf.exists() and f"{len(muss_controls)} von {len(all_controls)} " not in gf.read_text():
        problems.append(
            f"Die Ueberschrift der GF-Seite nennt nicht "
            f"'{len(muss_controls)} von {len(all_controls)}'"
        )

    # 6. Aus den geschriebenen Baustein-Seiten zurueckgelesen: eine Zeile je Zuordnung.
    expected_rows = sum(len(e) for e in by_baustein.values())
    actual_rows = sum(
        count_in(p, "<tr><td>")
        for p in VERGLEICH_OUT_DIR.glob("*.mdx")
        if p.name != "index.mdx"
    )
    if actual_rows != expected_rows:
        problems.append(
            f"{actual_rows} Zuordnungszeilen auf den Baustein-Seiten, "
            f"aber {expected_rows} Zuordnungen in der Mapping-Datei"
        )

    # 7. Die Startseiten-Zahlen gegen dieselben Quellen.
    landing = json.loads((DATA_OUT_DIR / "landing.json").read_text())["stats"]
    if landing["controls"] != len(all_controls):
        problems.append(
            f"landing.json nennt {landing['controls']} Anforderungen, "
            f"der Katalog hat {len(all_controls)}"
        )
    if landing["mappings"] != expected_rows:
        problems.append(
            f"landing.json nennt {landing['mappings']} Zuordnungen, "
            f"auf den Seiten stehen {expected_rows}"
        )

    if problems:
        raise SystemExit(
            "Zahlen auf der Seite passen nicht zum Katalog:\n  - "
            + "\n  - ".join(problems)
        )

    print(
        f"Plausibilitaet ok: {len(all_controls)} Anforderungen "
        f"({len(muss_controls)} MUSS), {len(all_controls)} Anker, {actual_rows} Zuordnungen"
    )


def collect_controls(node):
    """Alle Anforderungen unter einem Control- oder Gruppen-Knoten, rekursiv.
    Funktioniert fuer beide Knotentypen, weil beide optionale
    "controls"/"groups"-Listen haben (OSCAL-Struktur).

    Zaehlt bewusst **jeden** Control-Knoten, nicht nur Blaetter. Frueher
    wurden hier nur Blaetter gesammelt, in der Annahme, Eltern-Knoten seien
    reine Struktur-Container. Das ist in diesem Katalog falsch: gegen den
    Katalogstand geprueft haben **alle 1000** Knoten ein eigenes `statement`
    mit eigenem Modalverb, auch die 126 mit Unter-Anforderungen (z. B. GC.3.1
    "... MUSS ein Verfahren zur systematischen Erfassung ... festlegen").
    Die Blatt-Logik hat dadurch 26 der 149 MUSS-Anforderungen unterschlagen —
    ausgerechnet auf der Geschaeftsfuehrungs-Seite, die von Pflichten handelt.
    """
    for c in node.get("controls", []):
        yield c
        yield from collect_controls(c)
    for g in node.get("groups", []):
        yield from collect_controls(g)


def is_muss(control):
    return part_prop_value(control, "statement", "modal_verb") == "MUSS"


# Quelle: Grundschutz-PlusPlus/documentation/namespaces/security_level.csv --
# nur diese zwei Werte existieren im Katalog (kein Basis/Standard/Kern wie im
# alten Kompendium), siehe ADR-0007.
SEC_LEVEL_LABELS = {"normal-SdT": "Standard-Sicherheitsstufe", "erhöht": "Erhöhte Sicherheitsstufe"}


def render_muss_table(group_id, group_title, slug, muss_controls):
    lines = [f'<div class="rollen-section" data-group="{group_id}">\n']
    lines.append(f"### {group_id} {group_title} {heading_anchor(group_id)}\n")
    lines.append('<table class="vergleich-table rollen-muss-table">\n')
    lines.append("<thead><tr><th>Anforderung</th><th>Stufe</th></tr></thead>\n<tbody>\n")
    for control in muss_controls:
        sec_level = prop_value(control, "sec_level") or ""
        sec_label = SEC_LEVEL_LABELS.get(sec_level, sec_level)
        lines.append(
            f'<tr data-sec="{attr_escape(sec_level)}">'
            # Mit Anker: ohne ihn landet man oben auf einer bis zu 150 KB langen
            # Gruppenseite und sucht die Anforderung selbst. Die Anker setzt
            # render_control().
            f'<td><a class="new-id" href="/grundschutzpp/{slug}/#{control["id"]}">'
            f'{control["id"]} – {control["title"]}</a></td>'
            f'<td>{sec_label}</td></tr>\n'
        )
    lines.append("</tbody>\n</table>\n</div>\n\n")
    return "".join(lines)


def render_geschaeftsfuehrung_page(management, themenfelder, groups_by_id):
    all_groups = management + themenfelder
    total = 0
    total_muss = 0
    muss_normal_sdt = 0
    sections = []
    for gid, title, slug, _ in all_groups:
        controls = list(collect_controls(groups_by_id[gid]))
        muss = [c for c in controls if is_muss(c)]
        total += len(controls)
        total_muss += len(muss)
        muss_normal_sdt += sum(1 for c in muss if prop_value(c, "sec_level") == "normal-SdT")
        if muss:
            sections.append(render_muss_table(gid, title, slug, muss))

    lines = [
        "---\n",
        f"title: {yaml_quote('Für Geschäftsführung')}\n",
        f"description: {yaml_quote('Pflicht-Anforderungen, Einstufungskriterien und Haftungsrahmen auf einen Blick.')}\n",
        "---\n\n",
        GF_FILTER_IMPORT,
        "\n",
        "> Diese Seite ersetzt keine Rechts- oder Haftungsberatung. Sie ordnet "
        "öffentliche Quellen ein (den BSI-Katalog und geltendes Gesetzesrecht) "
        "— eine Bewertung des Einzelfalls kann nur eine Rechtsanwältin, ein "
        "Rechtsanwalt oder eine Wirtschaftsprüfung vornehmen.\n\n",
        f"## Auf einen Blick\n\n"
        f"**{total_muss} von {total} Anforderungen im gesamten Katalog sind "
        f"MUSS** — uneingeschränkt zu erfüllen, unabhängig vom individuellen "
        f"Risikoappetit (RFC2119 / DIN 820-2:2022, Anhang H). Das ist die "
        f"Teilmenge, die aus Governance-Sicht zuerst zählt.\n\n",
        # Umlaute im Titel wuerden vom Auto-Slugger prozentcodiert ("%C3%BC"),
        # deshalb explizite, transliterierte ID -- gleicher Grund wie bei
        # heading_anchor() fuer Controls und Gruppen. Muss hier im Generator
        # stehen: die Rollenseiten werden erzeugt, ein Anker direkt in der
        # .mdx waere beim naechsten Lauf wieder weg.
        "## Bin ich überhaupt betroffen? {#bin-ich-ueberhaupt-betroffen}\n\n"
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
        "## Was schreibt das Gesetz meiner Geschäftsleitung vor? {#was-schreibt-das-gesetz-vor}\n\n"
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
        f'<GfFilter mussTotal={{{total_muss}}} mussNormalSdt={{{muss_normal_sdt}}} />\n\n',
        "## Die MUSS-Anforderungen nach Bereich\n\n",
        *sections,
    ]
    ROLLEN_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (ROLLEN_OUT_DIR / "geschaeftsfuehrung.mdx").write_text("".join(lines))


def render_pdca_cycle_prop(management, groups_by_id):
    by_id = {gid: (title, slug) for gid, title, slug, _ in management}

    def node(gid):
        title, slug = by_id[gid]
        count = len(list(collect_controls(groups_by_id[gid])))
        return f"{{ id: {jsx_string(gid)}, title: {jsx_string(title)}, slug: {jsx_string(slug)}, count: {count} }}"

    # Reihenfolge des tatsächlichen PDCA-Ablaufs -- weicht von der
    # Katalog-Reihenfolge ab (dort steht VRB vor PERF), siehe PdcaCycle.astro.
    sequence = ["GC", "STM", "UMS", "PERF", "VRB"]
    nodes = "[" + ", ".join(node(gid) for gid in sequence) + "]"
    risk = node("RISK")
    return nodes, risk


def render_isb_page(management, groups_by_id):
    entries = []
    for gid, title, slug, summary in management:
        count = len(list(collect_controls(groups_by_id[gid])))
        entries.append((gid, title, slug, f"{summary} ({count} Anforderungen)"))

    nodes_prop, risk_prop = render_pdca_cycle_prop(management, groups_by_id)

    lines = [
        "---\ntitle: " + yaml_quote("Für ISB") + "\n---\n\n",
        PDCA_CYCLE_IMPORT,
        "\n",
        "Der BSI-OSCAL-Katalog (`Grundschutz++-resolved_catalog.json`, CC "
        "BY-SA 4.0, BSI-Bund) ist für Maschinen geschrieben – SSP-Generierung, "
        "Tooling, Validierung. OSCAL selbst stammt von NIST, nicht vom BSI: "
        "ein bereits etablierter, international genutzter Standard, den das "
        "BSI bewusst übernommen hat, statt eine eigene Lösung zu bauen.\n\n"
        "Diese Seite übersetzt denselben Katalog in etwas, das man als ISB im "
        "Tagesgeschäft tatsächlich liest — das Managementsystem als "
        "PDCA-Zyklus, mit Risikomanagement als durchgehendem Begleiter statt "
        "eigener Phase.\n\n",
        "## Der PDCA-Zyklus\n\n",
        f"<PdcaCycle nodes={{{nodes_prop}}} risk={{{risk_prop}}} />\n\n",
        render_index_section(
            "Die sechs Praktiken im Detail",
            "Dieselben sechs Praktiken als Liste, falls dir das lieber ist als der Kreis oben.",
            entries,
        ),
        "## Werkzeuge für den Alltag {#werkzeuge-fuer-den-alltag}\n\n"
        "- **[Vergleich: Altes Kompendium ↔ Grundschutz++](/vergleich/)** — "
        "jede Zuordnung zwischen alter und neuer Anforderung, mit "
        "Beziehungstyp (entspricht/Teilbereich von/umfasst/überschneidet "
        "sich mit) und echten Links zu BSI's Baustein-PDFs.\n"
        "- **Basisgefährdungen direkt am Control** — jede Anforderung zeigt "
        "die zugeordneten elementaren Gefährdungen (BSI, 47 Stück) als "
        "hoverbare Pille, ohne extra Nachschlagen in `basethreats.csv`.\n"
        "- **[Status & Zeitplan](/grundschutzpp/zeitplan/)** — Pilotphase, "
        "Übergangsfrist, geplante Zertifizierung.\n\n"
        "Diese Seite ist kein offizielles BSI-Angebot.\n",
    ]
    ROLLEN_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (ROLLEN_OUT_DIR / "isb.mdx").write_text("".join(lines))


# Redaktionelle Zweiteilung der 14 operativen Themenfelder (keine
# BSI-eigene Kategorie -- deshalb auf der Seite selbst als Einordnung
# gekennzeichnet, nicht als Katalog-Fakt). Kriterium: setzt ein Dev/eine
# Dev-nahe Rolle das direkt um (Code, Config, Systeme), oder ist es
# Prozess/Personal/Einkauf/Gebäude, das einen Dev nur indirekt betrifft.
# ASST ist ein Grenzfall -- Datenklassifizierung wirkt sich direkt auf den
# Umgang mit Daten im Code aus, daher hier bei "technisch" einsortiert.
DEV_TECHNICAL_GROUPS = ["ARCH", "KONF", "DEV", "BER", "DET", "NOT", "REA", "TEST", "ASST"]
DEV_ORG_GROUPS = ["PERS", "BES", "DLS", "GEB", "SENS"]


def render_devs_page(themenfelder, groups_by_id):
    by_id = {gid: (title, slug, summary) for gid, title, slug, summary in themenfelder}

    def entries_for(group_ids):
        out = []
        for gid in group_ids:
            title, slug, summary = by_id[gid]
            count = len(list(collect_controls(groups_by_id[gid])))
            out.append((gid, title, slug, f"{summary} ({count} Anforderungen)"))
        return out

    lines = [
        "---\ntitle: " + yaml_quote("Für Devs") + "\n---\n\n",
        "Jede Anforderung zeigt Pflichtgrad, Sicherheitsstufe, "
        "Aufwandsschätzung und zugeordnete Basisgefährdungen direkt am "
        "Text, als Badges mit Hover-Erklärung — keine ISMS-Prozess-"
        "Erklärung davor, kein Umweg über das Managementsystem.\n\n",
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
    (ROLLEN_OUT_DIR / "devs.mdx").write_text("".join(lines))


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


def group_mappings_by_baustein(all_mappings):
    """Zuordnungen nach altem Baustein buendeln — die Einheit, in der Leute suchen.

    Wer migriert, fragt "was wird aus OPS.1.1.5", nicht "was gehoert alles
    zu DET". Deshalb ist der alte Baustein die Seiteneinheit, nicht die
    neue Praktik.
    """
    by_baustein = {}
    for old_id, rel, new_id in all_mappings:
        baustein_id = baustein_id_from_itgs_id(old_id)
        if not baustein_id:
            continue
        by_baustein.setdefault(baustein_id, []).append((old_id, rel, new_id))
    return by_baustein


def render_baustein_page(baustein_id, entries, baustein_links, control_index):
    pdf = baustein_links.get(baustein_id)
    title = baustein_title(baustein_id, pdf)
    full_name = f"{baustein_id} {title}".strip()
    layer = KOMPENDIUM_LAYERS.get(baustein_id.split(".")[0], "")

    pdf_line = (
        f'Der Baustein selbst steht als <a href="{pdf}" target="_blank" '
        f'rel="noopener noreferrer">PDF beim BSI</a>.'
        if pdf
        else ""
    )

    lines = [
        "---\n",
        f"title: {yaml_quote(full_name)}\n",
        f"description: {yaml_quote(f'Welche Anforderungen aus {full_name} (IT-Grundschutz-Kompendium, Edition 2023) in welchen Grundschutz++-Controls aufgehen — je Zuordnung mit Beziehungstyp.')}\n",
        "---\n",
        "\n",
        f"Nachfolge-Zuordnungen für **{full_name}**"
        + (f" aus der Schicht {layer}" if layer else "")
        + f", {len(entries)} Stück aus der offiziellen BSI-Mapping-Datei. "
        "Der alte Anforderungstext wird hier bewusst nicht wiedergegeben "
        "(siehe [ADR-0005](https://github.com/grundschutz-docs/docs/blob/main/adr/0005-vorgaenger-anforderung-alt-neu.md)) — "
        + pdf_line
        + "\n",
        "\n",
        '<div class="vergleich-section not-content">\n',
        '<table class="vergleich-table">\n',
        "<thead><tr><th>Alte Anforderung</th><th>Beziehung</th><th>Neue Anforderung</th></tr></thead>\n",
        "<tbody>\n",
    ]
    for old_id, rel, new_id in sorted(entries, key=lambda e: (e[0], e[2])):
        old_cell = (
            f'<a class="old-id" href="{pdf}" target="_blank" rel="noopener noreferrer">{old_id}</a>'
            if pdf
            else f'<span class="old-id">{old_id}</span>'
        )
        lines.append(
            f"<tr><td>{old_cell}</td>"
            f'<td><span class="rel-badge" data-rel="{rel}">{relationship_label(rel)}</span></td>'
            f"<td>{control_link(new_id, control_index)}</td></tr>\n"
        )
    lines += [
        "</tbody>\n",
        "</table>\n",
        "</div>\n",
        "\n",
        "[Alle Bausteine im Überblick](/vergleich/)\n",
    ]
    return "".join(lines)


def render_vergleich_index(by_baustein, baustein_links):
    by_layer = {}
    for baustein_id, entries in by_baustein.items():
        by_layer.setdefault(baustein_id.split(".")[0], []).append((baustein_id, entries))

    lines = [
        "---\n",
        f"title: {yaml_quote('Vergleich: Altes Kompendium ↔ Grundschutz++')}\n",
        f"description: {yaml_quote('Zu jedem Baustein des IT-Grundschutz-Kompendiums (Edition 2023) die Nachfolge-Anforderungen im Grundschutz++-Katalog, nach offizieller BSI-Mapping-Datei.')}\n",
        "---\n",
        "\n",
        VERGLEICH_FILTER_IMPORT,
        "\n",
        "Zu jedem alten Baustein gibt es hier eine eigene Seite mit seinen "
        "Nachfolge-Anforderungen — aus der offiziellen BSI-Mapping-Datei "
        "(`ITGS-to-GS++-mapping_collection.json`), kein alter Volltext, nur "
        "Struktur und echte Links (siehe ADR-0005). Tippe eine bekannte "
        "Baustein-ID ins Suchfeld, z. B. `OPS.1.1.5`.\n",
        "\n",
        "<VergleichFilter />\n",
        "\n",
    ]
    for layer_id in sorted(by_layer, key=lambda lid: list(KOMPENDIUM_LAYERS).index(lid) if lid in KOMPENDIUM_LAYERS else 99):
        layer_name = KOMPENDIUM_LAYERS.get(layer_id, layer_id)
        lines += [
            '<div class="vergleich-section not-content">\n',
            f"## {layer_id} {layer_name}\n",
            "\n",
            '<table class="vergleich-table">\n',
            "<thead><tr><th>Baustein</th><th>Zuordnungen</th><th>Original</th></tr></thead>\n",
            "<tbody>\n",
        ]
        for baustein_id, entries in sorted(by_layer[layer_id]):
            pdf = baustein_links.get(baustein_id)
            title = baustein_title(baustein_id, pdf)
            pdf_cell = (
                f'<a href="{pdf}" target="_blank" rel="noopener noreferrer">PDF beim BSI</a>'
                if pdf
                else "—"
            )
            lines.append(
                f'<tr><td><a class="old-id" href="/vergleich/{baustein_slug(baustein_id)}/">{baustein_id}</a>'
                f' <span class="new-title">{title}</span></td>'
                f"<td>{len(entries)}</td><td>{pdf_cell}</td></tr>\n"
            )
        lines += ["</tbody>\n", "</table>\n", "</div>\n", "\n"]
    return "".join(lines)


def write_mdx(path, frontmatter, body):
    needs_control_meta = "<ControlMeta" in body
    prefix = CONTROL_META_IMPORT + "\n" if needs_control_meta else ""
    path.write_text(frontmatter + prefix + body)


def main():
    data = json.loads(CATALOG_FILE.read_text())
    catalog = data["catalog"]
    params_by_id = build_params_index(catalog)
    control_index = build_control_index(catalog)
    basethreats_by_id = load_basethreats()
    mapping_data = json.loads(MAPPING_FILE.read_text())
    predecessor_index = build_predecessor_index(mapping_data)
    baustein_links = json.loads(BAUSTEINE_LINKS_FILE.read_text())["bausteine"]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.mdx"):
        old.unlink()
    ROLLEN_OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in ROLLEN_OUT_DIR.glob("*.mdx"):
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
            basethreats_by_id=basethreats_by_id,
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
        write_mdx(OUT_DIR / f"{slug}.mdx", frontmatter, body)

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
    (OUT_DIR / "index.mdx").write_text("\n".join(index_lines))

    zeitplan_lines = [
        "---\ntitle: Status & Zeitplan\n---\n\n",
        "Grundschutz++ ersetzt das bisherige IT-Grundschutz-Kompendium nicht von "
        "heute auf morgen. Stand nach BSI-Fahrplan und Fachpublikationen "
        "(nicht offiziell von der BSI in jedem Detail bestätigt):\n",
        render_timeline(),
    ]
    (OUT_DIR / "zeitplan.mdx").write_text("\n".join(zeitplan_lines))

    # Vergleichsseiten: eine Uebersicht plus eine Seite je altem Baustein.
    # Frueher war das eine einzige Seite mit ~1200 Zeilen -- unbrauchbar
    # sowohl zum Lesen als auch zum Gefundenwerden, weil jede Suche nach
    # einer Baustein-ID gegen alle anderen auf derselben Seite konkurriert.
    all_mappings = build_all_mappings(mapping_data)
    by_baustein = group_mappings_by_baustein(all_mappings)

    legacy_vergleich = OUT_DIR.parent / "vergleich.mdx"
    if legacy_vergleich.exists():
        legacy_vergleich.unlink()
    VERGLEICH_OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in VERGLEICH_OUT_DIR.glob("*.mdx"):
        old.unlink()

    (VERGLEICH_OUT_DIR / "index.mdx").write_text(
        render_vergleich_index(by_baustein, baustein_links)
    )
    for baustein_id, entries in by_baustein.items():
        (VERGLEICH_OUT_DIR / f"{baustein_slug(baustein_id)}.mdx").write_text(
            render_baustein_page(baustein_id, entries, baustein_links, control_index)
        )

    stats = write_landing_data(
        catalog, control_index, by_baustein, all_mappings, params_by_id, baustein_links
    )


    # Rollenbasierte Einstiegsseiten (ADR-0007) -- aus denselben Gruppen-
    # Listen wie oben, keine eigene Zielgruppen-Einstufung im Katalog nötig.
    render_geschaeftsfuehrung_page(management, themenfelder, groups_by_id)
    render_isb_page(management, groups_by_id)
    render_devs_page(themenfelder, groups_by_id)

    # Ganz zum Schluss: die Pruefungen lesen die *fertig geschriebenen* Dateien
    # zurueck, also muessen alle Seiten vorher auf der Platte liegen.
    check_invariants(
        catalog,
        control_index,
        [c for c in collect_controls(catalog) if is_muss(c)],
        by_baustein,
    )

    total = len(management) + len(themenfelder)
    print(f"{total} Gruppen-Seiten (.mdx) erzeugt in {OUT_DIR}")
    print(f"3 Rollen-Seiten (.mdx) erzeugt in {ROLLEN_OUT_DIR}")
    print(f"{len(by_baustein)} Baustein-Seiten + Übersicht erzeugt in {VERGLEICH_OUT_DIR}")
    print(f"Startseiten-Daten: {stats}")

    def sidebar_group(label, entries):
        items = ",\n\t\t\t\t\t\t".join(
            f'{{ label: "{gid} {title}", slug: "grundschutzpp/{slug}" }}' for gid, title, slug, _ in entries
        )
        return f'{{\n\t\t\t\t\tlabel: "{label}",\n\t\t\t\t\titems: [\n\t\t\t\t\t\t{items},\n\t\t\t\t\t],\n\t\t\t\t}}'

    print("\nastro.config.mjs Sidebar-Snippet (manuell einfügen falls gewünscht):\n")
    print(sidebar_group("Managementsystem", management) + ",\n" + sidebar_group("Themenfelder", themenfelder))


if __name__ == "__main__":
    main()
