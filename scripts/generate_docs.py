#!/usr/bin/env python3
"""
Liest den Grundschutz++-resolved_catalog.json (OSCAL) und generiert daraus
lesbare Markdown-Seiten fuer Starlight.

Erneut ausfuehren nach jedem `git pull` im Grundschutz-PlusPlus-Repo, um die
Doku-Seite auf den aktuellen Stand zu bringen:

    cd Grundschutz-PlusPlus && git pull
    python3 ../Grundschutz-Docs/scripts/generate_docs.py
    cd ../Grundschutz-Docs && npm run build   # oder: npm run dev
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CATALOG_FILE = REPO_ROOT / "Grundschutz-PlusPlus" / "control_layer" / "Grundschutz++" / "Grundschutz++-resolved_catalog.json"
OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "grundschutzpp"
ASTRO_CONFIG = Path(__file__).resolve().parent.parent / "astro.config.mjs"

PARAM_RE = re.compile(r"\{\{\s*insert:\s*param,\s*([a-zA-Z0-9._-]+)\s*\}\}")


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


def render_group(group, level, params_by_id):
    heading = "#" * min(level, 6)
    lines = [f"{heading} {group['id']} {group['title']}\n"]

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


def main():
    data = json.loads(CATALOG_FILE.read_text())
    catalog = data["catalog"]
    params_by_id = build_params_index(catalog)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()

    sidebar_items = []
    for group in catalog["groups"]:
        slug = group["id"].lower()
        body = render_group(group, level=1, params_by_id=params_by_id)
        frontmatter = (
            "---\n"
            f"title: \"{group['id']} – {group['title']}\"\n"
            "---\n\n"
        )
        (OUT_DIR / f"{slug}.md").write_text(frontmatter + body)
        sidebar_items.append((group["id"], group["title"], slug))

    index_lines = ["---\ntitle: Grundschutz++ Kompendium\n---\n\n",
                   "Automatisch generiert aus dem OSCAL-Katalog. "
                   "Nicht Teil des offiziellen BSI-Materials — eigene lesbare Aufbereitung.\n\n"]
    for gid, title, slug in sidebar_items:
        index_lines.append(f"- [{gid} {title}](/grundschutzpp/{slug}/)\n")
    (OUT_DIR / "index.md").write_text("".join(index_lines))

    print(f"{len(sidebar_items)} Gruppen-Seiten erzeugt in {OUT_DIR}")

    sidebar_js = ",\n\t\t\t\t\t".join(
        f'{{ label: "{gid} {title}", slug: "grundschutzpp/{slug}" }}'
        for gid, title, slug in sidebar_items
    )
    print("\nastro.config.mjs Sidebar-Snippet (manuell einfügen falls gewünscht):\n")
    print(sidebar_js)


if __name__ == "__main__":
    main()
