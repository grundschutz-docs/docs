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
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CATALOG_FILE = REPO_ROOT / "Grundschutz-PlusPlus" / "control_layer" / "Grundschutz++" / "Grundschutz++-resolved_catalog.json"
OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "grundschutzpp"
ASTRO_CONFIG = Path(__file__).resolve().parent.parent / "astro.config.mjs"

PARAM_RE = re.compile(r"\{\{\s*insert:\s*param,\s*([a-zA-Z0-9._-]+)\s*\}\}")

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


def render_control(control, level, params_by_id):
    heading = "#" * min(level, 6)
    lines = [f"{heading} {control['id']} – {control['title']}\n"]

    sec_level = prop_value(control, "sec_level")
    effort = prop_value(control, "effort_level")
    threats = prop_value(control, "threats")
    badges = []
    if sec_level:
        badges.append(f"**Stufe:** `{sec_level}`")
    if effort:
        badges.append(f"**Aufwand:** {effort}")
    if threats:
        badges.append(f"**Gefährdungen:** {threats}")
    if badges:
        lines.append(" · ".join(badges) + "\n")

    statement = substitute_params(part_text(control, "statement"), params_by_id)
    if statement:
        lines.append(f"> {statement}\n")

    guidance = substitute_params(part_text(control, "guidance"), params_by_id)
    if guidance:
        lines.append(f"{guidance}\n")

    for sub in control.get("controls", []):
        lines.append(render_control(sub, level + 1, params_by_id))

    return "\n".join(lines)


def render_group(group, level, params_by_id, include_heading=True):
    lines = []
    if include_heading:
        heading = "#" * min(level, 6)
        lines.append(f"{heading} {group['id']} {group['title']}\n")

    desc = group_description(group)
    if desc:
        lines.append(f"{desc}\n")

    for control in group.get("controls", []):
        lines.append(render_control(control, level + 1, params_by_id))

    for sub in group.get("groups", []):
        lines.append(render_group(sub, level + 1, params_by_id))

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


def first_sentence(text):
    if not text:
        return ""
    match = re.search(r"(.+?[.!?])(\s|$)", text)
    return match.group(1) if match else text


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

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()

    management, themenfelder = [], []
    for group in catalog["groups"]:
        slug = group["id"].lower()
        # include_heading=False: Starlight rendert die Seiten-Überschrift bereits
        # automatisch aus der Frontmatter — sonst stünde sie doppelt auf der Seite.
        body = render_group(group, level=1, params_by_id=params_by_id, include_heading=False)
        frontmatter = (
            "---\n"
            f"title: \"{group['id']} – {group['title']}\"\n"
            "---\n\n"
        )
        (OUT_DIR / f"{slug}.md").write_text(frontmatter + body)

        entry = (group["id"], group["title"], slug, first_sentence(group_description(group)))
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

    total = len(management) + len(themenfelder)
    print(f"{total} Gruppen-Seiten erzeugt in {OUT_DIR}")

    def sidebar_group(label, entries):
        items = ",\n\t\t\t\t\t\t".join(
            f'{{ label: "{gid} {title}", slug: "grundschutzpp/{slug}" }}' for gid, title, slug, _ in entries
        )
        return f'{{\n\t\t\t\t\tlabel: "{label}",\n\t\t\t\t\titems: [\n\t\t\t\t\t\t{items},\n\t\t\t\t\t],\n\t\t\t\t}}'

    print("\nastro.config.mjs Sidebar-Snippet (manuell einfügen falls gewünscht):\n")
    print(sidebar_group("Managementsystem", management) + ",\n" + sidebar_group("Themenfelder", themenfelder))


if __name__ == "__main__":
    main()
