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
import difflib
import functools
import json
import os
import re
import subprocess
import sys
import urllib.parse
from collections import Counter
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CATALOG_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "control_layer" / "Grundschutz++" / "Grundschutz++-resolved_catalog.json"
)
DEFAULT_BASETHREATS_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "documentation" / "namespaces" / "basethreats.csv"
)
DEFAULT_TAGS_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "documentation" / "namespaces" / "tags.csv"
)
# Lokal: Grundschutz-PlusPlus liegt als Ordner neben diesem Repo. In CI gibt es
# diesen Nachbarordner nicht — dort wird der Pfad stattdessen über die Umgebungsvariable
# gesetzt (siehe .github/workflows/sync-catalog.yml im OSS-Repo).
CATALOG_FILE = Path(os.environ["GRUNDSCHUTZPP_CATALOG"]) if os.environ.get("GRUNDSCHUTZPP_CATALOG") else DEFAULT_CATALOG_FILE
BASETHREATS_FILE = (
    Path(os.environ["GRUNDSCHUTZPP_BASETHREATS"]) if os.environ.get("GRUNDSCHUTZPP_BASETHREATS") else DEFAULT_BASETHREATS_FILE
)
TAGS_FILE = Path(os.environ["GRUNDSCHUTZPP_TAGS"]) if os.environ.get("GRUNDSCHUTZPP_TAGS") else DEFAULT_TAGS_FILE
DEFAULT_TARGETS_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "documentation" / "namespaces" / "target_object_categories.csv"
)
TARGETS_FILE = (
    Path(os.environ["GRUNDSCHUTZPP_TARGETS"]) if os.environ.get("GRUNDSCHUTZPP_TARGETS") else DEFAULT_TARGETS_FILE
)
DEFAULT_MAPPING_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "control_layer" / "Mappings" / "IT-GS2023-zu-GSpp" / "ITGS-to-GS++-mapping_collection.json"
)
MAPPING_FILE = Path(os.environ["GRUNDSCHUTZPP_MAPPING"]) if os.environ.get("GRUNDSCHUTZPP_MAPPING") else DEFAULT_MAPPING_FILE
# data/bsi-kompendium-2023-bausteine.json: eigene, einmal von BSIs
# Bausteine-Uebersichtsseite gescrapte Lookup-Tabelle (Baustein-ID -> PDF-URL),
# siehe adr/0005-vorgaenger-anforderung-alt-neu.md. Lag frueher bewusst ausserhalb
# beider Repos ("externe Referenzdaten") -- das scheiterte am ersten echten
# CI-Lauf von sync-catalog.yml, der nur je Checkout, nicht auf die lokale
# Festplatte des Maintainers zugreifen kann. Jetzt Teil dieses Repos, siehe
# commit message fuer die Umstellung.
DEFAULT_BAUSTEINE_LINKS_FILE = Path(__file__).resolve().parent.parent / "data" / "bsi-kompendium-2023-bausteine.json"
BAUSTEINE_LINKS_FILE = (
    Path(os.environ["BSI_BAUSTEINE_LINKS"]) if os.environ.get("BSI_BAUSTEINE_LINKS") else DEFAULT_BAUSTEINE_LINKS_FILE
)
OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "grundschutzpp"
# Rollen-Seiten (ADR-0007) liegen wie vergleich.mdx eine Ebene flacher als
# die Gruppen-Seiten, aber in einem eigenen Unterordner (eigene Sidebar-Gruppe).
ROLLEN_OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "rollen"
VERGLEICH_OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "vergleich"
ZIELOBJEKTE_OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "zielobjekte"
DOKUMENTE_OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs" / "dokumente"
DATA_OUT_DIR = Path(__file__).resolve().parent.parent / "src" / "data"
CONTROL_META_IMPORT = "import ControlMeta from '../../../components/ControlMeta.astro';\n"
# vergleich.mdx liegt eine Ebene flacher (direkt in src/content/docs/), daher
# ein "../" weniger als CONTROL_META_IMPORT.
# Drei Ebenen hoch: src/content/docs/vergleich/index.mdx -> src/components/
VERGLEICH_FILTER_IMPORT = "import VergleichFilter from '../../../components/VergleichFilter.astro';\n"
# rollen/*.mdx liegt auf derselben Tiefe wie grundschutzpp/*.mdx (nicht wie
# vergleich.mdx), daher derselbe "../../../"-Pfad wie CONTROL_META_IMPORT.
PDCA_CYCLE_IMPORT = "import PdcaCycle from '../../../components/PdcaCycle.astro';\n"

PARAM_RE = re.compile(r"\{\{\s*insert:\s*param,\s*([a-zA-Z0-9._-]+)\s*\}\}")

# Zeitplan nach dem Meilensteinplan des BSI ("Meilensteinplan (Stand Oktober
# 2026)" auf BSI_MEILENSTEINE_URL), die it-sa-Daten zusaetzlich nach BSIs
# it-sa-Seite. Geprueft am 2026-10-18 gegen den Rohtext beider Seiten.
#
# Nur Termine, die das BSI selbst nennt. Frueher standen hier "Uebergangsphase
# 04/2026 - 12/2029" und "Ablösung ab 01/2029" aus Fachpublikationen -- beide
# Daten stehen beim BSI nicht (es nennt die Uebergangszeit nur "mehrjaehrig",
# ohne Enddatum), und die 12/2029 stand als Banner ueber jeder Seite. Das BSI
# passt den Plan laufend an: vor jeder Aenderung hier die Quelle neu lesen
# und BSI_MEILENSTEINE_STAND setzen.
#     (start, end, label_de, detail_de, label_en, detail_en, range_text, banner)
#
# range_text ersetzt die aus start/end berechnete Anzeige (z. B. wenn das BSI
# nur "1. Quartal 2027" nennt oder die Uebergangszeit kein Enddatum hat).
# start/end steuern dann nur "laeuft" und den Banner. banner=False: Meilensteine,
# die nicht als "Grundschutz++ ist in ..." im Banner stehen sollen.
#
# English fields only back the sitewide Banner.astro status strip (shown on
# /en/ pages too) -- the zeitplan page itself (render_timeline()) stays
# German-only like the rest of the catalog. Keeping the translation right
# next to the German text it belongs to is what stops it from drifting out
# of sync the way the banner's old hand-written text once did (see
# write_status_data()'s docstring).
#
# Reihenfolge = Anzeigereihenfolge. Bei gleich langen laufenden Phasen gewinnt
# im Banner der spaetere Eintrag, darum steht die Uebergangszeit (Auffang
# fuer alle Luecken, ohne Enddatum) ganz am Ende.
BSI_MEILENSTEINE_URL = (
    "https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/"
    "Standards-und-Zertifizierung/Grundschutz-in-der-Informationssicherheit/"
    "Grundschutz-Plus-Plus/grundschutz-plus-plus_node.html"
)
BSI_MEILENSTEINE_STAND = "30.10.2026"
TIMELINE = [
    (
        date(2026, 4, 1), date(2026, 8, 31),
        "Pilotierungsphase", "Pilotpartner aus Verwaltung und Wirtschaft erproben die Methodik.",
        "pilot phase", "Pilot partners from public administration and industry are testing the methodology.",
        None, True,
    ),
    (
        date(2026, 9, 1), date(2026, 10, 26),
        "Weiterentwicklung nach der Pilotierung",
        "Die Methodik war zur Veröffentlichung auf der it-sa am 27.10.2026 vorgesehen. Die Erkenntnisse aus der Erprobung flossen in sie ein.",
        "post-pilot refinement phase",
        "The methodology was due to be published at it-sa on 27 October 2026. Findings from the pilot fed into it.",
        None, True,
    ),
    (
        date(2026, 10, 27), date(2026, 10, 29),
        "Veröffentlichungswoche der Methodik auf der it-sa",
        "Das BSI hat die Methodik am 26.10.2026 als BSI-Standard 300-1 veröffentlicht und sie auf der it-sa 2026 in Nürnberg vorgestellt.",
        "launch week at it-sa",
        "The BSI published the methodology as BSI Standard 300-1 on 26 October 2026 and presented it at it-sa 2026 in Nuremberg.",
        None, True,
    ),
    (
        # Schliesst die Luecke zwischen dem Ende der it-sa-Phase (29.10.) und dem Beginn der
        # Early-Adopter-Phase (01.01.2027), in der der Banner sonst auf den Auffang-Eintrag
        # "Uebergangszeit" sprang. Der Beginn am 30.10. ist kein BSI-Datum, sondern der Tag
        # nach der it-sa; die Bezeichnung beschreibt, sie ist kein Begriff des BSI.
        date(2026, 10, 30), date(2026, 12, 31),
        "Phase nach der Veröffentlichung von BSI-Standard 300-1",
        "Das BSI hat die Methodik am 26.10.2026 als BSI-Standard 300-1 veröffentlicht. Schulungskonzepte und ein Anwendungsbeispiel sollen bis Dezember 2026 folgen.",
        "phase after the publication of BSI Standard 300-1",
        "The BSI published the methodology as BSI Standard 300-1 on 26 October 2026. Training concepts and a worked example are planned for 30 November and December 2026.",
        None, True,
    ),
    (
        date(2026, 11, 30), date(2026, 12, 31),
        "Schulungskonzepte und Anwendungsbeispiel",
        "Zum 30.11.2026 sollen Schulungskonzepte für GS++-Praktiker und -Berater erscheinen, im Dezember 2026 ein Anwendungsbeispiel anhand der fiktiven Beispielbehörde „BDIT“.",
        "training concepts and worked example", "Planned by the BSI for 30 November and December 2026.",
        "30.11. / 12.2026", False,
    ),
    (
        date(2027, 1, 1), None,
        "Zertifizierbar",
        "Zertifizierungsanträge nach ISO 27001 auf Basis von Grundschutz++ können gestellt werden, ebenso für die Zertifizierung zum GS++-Berater und -Auditteamleiter.",
        "certifiable", "Certification applications under ISO 27001 based on Grundschutz++ can be submitted.",
        "ab 01.01.2027", False,
    ),
    (
        date(2027, 1, 1), date(2027, 12, 31),
        "Early-Adopter-Phase",
        "Anwender setzen die erste anwendbare Version der Methodik ein. Im 1. Quartal startet außerdem die Fortbildung zum GS++-Berater und -Auditteamleiter für bereits zertifizierte Personen.",
        "early-adopter phase", "Early adopters apply the first usable version of the methodology.",
        "1. Quartal – 12/2027", True,
    ),
    (
        date(2027, 2, 26), date(2027, 3, 31),
        "Leistungsmessung",
        "Ab 26.02.2027 ist das Konzept zur Leistungsmessung des ISMS in der Methodik, bis 31.03.2027 sollen alle Anforderungen der ISMS-Praktiken Leistungskennzahlen haben.",
        "performance measurement", "Performance measurement concept and indicators are due.",
        "26.02. – 31.03.2027", False,
    ),
    (
        date(2031, 11, 30), date(2031, 11, 30),
        "Ende der Zertifizierbarkeit nach bisherigem IT-Grundschutz",
        "Fünf Jahre nach Veröffentlichung von Grundschutz++. Ein Enddatum für die Übergangszeit selbst nennt das BSI nicht.",
        "end of certification under the previous IT-Grundschutz", "Five years after the publication of Grundschutz++.",
        "30.11.2031", False,
    ),
    (
        # start nur fuer den Banner (Auffang fuer alle Luecken zwischen den
        # Phasen oben); angezeigt wird range_text, denn das BSI nennt weder
        # Beginn noch Ende.
        date(2026, 4, 1), None,
        "Übergangszeit", "Der bisherige IT-Grundschutz bleibt laut BSI anwendbar.",
        "transition period", "The previous IT-Grundschutz remains applicable, according to the BSI.",
        "mehrjährig, Ende nicht festgelegt", True,
    ),
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


def pagefind_section(label):
    # Kein Text, der irgendwem fehlt oder vorgelesen werden muesste -- ein
    # leeres Element, das nur den data-pagefind-meta-Schluessel traegt. Macht
    # den Seitentyp (Anforderung/Vergleich/Rolle/Befund) im Suchergebnis
    # unterscheidbar, ohne dass man erst draufklicken muesste. Siehe
    # Search.astro, Template-Zweig fuer meta.section.
    return f'<span data-pagefind-meta="section:{label}"></span>\n\n'


def load_basethreats():
    with BASETHREATS_FILE.open(newline="", encoding="utf-8") as f:
        return {row["ID"]: row["Begriff"] for row in csv.DictReader(f)}


def threats_hint(threats, basethreats_by_id):
    ids = [t.strip() for t in threats.split(",") if t.strip()]
    labeled = [f"{tid} – {basethreats_by_id[tid]}" for tid in ids if tid in basethreats_by_id]
    return " · ".join(labeled) if labeled else None


def load_tags():
    with TAGS_FILE.open(newline="", encoding="utf-8") as f:
        return {row["Tag"]: row["Bedeutung"] for row in csv.DictReader(f)}


# Zielobjektkategorien (ZOK) aus der CSV des BSI: Name -> Definition, Beispiele,
# Elternkategorie, Synonyme. Wie BAUSTEIN_TITLES einmal in main() befuellt, damit
# die Zielobjekte nicht durch render_group/render_control/render_control_meta
# gereicht werden muessen. Die Zuordnung zur Anforderung steht im Katalog selbst
# (statement-Prop "target_object_categories", bei 636 von 1000 Anforderungen);
# die CSV liefert nur die Erklaerung dazu.
TARGETS = {}


def load_targets():
    with TARGETS_FILE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    name_by_uuid = {row["UUID"]: row["Zielobjekt"] for row in rows}
    return {
        row["Zielobjekt"]: {
            "definition": row["Definition"].strip(),
            "example": row["Beispiel"].strip(),
            "parent": name_by_uuid.get(row["ChildOfUUID"]),
            "synonyms": row["Synonyme"].strip(),
        }
        for row in rows
    }


def control_targets(control):
    value = part_prop_value(control, "statement", "target_object_categories")
    return [t.strip() for t in value.split(",") if t.strip()] if value else []


def target_hint(name):
    # Erster Satz der Definition, dann Beispiele und die Elternkategorie: die
    # volle Definition ist bei "Anwendungen" ueber 400 Zeichen -- zu lang fuer
    # einen Tooltip, und die Pille soll erklaeren, nicht die Seite sprengen.
    info = TARGETS.get(name)
    if not info:
        return None
    parts = [first_sentence(info["definition"])]
    if info["example"]:
        parts.append(f"Beispiele: {info['example']}.")
    if info["parent"]:
        parts.append(f"Teil von: {info['parent']}.")
    return " ".join(p for p in parts if p)


def inherited_targets(control):
    """Kategorien unterhalb der direkt zugeordneten (STM.2.1.4.1), ohne diese selbst.
    Nur fuer die unsichtbaren Suchfilter-Marken: ein Pagefind-Filter hing sonst nur an
    der direkten Angabe, "Webserver" fand 6 statt 87 Anforderungen."""
    direkt = set(control_targets(control))
    descendants = export_target_descendants()
    return sorted({d for t in direkt for d in descendants.get(t, [])} - direkt)


def render_targets_prop(control):
    # Eigenes Array wie bei tags: jede Kategorie bekommt ihre eigene Pille und
    # ihren eigenen Pagefind-Filterwert.
    names = control_targets(control)
    if not names:
        return None
    items = []
    for name in names:
        obj = f"{{ name: {jsx_string(name)}, slug: {jsx_string(tag_slug(name))}"
        hint = target_hint(name)
        if hint:
            obj += f", hint: {jsx_string(hint)}"
        synonyms = (TARGETS.get(name) or {}).get("synonyms")
        if synonyms:
            obj += f", synonyms: {jsx_string(synonyms)}"
        obj += " }"
        items.append(obj)
    return "[" + ", ".join(items) + "]"


# Handkuratiert, nicht alle ~50 vergebenen Tags: deckt die Begriffe ab, bei
# denen die Alltags-/Geschaeftssprache nachweislich von der Katalog-Formulierung
# abweicht (siehe Pagefind-Suchtest 2026-10-01 -- "was muss ich fuer
# Lieferanten beachten" fand trotz 125 zugeordneter Anforderungen zum Tag
# "Lieferketten" null Treffer). Recherchiert gegen BSI-eigene NIS-2-Papiere
# und etablierte Fachbegriffe, nicht geraten. "Physical Access Control" hat
# bewusst nur "Zutrittskontrolle", nicht "Zugangskontrolle" -- das bezeichnet
# im Deutschen (und in der DSGVO-Terminologie) digitalen, nicht physischen
# Zugang; eine Vermischung wuerde Treffer in die falsche Richtung ziehen.
TAG_SYNONYMS = {
    "Lieferketten": "Lieferanten, Zulieferer, Dienstleister, Supply Chain",
    "Hochverfügbarkeit": "Ausfallsicherheit, Redundanz",
    "Password Policy": "Passwortrichtlinie, Passwortregeln",
    "Insider Threat": "interne Bedrohung, Innentäter",
    "Bring Your Own Device": "BYOD, private Geräte, eigene Geräte",
    "Compliance-Management": "Regelkonformität, Vorschrifteneinhaltung",
    "Physical Access Control": "Zutrittskontrolle, Gebäudesicherheit",
    "Advanced Persistent Threats (APT)": "gezielter Angriff, staatlich gesteuerter Angreifer",
    "Exit-Strategie": "Anbieterwechsel, Vendor Lock-in, Vertragsende Dienstleister",
    "Kompetenzmanagement": "Schulung, Weiterbildung, Qualifikation",
}


def tag_slug(name):
    """Anker-ID eines Themen-Tags auf /grundschutzpp/themen/ ("Password Policy" -> "password-policy").

    Umlaute ausgeschrieben statt verworfen, sonst wuerde "Hochverfügbarkeit"
    zu "hochverf-gbarkeit" und die Anker waeren schwer zu lesen.
    """
    text = name.lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def render_tags_prop(control, tags_by_id):
    # Eigenes Array statt eines einzelnen String-Props wie bei "threats": jedes
    # Tag braucht seinen eigenen data-pagefind-filter-Wert (eine Pagefind-
    # Filter-Facette je Element, kein kommagetrennter Wert in einem Attribut),
    # und damit auch seine eigene Pille mit eigenem Tooltip statt einem
    # gemeinsamen, zusammengewuerfelten Hint-Text.
    value = prop_value(control, "tags")
    if not value:
        return None
    names = [t.strip() for t in value.split(",") if t.strip()]
    if not names:
        return None
    items = []
    for name in names:
        obj = f"{{ name: {jsx_string(name)}, slug: {jsx_string(tag_slug(name))}"
        hint = tags_by_id.get(name)
        if hint:
            obj += f", hint: {jsx_string(hint)}"
        synonyms = TAG_SYNONYMS.get(name)
        if synonyms:
            obj += f", synonyms: {jsx_string(synonyms)}"
        obj += " }"
        items.append(obj)
    return "[" + ", ".join(items) + "]"


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


# Offizielle Titel aus data/bsi-kompendium-2023-bausteine.json ("titel"),
# von main() gefuellt. Vorrang vor der Ableitung aus dem Dateinamen: die ist
# ASCII-transliteriert (Gebaeude, Speicherloesungen), verliert Bindestriche
# (DNS Server, WLAN Betrieb) und haengt teils "2023" an -- bei 49 von 111
# Bausteinen wich das vom Titel auf BSIs eigener Seite ab.
BAUSTEIN_TITLES = {}


def baustein_title(baustein_id, url):
    """Offizieller Baustein-Titel; Notnagel: aus dem BSI-PDF-Dateinamen ableiten.

    Die Ableitung unten ist nur noch der Fallback fuer einen Baustein ohne
    Eintrag in "titel" (main() bricht in dem Fall ohnehin ab).

    bsi-kompendium-2023-bausteine.json enthaelt nur ID -> PDF-URL, aber der
    Dateiname traegt den Titel mit ("OPS_1_1_5_Protokollierung_Edition_2023
    .pdf" -> "Protokollierung"). Fuer alle 111 Bausteine geprueft.

    Bekannte Grenze: Bindestriche zusammengesetzter Titel gehen im
    Dateinamen verloren. "Netzarchitektur und -design" laesst sich aus dem
    folgenden Kleinbuchstaben rekonstruieren, "Prozessleit- und
    Automatisierungstechnik" nicht -- dort haengt der Bindestrich am ersten
    Wort und ist spurlos weg.
    """
    if baustein_id in BAUSTEIN_TITLES:
        return BAUSTEIN_TITLES[baustein_id]
    if not url:
        return ""
    name = urllib.parse.urlparse(url).path.rsplit("/", 1)[-1]
    # "Editi?on": BSI hat einen Teil der eigenen PDF-Dateinamen als
    # "..._Editon_2023.pdf" hochgeladen (ohne das zweite i) -- die echte Datei
    # heisst wirklich so, nicht nur der Link ist vertippt (ORP.2/3/4/5
    # geprueft: "Edition" liefert 404, "Editon" das PDF). Ohne das "i?" bleibt
    # "_Editon_2023" im Titel stehen, weil es nicht mehr matcht.
    name = re.sub(r"(?:_Editi?on_\d{4})?\.pdf$", "", name)
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

# Ueberschriften der Rollenseiten mit Umlauten brauchen eine explizite,
# transliterierte Anker-ID -- der Auto-Slugger wuerde "%C3%BC" erzeugen. Als
# Liste statt als verstreute Literale, damit Pruefung 8 sie gegen die
# geschriebenen Dateien halten kann.
ROLLEN_ANKER = {
    "geschaeftsfuehrung.mdx": ("bin-ich-ueberhaupt-betroffen", "was-schreibt-das-gesetz-vor"),
    "isb.mdx": ("werkzeuge-fuer-den-alltag",),
}


# Meta-Descriptions der Praktik-Seiten, die wir bewusst kuerzen. Der Katalogtext
# ist 213-284 Zeichen lang; Suchergebnisse schneiden bei etwa 155-160 ab, bevor
# der Zweck der Praktik kommt (2026-10-14). Die Seiten werden erzeugt, und der
# taegliche Workflow sync-catalog.yml laeuft den Generator erneut -- eine von
# Hand in der .mdx gekuerzte Beschreibung waere beim naechsten Lauf wieder weg.
#
# "original" ist der Katalogtext, den wir ersetzen. Weicht der Katalog spaeter
# davon ab (das BSI aendert die Beschreibung), meldet der Generator das, statt
# unseren Text stillschweigend ueber die neue Fassung zu legen. Die Override
# gilt nur fuer die Meta-Description, nicht fuer die Praktik-Listen auf den
# Uebersichts- und Rollenseiten.
DESCRIPTION_OVERRIDES = {
    "KONF": {
        "original": "Die Praktik Konfiguration stellt sicher, dass IT-Komponenten – wie Anwendungen und IT-Systeme – gemäß den festgelegten Informationssicherheitsrichtlinien eingerichtet und kontinuierlich gepflegt werden, um Sicherheitslücken durch fehlerhafte oder unsichere Einstellungen zu vermeiden.",
        "text": "Praktik Konfiguration: IT-Komponenten gemäß Sicherheitsrichtlinien einrichten und pflegen, um Lücken durch unsichere Einstellungen zu vermeiden.",
    },
    "TEST": {
        "original": "Die Praktik \"Änderungen und Tests\" stellt sicher, dass alle geplanten Veränderungen an Informationssystemen systematisch und kontrolliert ablaufen, um ungewollte Störungen, Sicherheitsrisiken oder Compliance-Verstöße zu vermeiden (Change Management).",
        "text": "Praktik Änderungen und Tests: geplante Änderungen an Informationssystemen kontrolliert umsetzen (Change Management), ohne Störungen und Risiken.",
    },
    "REA": {
        "original": "Die Praktik Sicherheitsvorfallsbehandlung sorgt dafür, dass Informationssicherheitsvorfälle effizient erkannt, gemeldet, analysiert und behoben werden, um Schäden zu minimieren und den Normalbetrieb so schnell wie möglich wiederherzustellen.",
        "text": "Praktik Sicherheitsvorfallsbehandlung: Vorfälle effizient erkennen, melden, analysieren und beheben, um Schäden gering zu halten.",
    },
    "RISK": {
        "original": "Risikomanagement ist ein systematischer, wiederkehrender Zyklus, mit dem Ziel, Risiken für die Vertraulichkeit, Integrität und Verfügbarkeit von Informationen zu identifizieren, zu bewerten, zu steuern und kontinuierlich zu überwachen.",
        "text": "Risikomanagement als wiederkehrender Zyklus: Risiken für Vertraulichkeit, Integrität und Verfügbarkeit erkennen, bewerten, steuern und überwachen.",
    },
    "NOT": {
        "original": "Die Notfallplanung stellt sicher, dass bei schwerwiegenden Störungen oder Krisen schnell und koordiniert reagiert wird, um den Fortbestand kritischer Geschäftsprozesse und die Wiederherstellung der betroffenen Systeme zu gewährleisten.",
        "text": "Notfallplanung: bei schweren Störungen schnell und koordiniert reagieren, kritische Geschäftsprozesse sichern und Systeme wiederherstellen.",
    },
    "PERF": {
        "original": "Die Praktik Monitoring-Evaluation stellt durch kontinuierliche Überwachung und systematische Bewertung sicher, dass die implementierten Sicherheitsmaßnahmen wirksam sind und die Sicherheitsziele der Organisation erreicht werden.",
        "text": "Praktik Monitoring-Evaluation: durch laufende Überwachung und Bewertung prüfen, ob Sicherheitsmaßnahmen wirken und Ziele erreicht werden.",
    },
    "ARCH": {
        "original": "Die Praktik Architektur definiert die grundlegende Struktur sowie die Sicherheitsprinzipien der IT-Infrastruktur und leitet daraus Anforderungen für einzelne IT-Komponenten ab – etwa für Anwendungen oder IT-Systeme.",
        "text": "Praktik Architektur: Struktur und Sicherheitsprinzipien der IT-Infrastruktur festlegen und daraus Anforderungen für IT-Komponenten ableiten.",
    },
    "UMS": {
        "original": "Die Praktik Umsetzung sorgt für die systematische Planung, Implementierung und Dokumentation von Anforderungen bzw. der Sicherheitsmaßnahmen, die aus der Strukturmodellierung und Risikobewertung abgeleitet wurden.",
        "text": "Praktik Umsetzung: Anforderungen und Sicherheitsmaßnahmen aus Strukturmodellierung und Risikobewertung planen, umsetzen und dokumentieren.",
    },
}


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


def write_bausteine_data(by_baustein, baustein_links):
    """ID, Titel und Seite der Bausteine mit Vergleichsseite fuer die Suche.

    Search.astro springt damit bei einer eingetippten alten Baustein-ID
    direkt auf die Vergleichsseite. Pagefind allein trifft "inf 2" oder
    "OPS 1.1.5" nicht zuverlaessig, weil es an Leerzeichen und Punkten in
    Woerter zerlegt.
    """
    data = [
        {
            "id": baustein_id,
            "title": baustein_title(baustein_id, baustein_links.get(baustein_id)),
            "slug": baustein_slug(baustein_id),
        }
        for baustein_id in sorted(by_baustein)
    ]
    # Bausteine ohne Zuordnung im BSI-Mapping: keine Seite ("slug" leer), aber
    # die Suche soll ehrlich antworten statt zu schweigen.
    data += [
        {
            "id": baustein_id,
            "title": baustein_title(baustein_id, baustein_links.get(baustein_id)),
            "slug": "",
        }
        for baustein_id in sorted(set(baustein_links) - set(by_baustein))
    ]
    DATA_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_OUT_DIR / "bausteine.json").write_text(
        json.dumps(data, indent="\t", ensure_ascii=False) + "\n"
    )
    return data


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
    "equal-to": "identisch mit",
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
        # Zusaetzlich zum externen BSI-PDF ein interner Link auf die eigene
        # Vergleichsseite (alle Zuordnungen dieses Bausteins) -- die gab es
        # bisher nur in der Gegenrichtung (control_link() auf den Vergleichs-
        # seiten). Ohne das war die Anforderungsseite eine Sackgasse fuer
        # jeden, der von hier aus den vollen Alt-Kontext sehen wollte.
        if baustein_id:
            obj += f", vergleichHref: {jsx_string(f'/vergleich/{baustein_slug(baustein_id)}/')}"
        obj += " }"
        items.append(obj)
    return "[" + ", ".join(items) + "]"


def render_control_meta(control, basethreats_by_id, tags_by_id, predecessor_index, baustein_links):
    modal_verb = part_prop_value(control, "statement", "modal_verb")
    sec_level = prop_value(control, "sec_level")
    effort = prop_value(control, "effort_level")
    threats = prop_value(control, "threats")
    tags = render_tags_prop(control, tags_by_id)
    targets = render_targets_prop(control)
    inherited = inherited_targets(control)
    dokument = part_prop_value(control, "statement", "documentation")
    predecessors = render_predecessors_prop(control["id"], predecessor_index, baustein_links)
    if not (modal_verb or sec_level or effort or threats or tags or targets or predecessors):
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
    if tags:
        attrs.append(f"tags={{{tags}}}")
    if targets:
        attrs.append(f"targets={{{targets}}}")
        if inherited:
            attrs.append("inheritedTargets={[" + ", ".join(jsx_string(n) for n in inherited) + "]}")
    else:
        # Keine Zielobjektkategorie: laut Standard 300-1 (3.4.1) gehoert die
        # Anforderung in jedes Anforderungspaket. 364 von 1000 Anforderungen.
        attrs.append("noTarget")
    if dokument:
        attrs.append("document={{ name: " + jsx_string(dokument) + ", slug: " + jsx_string(tag_slug(dokument)) + " }}")
    if predecessors:
        attrs.append(f"predecessors={{{predecessors}}}")
    return f"<ControlMeta {' '.join(attrs)} />\n"


def heading_anchor(id_):
    """{#id}-Ueberschriften-Attribut, nativ vom Satteri-Markdown-Prozessor
    geparst (markdown.processor in astro.config.mjs, features.headingAttributes).
    Satteri konsumiert die {}-Syntax vor MDX' eigenem Ausdrucks-Scanner --
    kein HTML-Entity-Escaping noetig, mit Build + Link-Validator bestaetigt."""
    return f"{{#{id_}}}"


def render_control(control, level, params_by_id, basethreats_by_id, tags_by_id, predecessor_index, baustein_links):
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
        # Reine Such-Gewichtung, keine neue Information: Pagefind gewichtet
        # Ueberschriften schon mit 7.0 (h1) bis 2.0 (h6) -- auf einer
        # Vergleichsseite kann dieselbe ID aber in einer dichten Tabelle
        # mehrfach auftauchen und die Einzel-Ueberschrift der echten
        # Anforderung trotzdem ueberholen (beobachtet: GC.5.1.1 rangierte
        # hinter einer Seite, die die ID nur in einer Mapping-Zeile nennt).
        # Deshalb hier zusaetzlich zur Skala 10.0 (quadratisch, ~100x
        # Standardtext). aria-hidden, weil die ID in der Ueberschrift bereits
        # vorgelesen wird -- Screenreader sollen sie nicht doppelt hoeren.
        f'<span class="sr-only" aria-hidden="true" data-pagefind-weight="10">{control["id"]}</span>\n',
    ]

    meta = render_control_meta(control, basethreats_by_id, tags_by_id, predecessor_index, baustein_links)
    if meta:
        lines.append(meta)

    statement = substitute_params(part_text(control, "statement"), params_by_id)
    if statement:
        lines.append(f"> {statement}\n")

    guidance = substitute_params(part_text(control, "guidance"), params_by_id)
    if guidance:
        lines.append(f"{guidance}\n")

    for sub in control.get("controls", []):
        lines.append(render_control(sub, level + 1, params_by_id, basethreats_by_id, tags_by_id, predecessor_index, baustein_links))

    return "\n".join(lines)


def render_group(group, level, params_by_id, basethreats_by_id, tags_by_id, predecessor_index, baustein_links, include_heading=True):
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
        lines.append(render_control(control, level + 1, params_by_id, basethreats_by_id, tags_by_id, predecessor_index, baustein_links))

    for sub in group.get("groups", []):
        lines.append(render_group(sub, level + 1, params_by_id, basethreats_by_id, tags_by_id, predecessor_index, baustein_links))

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
    for start, end, label, detail, _label_en, _detail_en, range_text, _banner in TIMELINE:
        is_current = start <= today and (end is None or today <= end)
        status = ' data-current="true"' if is_current else ""
        badge = '<span class="status-badge">läuft</span>' if is_current else ""
        lines.append(
            f'<li{status}><span class="status-range">{range_text or format_range(start, end)}</span>'
            f"<strong>{label}</strong>{badge}<p>{detail}</p></li>"
        )
    lines.append("</ul>\n")
    return "\n".join(lines)


def banner_phase(day):
    """Der TIMELINE-Eintrag, der an diesem Tag im Banner steht, oder None.

    Kuerzeste laufende Phase gewinnt; bei Gleichstand der spaetere Eintrag (siehe
    Kommentar an TIMELINE). Eigene Funktion, damit sich fuer jeden Tag pruefen laesst,
    was der Banner zeigen wuerde (scripts/tests/test_timeline.py)."""
    laufend = [
        entry
        for entry in TIMELINE
        if entry[7] and entry[0] <= day and (entry[1] is None or day <= entry[1])
    ]
    if not laufend:
        return None
    return min(reversed(laufend), key=lambda p: (p[1] - p[0]).days if p[1] else 10**6)


def write_status_data():
    """Aktuelle Phase fuer die sitewide Status-Leiste (Banner.astro).

    Der Banner stand bis 2026-10-01 als fester Text im Bauteil und behauptete
    danach weiter "aktuell in der Pilotphase (bis 30.9.2026)" -- auf einer
    Seite, deren Thema Fristen sind, der teuerste denkbare Fehler: er steht
    ueber allem und widersprach der eigenen, datumsgesteuerten Zeitleiste.
    Jetzt kommt beides aus TIMELINE, damit es nicht wieder auseinanderlaufen
    kann.

    Mehrere Phasen koennen gleichzeitig laufen (Pilot- und Uebergangsphase
    ueberlappten von 04/2026 bis 09/2026). Fuer die Leiste gewinnt die
    kuerzeste laufende Phase -- die spezifischste Aussage, und dieselbe Wahl,
    die vorher von Hand getroffen war.
    """
    today = date.today()
    phase = banner_phase(today)
    if phase is None:
        raise SystemExit(
            f"Keine Phase in TIMELINE umfasst heute ({today.isoformat()}). "
            "Die Status-Leiste haette nichts anzuzeigen -- TIMELINE in "
            "scripts/generate_docs.py fortschreiben."
        )
    start, end, label, detail, label_en, detail_en, _range_text, _banner = phase

    data = {
        "phase": label,
        "bis": end.strftime("%m/%Y") if end else None,
        # Die Leiste steht auf jeder Seite und soll ein dezenter Hinweis bleiben,
        # keine zweite Ueberschrift: nur der erste Satz des Detailtexts. Darum
        # steht in TIMELINE die wichtigste Aussage immer zuerst.
        "detail": first_sentence(detail),
        "phase_en": label_en,
        "detail_en": first_sentence(detail_en),
    }
    DATA_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_OUT_DIR / "status.json").write_text(
        json.dumps(data, indent="\t", ensure_ascii=False) + "\n"
    )
    return data


def render_index_section(heading, intro, entries):
    lines = [f"## {heading}\n", f"{intro}\n", '<ul class="practice-index">']
    for gid, title, slug, summary in entries:
        lines.append(
            f'<li><a href="/grundschutzpp/{slug}/"><span class="practice-id">{gid}</span> {title}</a>'
            f"<p>{summary}</p></li>"
        )
    lines.append("</ul>\n")
    return "\n".join(lines)


# --- Export (CSV/JSON) --------------------------------------------------------
# Download-Dateien fuer den IT-Grundschutz-Check: alle Anforderungen, je Praktik
# eine Datei, dazu die JSON-Datei, aus der die Exportseite im Browser filtert.
# Liegt in public/, wird also unveraendert ausgeliefert. Der Dateistand kommt aus
# dem Katalog (metadata.last-modified), nicht aus dem Tagesdatum: sonst aenderte
# jeder Sync-Lauf alle Dateien, auch wenn der Katalog gleich geblieben ist.
EXPORT_OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "downloads"
EXPORT_SITE_URL = os.environ.get("SITE_URL", "https://grundschutz-docs.de").rstrip("/")
EXPORT_NO_TARGET = "Ohne Zielobjektkategorie"
EXPORT_LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
EXPORT_SOURCE_URL = "https://github.com/BSI-Bund/Stand-der-Technik-Bibliothek"
DEFAULT_DOCUMENTATION_FILE = (
    REPO_ROOT / "Grundschutz-PlusPlus" / "documentation" / "namespaces" / "documentation_guidelines.csv"
)
DOCUMENTATION_FILE = (
    Path(os.environ["GRUNDSCHUTZPP_DOCUMENTATION"])
    if os.environ.get("GRUNDSCHUTZPP_DOCUMENTATION")
    else DEFAULT_DOCUMENTATION_FILE
)

# Reihenfolge = Spalten in der CSV. Die vier Leerspalten dahinter sind fuer den
# Soll-Ist-Abgleich gedacht und gehoeren nicht zum Katalog.
EXPORT_COLUMNS = [
    "ID", "Titel", "Praktik", "Anforderung", "Pflichtgrad", "Sicherheitsstufe", "Aufwand",
    "Zielobjektkategorien", "Gilt auch für Unterkategorien", "Ergebnis", "Dokumentiert in", "Gefährdungen",
    "Vorgänger im Kompendium 2023", "Seite",
]
EXPORT_WORKSHEET_COLUMNS = ["Umsetzungsstatus", "Verantwortlich", "Frist", "Bemerkung"]
EXPORT_SOURCE_COLUMN = "Quelle"


def load_documentation_guidelines():
    # documentation_guidelines.csv des BSI: Dokumenttyp -> Beschreibung, Kategorie,
    # Zielgruppe. Die Tabelle ist beim BSI nicht fertig: einzelne Zeilen tragen "???".
    # Die gelten hier als "unbekannt" und werden nicht als Text uebernommen.
    def clean(value):
        value = (value or "").strip()
        return "" if value == "???" else value

    with DOCUMENTATION_FILE.open(newline="", encoding="utf-8") as f:
        return {
            row["Begriff"].strip(): {
                "beschreibung": clean(row["Definition"]),
                "kategorie": clean(row["Kategorie"]),
                "zielgruppe": clean(row["Zielgruppe"]),
            }
            for row in csv.DictReader(f)
        }


def export_stand(catalog):
    iso = catalog["metadata"]["last-modified"][:10]
    y, m, d = iso.split("-")
    return f"{d}.{m}.{y}"


def export_source_note(stand):
    return (
        f"BSI Grundschutz++ (Anwenderkatalog), Stand {stand}, © BSI-Bund, CC BY-SA 4.0 "
        f"({EXPORT_LICENSE_URL}); bearbeitet (Auswahl, Spalten) von grundschutz-docs.de; "
        f"Original: {EXPORT_SOURCE_URL}"
    )


def export_plain_text(text, params_by_id):
    # Klartext fuer Tabellen: Parameter als [Label], wie in der RAG-Datei.
    if not text:
        return ""
    return " ".join(PARAM_RE.sub(lambda m: f"[{params_by_id.get(m.group(1), m.group(1))}]", text).split())


@functools.cache
def export_target_descendants():
    """Zielobjektkategorie -> alle Kategorien darunter (Kinder, Enkel, ...), aus der Hierarchie
    der BSI-Tabelle (TARGETS).

    Warum: Der Katalog verlangt in STM.2.1.4.1 ("Vererbung von Zielobjektkategorien"),
    dass ein Asset auch die in der Hierarchie uebergeordneten Kategorien erhaelt. Eine
    Anforderung fuer "Anwendungen" gilt damit auch fuer ein Asset der Kategorie
    "Webserver". Wer nur die direkt zugeordnete Kategorie auswertet, uebersieht sie."""
    def ancestors(name):
        out, seen, parent = [], set(), TARGETS[name]["parent"]
        while parent and parent not in seen:
            out.append(parent)
            seen.add(parent)
            parent = TARGETS[parent]["parent"]
        return out

    return {name: sorted(other for other in TARGETS if name in ancestors(other)) for name in TARGETS}


def export_rows(catalog, params_by_id, basethreats_by_id, predecessor_index):
    descendants = export_target_descendants()
    rows = []
    for group in catalog["groups"]:
        slug = group["id"].lower()
        for control in collect_controls(group):
            cid = control["id"]
            threat_ids = [t.strip() for t in (prop_value(control, "threats") or "").split(",") if t.strip()]
            sec = prop_value(control, "sec_level")
            direct_targets = control_targets(control)
            rows.append(
                {
                    "id": cid,
                    "titel": control.get("title", ""),
                    "praktik_id": group["id"],
                    "praktik": f"{group['id']} {group['title']}",
                    "anforderung": export_plain_text(part_text(control, "statement"), params_by_id),
                    "pflichtgrad": part_prop_value(control, "statement", "modal_verb") or "",
                    "stufe": SEC_LEVEL_LABELS.get(sec, sec or ""),
                    "aufwand": prop_value(control, "effort_level") or "",
                    "zielobjekte": direct_targets or [EXPORT_NO_TARGET],
                    # Kategorien darunter, fuer die die Anforderung wegen der Vererbung ebenfalls gilt
                    "unterkategorien": sorted(
                        {d for c in direct_targets for d in descendants.get(c, [])} - set(direct_targets)
                    ),
                    "ergebnis": part_prop_value(control, "statement", "result") or "",
                    "dokument": part_prop_value(control, "statement", "documentation") or "",
                    "gefaehrdungen": [f"{t} – {basethreats_by_id[t]}" for t in threat_ids if t in basethreats_by_id],
                    "vorgaenger": [
                        f"{old} ({relationship_label(rel)})" for old, rel in predecessor_index.get(cid, [])
                    ],
                    "seite": f"{EXPORT_SITE_URL}/grundschutzpp/{slug}/#{cid}",
                }
            )
    return rows


def export_name_key(name):
    # Die einzige erlaubte Abweichung zwischen zwei Dokumentnamen: Gross-/Kleinschreibung,
    # Leerzeichen und Bindestriche. Alles andere gilt als anderer Name.
    return name.casefold().replace(" ", "").replace("-", "")


def export_documents(rows, guidelines, praktik_order):
    """Eine Zeile je Dokumenttyp, auf den Anforderungen einzahlen.

    Die Anforderung nennt im Katalog das Dokument, in dem ihr Ergebnis festgehalten
    werden soll (statement-Prop "documentation"). Hier wird das umgedreht: Welche
    Dokumente muss es geben, und wie viele Anforderungen haengen daran?

    Die Namen im Katalog und in documentation_guidelines.csv stimmen nicht immer
    ueberein ("Beschaffungskriterien" gegen "Leistungsbeschreibung"). Beschreibung,
    Kategorie und Zielgruppe gibt es nur, wenn der Name entweder exakt gleich ist
    ("exakt") oder sich ausschliesslich in Gross-/Kleinschreibung, Leerzeichen und
    Bindestrichen unterscheidet ("schreibweise"). Dafuer muessen alle vier gelten:
      1. der Name steht nicht schon exakt in der Tabelle (exakt hat Vorrang),
      2. die Namen sind nach export_name_key() gleich,
      3. genau ein Begriff der Tabelle passt (bei zwei gilt keiner),
      4. dieser Begriff wird im Katalog nicht selbst exakt verwendet, sonst bekaemen
         zwei Dokumenttypen dieselbe Beschreibung.
    Alles andere bleibt ohne Beschreibung ("") -- geraten wird nicht.
    """
    by_name = {}
    for row in rows:
        if not row["dokument"]:
            continue
        entry = by_name.setdefault(row["dokument"], {"anzahl": 0, "muss": 0, "praktiken": set()})
        entry["anzahl"] += 1
        entry["muss"] += row["pflichtgrad"] == "MUSS"
        entry["praktiken"].add(row["praktik_id"])
    used = set(by_name)
    by_key = {}
    for begriff in guidelines:
        by_key.setdefault(export_name_key(begriff), []).append(begriff)
    docs = []
    for name, entry in by_name.items():
        if name in guidelines:
            bsi_name, zuordnung = name, "exakt"
        else:
            kandidaten = [b for b in by_key.get(export_name_key(name), []) if b not in used]
            bsi_name, zuordnung = (kandidaten[0], "schreibweise") if len(kandidaten) == 1 else ("", "")
        info = guidelines.get(bsi_name)
        docs.append(
            {
                "dokument": name,
                "anzahl": entry["anzahl"],
                "muss": entry["muss"],
                "praktiken": sorted(entry["praktiken"], key=praktik_order.index),
                "beschreibung": info["beschreibung"] if info else "",
                "kategorie": info["kategorie"] if info else "",
                "zielgruppe": info["zielgruppe"] if info else "",
                "zuordnung": zuordnung,
                "bsi_name": bsi_name,
            }
        )
    docs.sort(key=lambda d: (-d["anzahl"], d["dokument"]))
    return docs


def export_csv_line(row, source_note):
    return [
        row["id"], row["titel"], row["praktik"], row["anforderung"], row["pflichtgrad"], row["stufe"],
        row["aufwand"], "; ".join(row["zielobjekte"]), "; ".join(row["unterkategorien"]),
        row["ergebnis"], row["dokument"],
        "; ".join(row["gefaehrdungen"]), "; ".join(row["vorgaenger"]), row["seite"],
        "", "", "", "",
        source_note,
    ]


def write_export_csv(path, rows, source_note):
    # Deutsches Excel erwartet Semikolon als Trenner und UTF-8 mit BOM, sonst
    # stehen alle Spalten in einer Zelle bzw. die Umlaute sind kaputt.
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";", lineterminator="\r\n")
        w.writerow(EXPORT_COLUMNS + EXPORT_WORKSHEET_COLUMNS + [EXPORT_SOURCE_COLUMN])
        for row in rows:
            w.writerow(export_csv_line(row, source_note))


def export_license(stand):
    """Alle Hinweise zu Quelle und Lizenz an einer Stelle.

    LIZENZ.txt, das Info-Blatt der Excel-Datei und die JSON-Datei lesen von hier.
    Stuende der Text an drei Stellen, liefen sie bei der naechsten Aenderung
    auseinander, und die Quellenangabe waere in einer der Dateien falsch."""
    return {
        "stand": stand,
        "urheber": "Bundesamt für Sicherheit in der Informationstechnik (BSI-Bund)",
        "werk": "Grundschutz++ (Anwenderkatalog), OSCAL-Katalog",
        "original": EXPORT_SOURCE_URL,
        "lizenz": "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)",
        "lizenz_url": EXPORT_LICENSE_URL,
        "aenderungen": (
            "Diese Dateien sind eine Bearbeitung des Originals und keine Datei des BSI. Sie wurden von "
            "grundschutz-docs.de aus dem Katalog erzeugt: Auswahl der Felder, Texte ohne Formatierung, "
            "Parameter als [Platzhalter], Zielobjektkategorien, Ergebnis, Dokument, Gefährdungen und die ID "
            "der Vorgänger-Anforderung aus dem Mapping ergänzt, Spalten für die eigene Arbeit angehängt. "
            "Der Inhalt der Anforderungen ist nicht verändert."
        ),
        "dokumente": (
            "Das Excel-Blatt \"Dokumente\" fasst zusammen, in welchen Dokumenten der Katalog Ergebnisse "
            "festhalten lässt. Beschreibung, Kategorie und Zielgruppe eines Dokumenttyps stammen aus "
            "documentation_guidelines.csv des BSI (ebenfalls CC BY-SA 4.0). Sie werden einem Dokumenttyp nur "
            "zugeordnet, wenn der Name dort exakt vorkommt oder sich nur in Groß-/Kleinschreibung, Leerzeichen "
            "und Bindestrichen unterscheidet; die Spalte \"Hinweis zur Beschreibung\" sagt, wie es zustande "
            "kam. Bei allen anderen Dokumenttypen bleibt die Beschreibung leer."
        ),
        "eigene_werte": (
            "Umsetzungsstatus: Erfüllt, Nicht erfüllt und Nicht anwendbar sind die Statuswerte des "
            "BSI-Standards 300-1 (4.1.1). \"In Umsetzung\" ergänzt grundschutz-docs.de, weil der Standard "
            "Anforderungen kennt, die noch nicht erfüllt, aber schon in der Umsetzungsplanung sind. "
            "Die Liste \"Vorhanden\" (Ja, Teilweise, Nein) ist eine Wahl von grundschutz-docs.de und "
            "stammt nicht aus dem Katalog oder dem Standard des BSI."
        ),
        "weitergabe": (
            "Die Bearbeitung steht ebenfalls unter CC BY-SA 4.0. Wer sie weitergibt, nennt das BSI als "
            "Urheber, verweist auf die Lizenz und gibt eigene Änderungen an."
        ),
        "nicht_enthalten": (
            "Text des IT-Grundschutz-Kompendiums 2023 und des BSI-Standards 300-1. Für diese gelten die "
            "Nutzungsbedingungen des BSI, nicht CC BY-SA. In der Spalte \"Vorgänger im Kompendium 2023\" "
            "stehen nur die IDs der alten Anforderungen."
        ),
        "hinweis": "Diese Dateien sind kein offizielles Angebot des BSI und keine Rechtsberatung.",
    }


def export_license_text(stand, lizenz):
    import textwrap

    def absatz(titel, text):
        return textwrap.fill(f"{titel} {text}", width=92, subsequent_indent=" " * (len(titel) + 1)) + "\n\n"

    return (
        "Grundschutz++ – Anforderungen als Tabelle (CSV und Excel)\n"
        "===========================================================\n\n"
        f"Datenstand des Katalogs: {stand}\n\n"
        f"Urheber:   {lizenz['urheber']}\n"
        f"Werk:      {lizenz['werk']}\n"
        f"Original:  {lizenz['original']}\n"
        f"Lizenz:    {lizenz['lizenz']}\n"
        f"           {lizenz['lizenz_url']}\n\n"
        + absatz("Änderungen:", lizenz["aenderungen"])
        + absatz("Dokumente:", lizenz["dokumente"])
        + absatz("Eigene Werte:", lizenz["eigene_werte"])
        + absatz("Weitergabe:", lizenz["weitergabe"])
        + absatz("Nicht enthalten:", lizenz["nicht_enthalten"])
        + lizenz["hinweis"]
        + "\n"
    )


def write_export_data(catalog, params_by_id, basethreats_by_id, predecessor_index, guidelines):
    stand = export_stand(catalog)
    note = export_source_note(stand)
    lizenz = export_license(stand)
    rows = export_rows(catalog, params_by_id, basethreats_by_id, predecessor_index)
    praktik_order = [g["id"] for g in catalog["groups"]]
    dokumente = export_documents(rows, guidelines, praktik_order)

    EXPORT_OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in EXPORT_OUT_DIR.glob("*"):
        old.unlink()

    write_export_csv(EXPORT_OUT_DIR / "grundschutzpp-anforderungen.csv", rows, note)
    by_praktik = {}
    for row in rows:
        by_praktik.setdefault(row["praktik_id"], []).append(row)
    for pid, praktik_rows in by_praktik.items():
        write_export_csv(EXPORT_OUT_DIR / f"grundschutzpp-anforderungen-{pid.lower()}.csv", praktik_rows, note)

    (EXPORT_OUT_DIR / "grundschutzpp-anforderungen.json").write_text(
        json.dumps(
            {
                "stand": stand,
                "quelle": note,
                "lizenz": lizenz,
                "spalten": EXPORT_COLUMNS,
                "arbeitsspalten": EXPORT_WORKSHEET_COLUMNS,
                "praktiken": [{"id": g["id"], "titel": g["title"]} for g in catalog["groups"]],
                "anforderungen": rows,
                "dokumente": dokumente,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )

    (EXPORT_OUT_DIR / "LIZENZ.txt").write_text(export_license_text(stand, lizenz), encoding="utf-8")
    per_schreibweise = [f"{d['dokument']} -> {d['bsi_name']}" for d in dokumente if d["zuordnung"] == "schreibweise"]
    ohne_beschreibung = [d["dokument"] for d in dokumente if not d["zuordnung"]]
    if per_schreibweise:
        print(
            f"HINWEIS: {len(per_schreibweise)} Dokumenttypen nur ueber die Schreibweise der BSI-Tabelle "
            f"zugeordnet: {'; '.join(per_schreibweise)}",
            file=sys.stderr,
        )
    if ohne_beschreibung:
        print(
            f"HINWEIS: {len(ohne_beschreibung)} Dokumenttypen aus dem Katalog stehen nicht unter "
            f"diesem Namen in documentation_guidelines.csv (keine Beschreibung im Export): "
            f"{', '.join(ohne_beschreibung)}",
            file=sys.stderr,
        )
    return {
        "anforderungen": len(rows),
        "praktiken": len(by_praktik),
        "dokumente": len(dokumente),
        "stand": stand,
    }


def check_export(catalog):
    """Liest die fertigen Export-Dateien zurueck und zaehlt gegen den *Rohtext*
    des Katalogs -- nicht gegen collect_controls(), das der Export selbst nutzt.
    Gleiche Regel wie bei check_invariants: ein Test auf demselben Codepfad
    bestaetigt nur den gemeinsamen Fehler."""
    problems = []
    raw = CATALOG_FILE.read_text()
    # Anforderungen tragen direkt nach der ID ein "class", Untergruppen (ARCH.1)
    # nicht -- ohne diese Unterscheidung kaemen 160 Gruppen-IDs dazu.
    raw_ids = set(re.findall(r'"id": "([A-Z]+(?:\.[0-9]+)+)",\s*"class":', raw))
    raw_rows = raw.count('"name": "modal_verb"')
    raw_muss = len(re.findall(r'"name": "modal_verb",\s*"ns": "[^"]*",\s*"value": "MUSS"', raw))
    raw_targets = raw.count('"name": "target_object_categories"')
    raw_documented = raw.count('"name": "documentation"')
    raw_results = raw.count('"name": "result"')

    with (EXPORT_OUT_DIR / "grundschutzpp-anforderungen.csv").open(newline="", encoding="utf-8-sig") as f:
        table = list(csv.reader(f, delimiter=";"))
    head, body = table[0], table[1:]
    if (EXPORT_OUT_DIR / "grundschutzpp-anforderungen.csv").read_bytes()[:3] != b"\xef\xbb\xbf":
        problems.append("CSV ohne UTF-8-BOM: Excel zeigt Umlaute falsch")
    expected_head = EXPORT_COLUMNS + EXPORT_WORKSHEET_COLUMNS + [EXPORT_SOURCE_COLUMN]
    if head != expected_head:
        problems.append("CSV-Kopfzeile weicht von EXPORT_COLUMNS ab")
    if any(len(r) != len(head) for r in body):
        problems.append("CSV: Zeilen mit falscher Spaltenzahl")

    # Spalten ueber den Namen ansprechen: bei einer neuen Spalte darf die Pruefung
    # nicht stillschweigend die falsche lesen.
    col = {name: i for i, name in enumerate(head)}
    ids = [r[col["ID"]] for r in body]
    if len(body) != raw_rows:
        problems.append(f"CSV hat {len(body)} Zeilen, der Katalogtext hat {raw_rows} modal_verb-Eintraege")
    if len(set(ids)) != len(ids):
        problems.append("CSV: doppelte IDs")
    if set(ids) != raw_ids:
        problems.append(
            f"CSV-IDs und Katalog-IDs weichen ab (nur CSV: {sorted(set(ids) - raw_ids)[:3]}, "
            f"nur Katalog: {sorted(raw_ids - set(ids))[:3]})"
        )
    muss = sum(1 for r in body if r[col["Pflichtgrad"]] == "MUSS")
    if muss != raw_muss:
        problems.append(f"CSV hat {muss} MUSS, der Katalogtext {raw_muss}")
    with_target = sum(1 for r in body if r[col["Zielobjektkategorien"]] != EXPORT_NO_TARGET)
    if with_target != raw_targets:
        problems.append(f"CSV hat {with_target} Zeilen mit Zielobjekt, der Katalogtext {raw_targets}")
    if any("{{" in r[col["Anforderung"]] or "insert:" in r[col["Anforderung"]] for r in body):
        problems.append("CSV: unersetzter Parameter im Anforderungstext")
    if any(r[col["Anforderung"]] == "" or r[col["Pflichtgrad"]] not in {"MUSS", "SOLLTE", "KANN"} for r in body):
        problems.append("CSV: leerer Anforderungstext oder unbekannter Pflichtgrad")

    # Ergebnis und Dokument: jede Anforderung hat im Katalog genau ein Ergebnis, ein
    # Dokument nur 961 von 1000. Beide Zahlen aus dem Rohtext gezaehlt.
    with_result = sum(1 for r in body if r[col["Ergebnis"]])
    documented = sum(1 for r in body if r[col["Dokumentiert in"]])
    if with_result != raw_results:
        problems.append(f"CSV hat {with_result} Zeilen mit Ergebnis, der Katalogtext {raw_results}")
    if documented != raw_documented:
        problems.append(f"CSV hat {documented} Zeilen mit Dokument, der Katalogtext {raw_documented}")
    # CSV-Injection: eine Zelle, die mit = + - @ beginnt, wuerde Excel als Formel lesen.
    if any(cell[:1] in "=+-@" for r in body for cell in r[: len(EXPORT_COLUMNS)] if cell):
        problems.append("CSV: Zelle beginnt mit = + - oder @ (Excel liest das als Formel)")

    # Vererbung der Zielobjektkategorien (STM.2.1.4.1): die Spalte "Gilt auch fuer
    # Unterkategorien" wird auf einem anderen Weg nachgerechnet als der Export sie
    # erzeugt: Hierarchie ueber UUID/ChildOfUUID aus der frisch gelesenen CSV (der Export
    # arbeitet mit Namen), direkte Zuordnungen aus dem Rohbaum des Katalogs.
    with TARGETS_FILE.open(newline="", encoding="utf-8") as fh:
        ziel_rows = list(csv.DictReader(fh))
    kinder_von, name_von, uuid_von = {}, {}, {}
    for zr in ziel_rows:
        kinder_von.setdefault(zr["ChildOfUUID"], []).append(zr["UUID"])
        name_von[zr["UUID"]] = zr["Zielobjekt"]
        uuid_von[zr["Zielobjekt"]] = zr["UUID"]

    def unterhalb(uuid):
        gefunden, offen = set(), list(kinder_von.get(uuid, []))
        while offen:
            k = offen.pop()
            if k not in gefunden:
                gefunden.add(k)
                offen.extend(kinder_von.get(k, []))
        return {name_von[k] for k in gefunden}

    erwartet_unter = {}

    def sammle(knoten):
        for c in knoten.get("controls", []):
            st = next(p for p in c["parts"] if p["name"] == "statement")
            v = next((x["value"] for x in st["props"] if x["name"] == "target_object_categories"), "")
            direkt = [x.strip() for x in v.split(",") if x.strip()]
            erwartet_unter[c["id"]] = sorted({n for d in direkt for n in unterhalb(uuid_von[d])} - set(direkt))
            sammle(c)
        for g in knoten.get("groups", []):
            sammle(g)

    sammle(json.loads(raw)["catalog"])
    # Beispiel in Text der Exportseite, der Komponente und des Info-Blatts ("Webserver" unter
    # "Anwendungen"): aendert das BSI die Hierarchie, muss der Text geaendert werden.
    if TARGETS.get("Webserver", {}).get("parent") != "Anwendungen":
        problems.append(
            "Das Beispiel 'Webserver' unter 'Anwendungen' (export.mdx, ExportTabelle.astro, "
            "export-workbook.js) stimmt nicht mehr zur Hierarchie des BSI: Texte anpassen"
        )
    if not any(erwartet_unter.values()):
        problems.append("Vererbung: keine einzige Unterkategorie gefunden, Hierarchie leer gelesen?")
    ist_unter = {
        r[col["ID"]]: sorted(x for x in r[col["Gilt auch für Unterkategorien"]].split("; ") if x) for r in body
    }
    if ist_unter != erwartet_unter:
        falsch = sorted(i for i in erwartet_unter if ist_unter.get(i) != erwartet_unter[i])[:3]
        problems.append(f"CSV: Spalte 'Gilt auch fuer Unterkategorien' weicht von der Nachrechnung ab (z. B. {falsch})")

    # Dieselbe Nachrechnung gegen die unsichtbaren Suchfilter-Marken (inheritedTargets) auf den
    # geschriebenen Katalogseiten: Pro Anforderung genau die Unterkategorien, die auch die
    # CSV-Spalte nennt. Aus dem Text zurueckgelesen, nicht aus dem Generatorcode.
    gelesen_marken, aktuell = {}, None
    for seite in OUT_DIR.glob("*.mdx"):
        for zeile in seite.read_text().splitlines():
            m = re.search(r"\{#([A-Z]+(?:\.[0-9]+)+)\}\s*$", zeile)
            if m and zeile.startswith("#"):
                aktuell = m.group(1)
            elif zeile.startswith("<ControlMeta ") and aktuell:
                im = re.search(r"inheritedTargets=\{\[(.*?)\]\}", zeile)
                gelesen_marken[aktuell] = sorted(re.findall(r'"([^"]+)"', im.group(1))) if im else []
                aktuell = None
    erwartet_marken = {i: v for i, v in erwartet_unter.items()}
    if gelesen_marken != erwartet_marken:
        falsch = sorted(i for i in erwartet_marken if gelesen_marken.get(i) != erwartet_marken[i])[:3]
        problems.append(f"Suchfilter: geerbte Zielobjekt-Marken auf den Katalogseiten weichen von der Nachrechnung ab (z. B. {falsch})")

    # Jede Datei je Praktik zusammen ergibt wieder die Gesamtdatei.
    summe = 0
    for datei in EXPORT_OUT_DIR.glob("grundschutzpp-anforderungen-*.csv"):
        with datei.open(newline="", encoding="utf-8-sig") as f:
            summe += len(list(csv.reader(f, delimiter=";"))) - 1
    if summe != len(body):
        problems.append(f"Praktik-Dateien ergeben {summe} Zeilen, die Gesamtdatei {len(body)}")

    # Der Link in der Spalte "Seite" muss auf einen existierenden Anker zeigen.
    for r in body:
        m = re.match(r".*/grundschutzpp/([a-z]+)/#(.+)$", r[col["Seite"]])
        seite = OUT_DIR / f"{m.group(1)}.mdx" if m else None
        if not m or not seite.exists() or f"{{#{m.group(2)}}}" not in seite.read_text():
            problems.append(f"CSV: Link fuer {r[0]} zeigt auf keinen Anker ({r[col['Seite']]})")
            break

    daten = json.loads((EXPORT_OUT_DIR / "grundschutzpp-anforderungen.json").read_text())
    if [a["id"] for a in daten["anforderungen"]] != ids:
        problems.append("JSON und CSV nennen verschiedene Anforderungen oder eine andere Reihenfolge")
    if {a["id"]: a["unterkategorien"] for a in daten["anforderungen"]} != erwartet_unter:
        problems.append("JSON: 'unterkategorien' weicht von der Nachrechnung ab")
    if not (EXPORT_OUT_DIR / "LIZENZ.txt").exists():
        problems.append("LIZENZ.txt fehlt")
    else:
        text = (EXPORT_OUT_DIR / "LIZENZ.txt").read_text(encoding="utf-8")
        lizenz = daten.get("lizenz") or {}
        for feld in ("stand", "urheber", "original", "lizenz", "lizenz_url", "aenderungen", "weitergabe", "nicht_enthalten"):
            if not lizenz.get(feld):
                problems.append(f"JSON: lizenz.{feld} fehlt oder ist leer")
            elif feld in ("stand", "urheber", "original", "lizenz_url") and lizenz[feld] not in text:
                problems.append(f"LIZENZ.txt nennt lizenz.{feld} nicht")
        # Der Quellenhinweis je Zeile (Spalte "Quelle") muss dieselben Angaben tragen.
        for feld in ("stand", "original", "lizenz_url"):
            if lizenz.get(feld) and lizenz[feld] not in daten["quelle"]:
                problems.append(f"Quelle-Spalte nennt lizenz.{feld} nicht")

    # Jede Praktik-Seite verweist auf ihre Export-Datei: die Datei muss es geben und der
    # Link auf der Seite muss zu ihr und zur vorgewaehlten Exportseite passen.
    for p in daten["praktiken"]:
        pid, slug = p["id"], p["id"].lower()
        datei = EXPORT_OUT_DIR / f"grundschutzpp-anforderungen-{slug}.csv"
        seite = OUT_DIR / f"{slug}.mdx"
        text = seite.read_text() if seite.exists() else ""
        if not datei.exists():
            problems.append(f"{pid}: {datei.name} fehlt")
        if f'/downloads/{datei.name}" download>' not in text:
            problems.append(f"{pid}: die Praktik-Seite verlinkt {datei.name} nicht als Download")
        if f'/export/?praktik={pid}"' not in text:
            problems.append(f"{pid}: die Praktik-Seite verlinkt die Exportseite nicht mit praktik={pid}")

    # Dokumentenuebersicht: ihre Summe muss die 961 Anforderungen mit Dokument
    # ergeben (Rohtext), und jede Zeile muss sich aus der CSV nachzaehlen lassen,
    # nicht aus den Daten, mit denen sie gebaut wurde.
    dokumente = daten["dokumente"]
    if sum(d["anzahl"] for d in dokumente) != raw_documented:
        problems.append(
            f"Dokumentenuebersicht ergibt {sum(d['anzahl'] for d in dokumente)} Anforderungen, "
            f"der Katalogtext {raw_documented}"
        )
    nachgezaehlt = {}
    for r in body:
        name = r[col["Dokumentiert in"]]
        if name:
            z = nachgezaehlt.setdefault(name, [0, 0])
            z[0] += 1
            z[1] += r[col["Pflichtgrad"]] == "MUSS"
    if {d["dokument"]: [d["anzahl"], d["muss"]] for d in dokumente} != nachgezaehlt:
        problems.append("Dokumentenuebersicht passt nicht zu den Zeilen der CSV (Anzahl oder MUSS je Dokument)")
    if len({d["dokument"] for d in dokumente}) != len(dokumente):
        problems.append("Dokumentenuebersicht: ein Dokumenttyp kommt doppelt vor")

    # Zuordnung der Beschreibungen: die Regel wird hier mit einer anderen Umsetzung
    # (regulaerer Ausdruck, CSV neu gelesen) nachgerechnet, nicht mit export_name_key().
    def key(name):
        return re.sub(r"[ \-]", "", name.casefold())

    with DOCUMENTATION_FILE.open(newline="", encoding="utf-8") as f:
        csv_rows = {r["Begriff"].strip(): r for r in csv.DictReader(f)}
    katalog_namen = {d["dokument"] for d in dokumente}
    for d in dokumente:
        name, z, bsi = d["dokument"], d["zuordnung"], d["bsi_name"]
        if z not in {"exakt", "schreibweise", ""}:
            problems.append(f"{name}: unbekannte Zuordnung {z!r}")
            continue
        if z == "exakt" and (name != bsi or name not in csv_rows):
            problems.append(f"{name}: als exakt markiert, steht aber nicht exakt in der Tabelle")
        if z == "schreibweise":
            if bsi not in csv_rows or bsi == name:
                problems.append(f"{name}: Schreibweise-Zuordnung auf {bsi!r}, das nicht (anders) in der Tabelle steht")
            elif key(name) != key(bsi):
                problems.append(f"{name}: Zuordnung zu {bsi!r}, obwohl sich die Namen nicht nur in Schreibweise unterscheiden")
            elif bsi in katalog_namen:
                problems.append(f"{name}: {bsi!r} wird im Katalog selbst verwendet, doppelte Zuordnung")
        if z == "":
            frei = [b for b in csv_rows if key(b) == key(name) and b not in katalog_namen]
            if name in csv_rows or frei:
                problems.append(f"{name}: ohne Zuordnung, obwohl die Tabelle {name if name in csv_rows else frei} kennt")
            if d["beschreibung"] or d["kategorie"] or d["zielgruppe"]:
                problems.append(f"{name}: Beschreibung ohne Zuordnung")
        if z:
            erwartet = {
                "beschreibung": (csv_rows[bsi]["Definition"] or "").strip(),
                "kategorie": (csv_rows[bsi]["Kategorie"] or "").strip(),
                "zielgruppe": (csv_rows[bsi]["Zielgruppe"] or "").strip(),
            }
            for feld, wert in erwartet.items():
                wert = "" if wert == "???" else wert
                if d[feld] != wert:
                    problems.append(f"{name}: {feld} weicht von der Tabelle ab")
    zuordnungen = [d["bsi_name"] for d in dokumente if d["zuordnung"]]
    if len(set(zuordnungen)) != len(zuordnungen):
        problems.append("Dokumentenuebersicht: ein Begriff der BSI-Tabelle ist mehreren Dokumenttypen zugeordnet")
    stats = {z: sum(1 for d in dokumente if d["zuordnung"] == z) for z in ("exakt", "schreibweise", "")}

    if problems:
        raise SystemExit("Export passt nicht zum Katalog:\n  - " + "\n  - ".join(problems))
    print(
        f"Export ok: {len(body)} Zeilen ({muss} MUSS, {with_target} mit Zielobjekt), {len(ids)} eindeutige IDs; "
        f"{len(dokumente)} Dokumenttypen ({stats['exakt']} exakt, {stats['schreibweise']} per Schreibweise, "
        f"{stats['']} ohne Beschreibung)"
    )



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

    # 4b. Zielobjektkategorien. Zwei Wege, die sich gegenseitig pruefen:
    #     (1) Jede im Katalog genannte Kategorie steht in der CSV des BSI --
    #         sonst haette die Pille keinen Tooltip und der Filterwert waere
    #         ein Name ohne Definition. Umgekehrt ist eine ungenutzte
    #         CSV-Zeile kein Fehler.
    #     (2) Aus den geschriebenen Seiten zurueckgelesen: je Anforderung genau
    #         eine ControlMeta-Angabe, entweder targets={[ oder noTarget. Pro
    #         Anforderung gezaehlt, nicht nur als Summe (siehe Pruefung 4).
    unbekannt = sorted({t for c in all_controls for t in control_targets(c)} - set(TARGETS))
    if unbekannt:
        problems.append(
            f"Zielobjektkategorien im Katalog, aber nicht in target_object_categories.csv: {unbekannt}"
        )
    mit_ziel = sum(1 for c in all_controls if control_targets(c))
    ohne_ziel = len(all_controls) - mit_ziel
    gelesen_mit = catalog_text.count(" targets={[")
    gelesen_ohne = catalog_text.count(" noTarget")
    if (gelesen_mit, gelesen_ohne) != (mit_ziel, ohne_ziel):
        problems.append(
            f"Zielobjekt-Angaben auf den Katalogseiten ({gelesen_mit} mit, {gelesen_ohne} ohne) "
            f"!= Katalog ({mit_ziel} mit, {ohne_ziel} ohne)"
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

    # 9. bausteine.json (Direktsprung der Suche) gegen die geschriebenen
    # Vergleichsseiten: jede Seite hat genau einen Eintrag, jeder Eintrag eine
    # Seite, und der Titel steht so auch auf der Seite. Sonst fuehrt der
    # Direktsprung ins Leere oder nennt einen anderen Titel als die Seite.
    bausteine = json.loads((DATA_OUT_DIR / "bausteine.json").read_text())
    seiten = {p.stem: p for p in VERGLEICH_OUT_DIR.glob("*.mdx") if p.name != "index.mdx"}
    mit_seite = [b for b in bausteine if b["slug"]]
    ohne_seite = [b for b in bausteine if not b["slug"]]
    if {b["slug"] for b in mit_seite} != set(seiten):
        problems.append("bausteine.json und die Vergleichsseiten nennen verschiedene Bausteine")
    for b in mit_seite:
        seite = seiten.get(b["slug"])
        if seite and f'title: "{b["id"]} {b["title"]}"' not in seite.read_text():
            problems.append(f"bausteine.json: Titel von {b['id']} weicht von der Seite ab")
    # Bausteine ohne Seite: die Liste auf /vergleich/ muss genau sie enthalten,
    # und die Gesamtzahl muss zur Startseiten-Zahl "von 111" passen.
    index_text = (VERGLEICH_OUT_DIR / "index.mdx").read_text()
    liste = index_text.split("{#ohne-zuordnung}", 1)[-1]
    in_liste = set(re.findall(r'<span class="old-id">([A-Z0-9.]+)</span>', liste))
    if in_liste != {b["id"] for b in ohne_seite}:
        problems.append(
            f"/vergleich/: Liste ohne Zuordnung ({len(in_liste)}) und bausteine.json "
            f"({len(ohne_seite)}) stimmen nicht überein"
        )
    gesamt = json.loads((DATA_OUT_DIR / "landing.json").read_text())["stats"]["bausteine_gesamt"]
    if len(bausteine) != gesamt:
        problems.append(f"bausteine.json hat {len(bausteine)} Einträge, landing.json nennt {gesamt} Bausteine")

    # 11. Entwurfshinweis der Mapping-Datei: die Sternchen auf den geschriebenen
    # Baustein-Seiten muessen genau die markierten Zuordnungen sein, und die Zahl
    # im Hinweis auf /vergleich/ muss dazu passen. Fehlt der Hinweis bei einer
    # Entwurfsdatei, brechen wir ab: dann steht die Seite wieder ohne Offenlegung da.
    if MAPPING_INFO["draft"]:
        sterne = sum(p.read_text().count('data-defaulted="true"') for p in VERGLEICH_OUT_DIR.glob("*.mdx") if p.name != "index.mdx")
        if sterne != len(MAPPING_INFO["defaulted"]):
            problems.append(
                f"{sterne} Sternchen auf den Baustein-Seiten, aber "
                f"{len(MAPPING_INFO['defaulted'])} als Standardwert markierte Zuordnungen"
            )
        if f"bei {len(MAPPING_INFO['defaulted'])} der {expected_rows} Zuordnungen" not in index_text:
            problems.append("/vergleich/: Hinweis zur Mapping-Datei nennt falsche Zahlen oder fehlt")
        ohne_note = sum(1 for p in VERGLEICH_OUT_DIR.glob("*.mdx") if p.name != "index.mdx" and 'class="mapping-note"' not in p.read_text())
        if ohne_note:
            problems.append(f"{ohne_note} Baustein-Seiten ohne Hinweis auf den Entwurfsstatus")

    # 8. Aus den geschriebenen Rollenseiten zurueckgelesen: die expliziten
    # Anker sind da. Pruefung 4 deckt nur die Katalogseiten ab -- genau
    # deshalb fiel am 2026-10-01 nicht auf, dass ein Generatorlauf die Anker
    # der Rollenseiten entfernte: sie waren in 30a968b direkt in die
    # *erzeugten* Dateien geschrieben worden, nicht in den Generator. Build
    # und Link-Pruefung blieben gruen, weil nichts intern darauf zeigt --
    # kaputt gewesen waeren nur Lesezeichen und fremde Links.
    for datei, anker in ROLLEN_ANKER.items():
        pfad = ROLLEN_OUT_DIR / datei
        if not pfad.exists():
            problems.append(f"{datei} fehlt")
            continue
        text = pfad.read_text()
        fehlend = [a for a in anker if f"{{#{a}}}" not in text]
        if fehlend:
            problems.append(
                f"{datei}: Anker {', '.join(fehlend)} fehlt — "
                "Ueberschriften mit Umlauten bekaemen sonst prozentcodierte IDs"
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
# Kurzform fuer schmale Bildschirme (CSS blendet zwischen "stufe-lang" und "stufe-kurz" um).
SEC_LEVEL_KURZ = {"normal-SdT": "Standard", "erhöht": "Erhöht"}


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
            f'<td><span class="stufe-lang">{sec_label}</span><span class="stufe-kurz">{SEC_LEVEL_KURZ.get(sec_level, sec_level)}</span></td></tr>\n'
        )
    lines.append("</tbody>\n</table>\n</div>\n\n")
    return "".join(lines)


def render_aufwand_section(aufwand):
    """Was der Katalog ueber Aufwand sagt -- und was nicht.

    Die naheliegende Frage einer Geschaeftsfuehrung nach "bin ich betroffen"
    ist "was kostet mich das". Der Katalog traegt dafuer ein Feld
    (effort_level, Skala 0-5), aber es beantwortet die Frage nicht so, wie man
    erwartet: MUSS-Anforderungen sind praktisch durchgehend mit 0 = "wird
    nicht bewertet" versehen. Das ist kein Datenfehler, sondern Absicht -- was
    ohnehin zwingend ist, wird nicht nach Aufwand gewichtet.

    Daraus folgt die eigentlich nuetzliche Aussage, und die steht nirgends im
    Katalog: Budgetspielraum gibt es nur unterhalb der Pflicht, und dort
    steigt der Aufwand mit der Freiwilligkeit.

    Bewusst keine Umrechnung in Euro oder Personentage. effort_level ist eine
    BSI-Skala, keine Kalkulation; sobald daraus "ca. 180 Personentage" wird,
    erfindet die Seite etwas.
    """
    def zeile(verb):
        c = aufwand[verb]
        gesamt = sum(c.values())
        nicht_bewertet = c.get("0", 0)
        bewertet = {k: v for k, v in c.items() if k != "0"}
        teile = []
        if nicht_bewertet:
            teile.append(f"{nicht_bewertet}× nicht bewertet")
        if bewertet:
            stufen = sorted(bewertet, key=int)
            # Ein einzelner Ausreisser (aktuell GC.5.1.1: MUSS mit Aufwand 3)
            # soll als solcher dastehen, nicht als "Stufe 3-3".
            if len(bewertet) == 1:
                stufe = stufen[0]
                teile.append(f"{bewertet[stufe]}× Stufe {stufe}")
            else:
                teile.append(f"Stufe {stufen[0]}–{stufen[-1]}")
                schwer = sum(v for k, v in bewertet.items() if k in ("4", "5"))
                if schwer:
                    teile.append(f"{schwer} davon auf 4–5")
        return (
            f"<tr><td><strong>{verb}</strong></td><td>{gesamt}</td>"
            f"<td>{', '.join(teile)}</td></tr>"
        )

    muss_gesamt = sum(aufwand["MUSS"].values())
    muss_unbewertet = aufwand["MUSS"].get("0", 0)
    kann = aufwand["KANN"]
    kann_gesamt = sum(kann.values())
    kann_teuer = kann.get("5", 0)

    return (
        "## Was kostet mich das?\n\n"
        f"Der Katalog gewichtet Anforderungen nach Aufwand (Skala 0–5), aber "
        f"nicht dort, wo man es zuerst vermutet: **{muss_unbewertet} der "
        f"{muss_gesamt} MUSS-Anforderungen tragen die Stufe 0 — „wird nicht "
        f"bewertet\".** Was ohnehin zwingend ist, wird nicht nach Aufwand "
        f"gewichtet. Eine Kostenschätzung für den Pflichtteil lässt sich aus "
        f"dem Katalog also nicht ableiten.\n\n"
        '<div class="table-scroll" tabindex="0">\n<table class="bsig-table">\n'
        "<thead><tr><th>Pflichtgrad</th><th>Anforderungen</th>"
        "<th>Aufwand</th></tr></thead>\n<tbody>\n"
        + zeile("MUSS") + "\n" + zeile("SOLLTE") + "\n" + zeile("KANN") + "\n"
        "</tbody>\n</table>\n</div>\n\n"
        f"Budgetspielraum liegt damit unterhalb der Pflicht — und dort steigt "
        f"der Aufwand mit der Freiwilligkeit: **{kann_teuer} der "
        f"{kann_gesamt} KANN-Anforderungen liegen auf der höchsten "
        f"Aufwandsstufe.** Das Teure ist überwiegend das Optionale.\n\n"
        "Die Stufen sind eine BSI-Einschätzung des Umsetzungs- und "
        "Pflegeaufwands, keine Kalkulation. Diese Seite rechnet sie bewusst "
        "nicht in Personentage oder Euro um — das hinge an eurer Größe, "
        "Ausgangslage und Eigenleistung.\n\n"
    )


def render_geschaeftsfuehrung_page(management, themenfelder, groups_by_id):
    all_groups = management + themenfelder
    total = 0
    total_muss = 0
    muss_normal_sdt = 0
    sections = []
    aufwand = {"MUSS": Counter(), "SOLLTE": Counter(), "KANN": Counter()}
    for gid, title, slug, _ in all_groups:
        controls = list(collect_controls(groups_by_id[gid]))
        muss = [c for c in controls if is_muss(c)]
        total += len(controls)
        total_muss += len(muss)
        for c in controls:
            verb = part_prop_value(c, "statement", "modal_verb")
            if verb in aufwand:
                aufwand[verb][prop_value(c, "effort_level")] += 1
        muss_normal_sdt += sum(1 for c in muss if prop_value(c, "sec_level") == "normal-SdT")
        if muss:
            sections.append(render_muss_table(gid, title, slug, muss))

    lines = [
        "---\n",
        f"title: {yaml_quote('Für Geschäftsführung')}\n",
        f"description: {yaml_quote('Pflicht-Anforderungen, Einstufungskriterien und Haftungsrahmen auf einen Blick.')}\n",
        "---\n\n",
        "\n",
        pagefind_section("Rolle"),
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
        "Das BSI-Gesetz (BSIG, in Kraft seit 6.12.2025) unterscheidet zwei "
        "Kategorien nach § 28 BSIG.\n\n"
        "**Unabhängig von der Größe besonders wichtig** sind Betreiber:innen "
        "kritischer Anlagen (KRITIS), qualifizierte Vertrauensdiensteanbieter, "
        "Top-Level-Domain-Registries und DNS-Diensteanbieter.\n\n"
        "Für alle anderen entscheiden Größe und Sektor. Die Operatoren stehen "
        "in den Spaltenköpfen: es zählt die Beschäftigtenzahl **oder** beide "
        "Finanzkennzahlen zusammen.\n\n"
        # Vorher als Fließtext mit verschachtelter Und/Oder-Bedingung. Eine
        # Geschaeftsfuehrung liest das einmal quer und will dann wissen "bin
        # ich drin" -- dafuer muss man die Logik im Kopf rueckwaerts aufloesen.
        # In der Tabelle liest man nur die eigene Zeile ab. Bewusst keine
        # Rechenhilfe mit Eingabefeld: die Seite stuft nicht ein (ADR-0007,
        # siehe rollen/geschaeftsfuehrung), sie legt die Kriterien nur so hin, dass man
        # sie selbst anwenden kann.
        '<div class="table-scroll" tabindex="0">\n'
        '<table class="bsig-table">\n'
        "<thead><tr><th>Kategorie</th><th>Beschäftigte</th>"
        "<th>oder Jahresumsatz</th><th>und Jahresbilanzsumme</th>"
        "<th>Sektor</th></tr></thead>\n<tbody>\n"
        "<tr><td><strong>Besonders wichtige Einrichtung</strong></td>"
        "<td>ab 250</td><td>über 50 Mio. €</td><td>über 43 Mio. €</td>"
        "<td>Anlage 1 BSIG</td></tr>\n"
        "<tr><td><strong>Wichtige Einrichtung</strong></td>"
        "<td>ab 50</td><td>über 10 Mio. €</td><td>über 10 Mio. €</td>"
        "<td>Anlage 1 oder 2 BSIG</td></tr>\n"
        "</tbody>\n</table>\n</div>\n\n"
        "Kleinere Einrichtungen außerhalb kritischer Sektoren fallen in der "
        "Regel nicht darunter. Diese Kriterien ersetzen keine "
        "Schutzbedarfsfeststellung — sie helfen nur bei der ersten "
        "Einordnung mit euren eigenen Zahlen.\n\n"
        # Ergaenzt 2026-10-14 nach Abgleich mit dem BSIG-Wortlaut und der
        # BSI-FAQ (siehe die englische Seite operating-in-germany.mdx, dort
        # dieselben Fundstellen). Vorher fehlten Konzernzaehlung,
        # Zustaendigkeit und die Ausnahmen aus § 28 Abs. 5-7 -- letztere
        # betreffen § 38 direkt, also genau die Pflicht, um die es auf dieser
        # Seite geht.
        "**Zuständigkeit.** Das BSI ist zuständig für besonders wichtige und "
        "wichtige Einrichtungen, die in Deutschland niedergelassen sind "
        "(§ 59 BSIG). Was „niedergelassen“ bedeutet, definiert das Gesetz "
        "nicht.\n\n"
        "**Zählweise im Konzern.** Beschäftigte, Umsatz und Bilanzsumme "
        "richten sich nach der EU-Empfehlung 2003/361/EG; Daten von Partner- "
        "und verbundenen Unternehmen werden hinzugerechnet, nach Auskunft des "
        "BSI auch von solchen außerhalb Deutschlands und der EU. Ausgenommen "
        "sind Einrichtungen, die bei Betrieb und Beschaffenheit ihrer "
        "IT-Systeme, -Komponenten und -Prozesse unabhängig sind (§ 28 Abs. 4 "
        "BSIG). Erfüllen Mutter und Tochter mit gemeinsamer IT gemeinsam die "
        "Schwellen, gelten nach der BSI-FAQ beide als betroffen, vorbehaltlich "
        "dieser Ausnahme.\n\n"
        "**Ausnahmen.** Die §§ 30, 31, 32, 35, 36, 38 und 39 BSIG gelten nicht "
        "für Finanzunternehmen im Sinne von Art. 2 Abs. 2 DORA und bestimmte "
        "weitere Einrichtungen (§ 28 Abs. 5–7 BSIG). Prüft das für eure "
        "Branche.\n\n"
        "Ob ihr betroffen seid, bewertet ihr selbst; das BSI teilt es nicht "
        "mit (BSI-FAQ).\n\n"
        "*Primärquellen: [§§ 28, 59 BSIG](https://www.gesetze-im-internet.de/bsig_2025/BJNR12D0B0025.html), "
        "[BSI NIS-2-FAQ](https://www.bsi.bund.de/DE/Themen/Regulierte-Wirtschaft/NIS-2-regulierte-Unternehmen/NIS-2-FAQ/NIS-2-FAQ-allgemein/FAQ-zu-NIS-2.html).*\n\n",
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
        "Jahre), für die AG § 93 AktG. Dort liegt keine Pflichtverletzung vor, "
        "wenn das Vorstandsmitglied \"bei einer unternehmerischen Entscheidung "
        "vernünftigerweise annehmen durfte, auf der Grundlage angemessener "
        "Information zum Wohle der Gesellschaft zu handeln\" (Business "
        "Judgment Rule, Abs. 1 Satz 2). Bei Streit über die Sorgfalt trifft "
        "die Vorstandsmitglieder die Beweislast (Abs. 2 Satz 2), eine "
        "nachvollziehbare Dokumentation ist deshalb praktisch wichtig. Ob die "
        "Regel auch ein Absehen von einer gesetzlichen Pflicht wie § 38 BSIG "
        "deckt, sagt der Gesetzestext nicht; das ist eine Auslegungsfrage für "
        "die Rechtsberatung. Ein anerkannter, öffentlich nachvollziehbarer "
        "Katalog wie Grundschutz++ kann helfen, die Auswahl und Umsetzung von "
        "Maßnahmen zu begründen, ist aber keine Garantie gegen Haftung.\n\n"
        "*Primärquellen: [§ 43 GmbHG](https://www.gesetze-im-internet.de/gmbhg/__43.html), "
        "[§ 93 AktG](https://www.gesetze-im-internet.de/aktg/__93.html).*\n\n",
        render_aufwand_section(aufwand),
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
        # Ein Filter nach Sicherheitsstufe stand hier, solange es MUSS in beiden
        # Stufen geben konnte. Im Katalog ist jede MUSS-Anforderung normal-SdT:
        # "Standard" filterte nichts, "erhoeht" blendete die ganze Seite aus.
        f"**Standard-Sicherheitsstufe** (Stand der Technik) — der Basisschutz, der "
        f"unabhängig vom individuellen Schutzbedarf für praktisch jede Einrichtung gilt. "
        f"{muss_normal_sdt} von {total_muss} MUSS-Anforderungen im Katalog haben diese Stufe.\n\n",
        "## Die MUSS-Anforderungen nach Bereich\n\n",
        *sections,
    ]
    ROLLEN_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (ROLLEN_OUT_DIR / "geschaeftsfuehrung.mdx").write_text("".join(lines))


# Reihenfolge des tatsächlichen PDCA-Ablaufs -- weicht von der Katalog-Reihenfolge ab (dort
# steht VRB vor PERF), siehe PdcaCycle.astro. Grafik und Liste auf rollen/isb.mdx nehmen
# dieselbe, damit "dieselben sechs Praktiken als Liste" auch dieselbe Reihenfolge heißt.
PDCA_SEQUENCE = ["GC", "STM", "UMS", "PERF", "VRB"]


def render_pdca_cycle_prop(management, groups_by_id):
    by_id = {gid: (title, slug) for gid, title, slug, _ in management}

    def node(gid):
        title, slug = by_id[gid]
        count = len(list(collect_controls(groups_by_id[gid])))
        return f"{{ id: {jsx_string(gid)}, title: {jsx_string(title)}, slug: {jsx_string(slug)}, count: {count} }}"

    nodes = "[" + ", ".join(node(gid) for gid in PDCA_SEQUENCE) + "]"
    risk = node("RISK")
    return nodes, risk


def render_isb_page(management, groups_by_id):
    entries = []
    for gid, title, slug, summary in sorted(management, key=lambda m: (PDCA_SEQUENCE + ["RISK"]).index(m[0])):
        count = len(list(collect_controls(groups_by_id[gid])))
        entries.append((gid, title, slug, f"{summary} ({count} Anforderungen)"))

    nodes_prop, risk_prop = render_pdca_cycle_prop(management, groups_by_id)

    lines = [
        "---\n"
        + "title: "
        + yaml_quote("Für ISB")
        + "\n"
        + "description: "
        + yaml_quote(
            "Der BSI-OSCAL-Katalog als PDCA-Zyklus für den ISB-Alltag: Vorgänger-Mapping zum alten Kompendium, Basisgefährdungen direkt am Text, Status und Zeitplan."
        )
        + "\n---\n\n",
        PDCA_CYCLE_IMPORT,
        "\n",
        pagefind_section("Rolle"),
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
        "- **[Export für Excel](/export/)** — alle Anforderungen oder deine "
        "Auswahl als Excel-Datei, mit Spalten für Status, Verantwortliche und "
        "Frist und einer Übersicht der Dokumente, die der Katalog nennt.\n"
        "- **[Dokumente im Katalog](/dokumente/)** — welche Dokumenttypen der "
        "Katalog nennt, mit der Beschreibung des BSI und den Anforderungen dahinter.\n"
        "- **[Anforderungen nach Zielobjektkategorie](/zielobjekte/)** — je "
        "Kategorie, was gilt: direkt und von übergeordneten Kategorien geerbt, "
        "dazu die Dokumente, die diese Anforderungen nennen.\n"
        "- **[Vergleich: Altes Kompendium ↔ Grundschutz++](/vergleich/)** — "
        "jede Zuordnung zwischen alter und neuer Anforderung, mit "
        f"Beziehungstyp ({'/'.join(RELATIONSHIP_LABELS.values())}) und "
        "echten Links zu den Baustein-PDFs des BSI.\n"
        "- **Basisgefährdungen direkt am Control** — jede Anforderung zeigt "
        "die zugeordneten elementaren Gefährdungen (BSI, 47 Stück) als "
        "hoverbare Pille, ohne extra Nachschlagen in `basethreats.csv`.\n"
        "- **[Status & Zeitplan](/grundschutzpp/zeitplan/)** — Meilensteinplan "
        "des BSI, Übergangszeit, Zertifizierung.\n"
        "- **[Änderungen am Katalog](/aenderungen/)** — was das BSI zwischen "
        "zwei veröffentlichten Ständen an den Anforderungen geändert hat, mit "
        "altem und neuem Wortlaut.\n\n"
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
        "---\n"
        + "title: "
        + yaml_quote("Für Devs")
        + "\n"
        + "description: "
        + yaml_quote(
            "Alle operativen Themenfelder von Grundschutz++ für Entwicklung und Betrieb, mit Pflichtgrad, Sicherheitsstufe, Aufwand und Basisgefährdungen direkt am Anforderungstext."
        )
        + "\n---\n\n",
        pagefind_section("Rolle"),
        "Jede Anforderung zeigt Pflichtgrad, Sicherheitsstufe, "
        "Aufwandsschätzung und zugeordnete Basisgefährdungen direkt am "
        "Text, als Badges mit Hover-Erklärung — keine ISMS-Prozess-"
        "Erklärung davor, kein Umweg über das Managementsystem.\n\n"
        "Für eigene Werkzeuge gibt es den Katalog auch als "
        "[Daten für Sprachmodelle (RAG)](/rag/) und als "
        "[Tabelle (CSV oder Excel)](/export/), auch je Praktik.\n\n"
        "Du betreibst ein bestimmtes System, zum Beispiel einen Webserver oder Cloud-Dienste? "
        "Dann sortiere nach [Zielobjektkategorie](/zielobjekte/): je Kategorie die "
        "Anforderungen, direkt und geerbt, dazu die [Dokumente](/dokumente/) "
        "(zum Beispiel Betriebskonzept oder Konfigurationshistorie), in denen der Katalog "
        "die Ergebnisse festhalten lässt.\n\n",
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


# Angaben der BSI-Mapping-Datei zu sich selbst, von main() gefuellt
# (read_mapping_info). Die Vergleichsseiten legen offen, dass das BSI die Datei
# als Entwurf kennzeichnet -- der Hinweis entfaellt von selbst, sobald dort
# kein "draft" mehr steht.
MAPPING_INFO = {"draft": False, "stand": "", "defaulted": set(), "defaulted_types": set()}


def de_date(iso):
    """"2026-07-21" -> "21.07.2026"; unveraendert, wenn es kein ISO-Datum ist."""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", iso or "")
    return f"{m.group(3)}.{m.group(2)}.{m.group(1)}" if m else (iso or "")


def read_mapping_info(mapping_data):
    """Status, Stand und als Standardwert markierte Zuordnungen der Mapping-Datei.

    Quelle: provenance.status bzw. status je Gruppe ("draft"), metadata.
    last-modified, und die Eigenschaft relationship_defaulted je Zuordnung.
    Wie das BSI die Eigenschaft meint, steht im Repo nirgends; die Seiten
    sagen das und nennen nur, was in der Datei steht.
    """
    coll = mapping_data["mapping-collection"]
    status = {g.get("status") for g in coll.get("mappings", [])}
    status.add((coll.get("provenance") or {}).get("status"))
    defaulted, types = set(), set()
    for group in coll.get("mappings", []):
        for m in group.get("maps", []):
            if any(p.get("name") == "relationship_defaulted" and p.get("value") == "true" for p in m.get("props", [])):
                src = m["sources"][0]["id-ref"]
                tgt = m["targets"][0]["id-ref"]
                defaulted.add((src, tgt))
                types.add(m.get("relationship"))
    MAPPING_INFO.update(
        draft="draft" in status,
        stand=de_date(((coll.get("metadata") or {}).get("last-modified") or "")[:10]),
        defaulted=defaulted,
        defaulted_types=types,
    )


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


def render_baustein_summary(entries, group_titles):
    """Zusammenfassung aus den Mapping-Daten -- Zahlen, kein Fremdtext.

    Die Baustein-Seiten bestanden vorher nur aus Einleitung + Tabelle und
    waren bei 95 Seiten nach identischem Muster dünn. Die Zusammenfassung
    beantwortet in Klartext, was die Tabelle zeigt: wie viel des alten
    Bausteins direkt weiterlebt und in welchen Themenfeldern es landet.
    Nur Zahlen und Titel aus dem neuen Katalog (ADR-0005: kein alter Volltext).
    """
    def pl(n, sing, plur):
        return f"{n} {sing if n == 1 else plur}"

    rel_counts = {}
    for _, rel, _ in entries:
        rel_counts[rel] = rel_counts.get(rel, 0) + 1
    # Die Zaehlung ist je Zuordnung (eine alte Anforderung kann mehrere neue
    # haben und umgekehrt) -- die Saetze duerfen deshalb nicht so tun, als
    # waeren es Anforderungen.
    rel_phrases = {
        "equal-to": "identisch",
        "equivalent-to": "inhaltlich gleichwertig",
        "subset-of": "alte Anforderung ist Teilbereich der neuen",
        "superset-of": "alte Anforderung umfasst mehr als die neue",
        "intersects-with": "teilweise Überschneidung",
    }
    parts = [f"{rel_phrases[rel]}: {rel_counts[rel]}" for rel in RELATIONSHIP_LABELS if rel in rel_counts]
    new_ids = {new_id for _, _, new_id in entries}
    old_ids = {old_id for old_id, _, _ in entries}
    per_field = {}
    for new_id in new_ids:
        field = new_id.split(".")[0]
        per_field[field] = per_field.get(field, 0) + 1
    fields = ", ".join(
        f"[{fid} {group_titles[fid]}](/grundschutzpp/{fid.lower()}/) ({n})"
        if fid in group_titles
        else f"{fid} ({n})"
        for fid, n in sorted(per_field.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    return (
        f"Das Mapping enthält {pl(len(entries), 'Zuordnung', 'Zuordnungen')} "
        "(eine alte Anforderung kann mehreren neuen entsprechen und umgekehrt). "
        f"Nach Beziehungstyp: {'; '.join(parts)}. "
        f"Die neuen Anforderungen liegen in diesen Themenfeldern (Anzahl in Klammern): {fields}.\n"
    )


def render_baustein_siblings(baustein_id, by_baustein, baustein_links):
    """Weitere Bausteine derselben Kompendium-Schicht -- interne Verlinkung."""
    layer_id = baustein_id.split(".")[0]
    siblings = sorted(b for b in by_baustein if b.split(".")[0] == layer_id and b != baustein_id)
    if not siblings:
        return ""
    layer_name = KOMPENDIUM_LAYERS.get(layer_id, layer_id)
    items = [
        f"- [{b} {baustein_title(b, baustein_links.get(b))}](/vergleich/{baustein_slug(b)}/)\n"
        for b in siblings
    ]
    return f"## Weitere Bausteine der Schicht {layer_id} {layer_name}\n\n" + "".join(items)


def baustein_search_title(full_name):
    return f"{full_name}: Nachfolge in Grundschutz++"


def baustein_description(full_name, count):
    noun = "Zuordnung" if count == 1 else "Zuordnungen"
    return (
        f"{full_name}: {count} {noun} zur Nachfolge in Grundschutz++ "
        "nach dem BSI-Mapping, je mit Beziehungstyp."
    )


def baustein_lead(full_name, layer, entries, group_titles):
    """Erster Absatz einer Baustein-Seite: die Antwort auf "wo steht das jetzt?".

    Wer ueber eine Suche nach der alten ID kommt, will zuerst das Ergebnis
    (wohin ist der Baustein gegangen), nicht die Herleitung. Die Zahlen sind
    dieselben wie in baustein_description() und der Tabelle darunter.
    """
    def pl(n, sing, plur):
        return f"{n} {sing if n == 1 else plur}"

    old_ids = {old for old, _, _ in entries}
    new_ids = {new for _, _, new in entries}
    per_field = {}
    for new_id in new_ids:
        field = new_id.split(".")[0]
        per_field[field] = per_field.get(field, 0) + 1
    ranked = sorted(per_field.items(), key=lambda kv: (-kv[1], kv[0]))

    def field_link(fid):
        if fid in group_titles:
            return f"[{fid} {group_titles[fid]}](/grundschutzpp/{fid.lower()}/)"
        return fid

    top_id, top_n = ranked[0]
    if len(ranked) == 1:
        where = f"im Themenfeld {field_link(top_id)}"
    elif top_n * 2 > len(new_ids):
        where = f"die meisten davon in {field_link(top_id)} ({top_n})"
    else:
        where = f"verteilt auf {len(ranked)} Themenfelder, am häufigsten {field_link(top_id)} ({top_n})"
    return (
        f"**{full_name}**"
        + (f" (Schicht {layer}, Edition 2023)" if layer else " (Edition 2023)")
        + f": Das BSI-Mapping verbindet {pl(len(old_ids), 'alte Anforderung', 'alte Anforderungen')} "
        f"dieses Bausteins mit {pl(len(new_ids), 'Grundschutz++-Anforderung', 'Grundschutz++-Anforderungen')}, {where}.\n"
    )


MAPPING_NOTE_ANCHOR = "stand-der-mapping-datei"


def render_mapping_note(entries):
    """Kurzer Hinweis unter dem Seitenkopf: Entwurfsstatus und markierte Zeilen.

    Leer, wenn das BSI die Datei nicht mehr als Entwurf fuehrt.
    """
    if not MAPPING_INFO["draft"]:
        return ""
    stand = MAPPING_INFO["stand"]
    text = (
        "Die Mapping-Datei des BSI ist in ihren Metadaten als Entwurf gekennzeichnet"
        + (f" (Stand {stand})" if stand else "")
        + f'. <a href="/vergleich/#{MAPPING_NOTE_ANCHOR}">Mehr dazu</a>.'
    )
    n_default = sum(1 for old, _rel, new in entries if (old, new) in MAPPING_INFO["defaulted"])
    if n_default:
        text += (
            f" Bei {n_default} von {len(entries)} Zuordnungen dieses Bausteins ist der "
            "Beziehungstyp in der Datei als Standardwert markiert (in der Tabelle mit * gekennzeichnet)."
        )
    return f'<p class="mapping-note">{text}</p>\n\n'


def render_mapping_notice(by_baustein, baustein_links, total):
    """Ausfuehrlicher Hinweis auf /vergleich/: was die Datei ueber sich selbst sagt."""
    if not MAPPING_INFO["draft"]:
        return ""
    stand = MAPPING_INFO["stand"]
    n_default = len(MAPPING_INFO["defaulted"])
    ohne = len(baustein_links) - len(by_baustein)
    parts = [
        "Das BSI kennzeichnet die Mapping-Datei in ihren Metadaten als Entwurf "
        "(<code>status: draft</code>"
        + (f", Stand {stand}" if stand else "")
        + f"). Für {ohne} der {len(baustein_links)} Bausteine enthält sie keine Zuordnung"
    ]
    if n_default:
        typen = MAPPING_INFO["defaulted_types"]
        parts.append(
            f", und bei {n_default} der {total} Zuordnungen ist der Beziehungstyp in der "
            "Datei als Standardwert markiert (<code>relationship_defaulted</code>"
            + (
                f"; alle haben den Typ „{relationship_label(next(iter(typen)))}“"
                if len(typen) == 1
                else ""
            )
            + "). Auf den Baustein-Seiten sind diese Zeilen mit * gekennzeichnet"
        )
    parts.append(
        ". Wir lesen das so, dass der Typ dort nicht einzeln bewertet wurde; eine "
        "Beschreibung der Eigenschaft haben wir beim BSI nicht gefunden. Wir geben "
        "die Datei so wieder, wie das BSI sie veröffentlicht hat, und haben sie nicht korrigiert."
    )
    return (
        f'<aside class="mapping-notice" id="{MAPPING_NOTE_ANCHOR}">\n'
        "<strong>Stand der Mapping-Datei</strong>\n"
        f"<p>{''.join(parts)}</p>\n"
        "</aside>\n\n"
    )


def render_baustein_page(baustein_id, entries, baustein_links, control_index, group_titles, by_baustein):
    pdf = baustein_links.get(baustein_id)
    title = baustein_title(baustein_id, pdf)
    full_name = f"{baustein_id} {title}".strip()
    layer = KOMPENDIUM_LAYERS.get(baustein_id.split(".")[0], "")

    pdf_sentence = (
        f' Den alten Baustein gibt es beim BSI als <a href="{pdf}" target="_blank" '
        f'rel="noopener noreferrer">PDF</a>.'
        if pdf
        else ""
    )

    lines = [
        "---\n",
        f"title: {yaml_quote(full_name)}\n",
        f"description: {yaml_quote(baustein_description(full_name, len(entries)))}\n",
        # <title> für die Suchergebnisse; Überschrift und Seitenleiste behalten
        # den kurzen Titel. Suchende tippen die alte Baustein-ID.
        "head:\n",
        "  - tag: title\n",
        f"    content: {yaml_quote(baustein_search_title(full_name))}\n",
        "---\n",
        "\n",
        pagefind_section("Vergleich"),
        baustein_lead(full_name, layer, entries, group_titles),
        "\n",
        # Quelle: BSI, Seite "IT-Grundschutz" (Stand 2026-10-18), wörtlich
        # "bleibt in der mehrjährigen Übergangszeit anwendbar". Kein Enddatum
        # nennen, das BSI nennt keins (siehe TIMELINE).
        "Der bisherige IT-Grundschutz bleibt laut BSI in einer „mehrjährigen "
        "Übergangszeit“ anwendbar; die Termine des BSI stehen im "
        "[Status & Zeitplan](/grundschutzpp/zeitplan/)." + pdf_sentence + "\n",
        "\n",
        render_mapping_note(entries),
        render_baustein_summary(entries, group_titles),
        "\n",
        '<div class="vergleich-section not-content">\n',
        '<div class="table-scroll" tabindex="0">\n',
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
        # Als Standardwert markierte Zuordnungen: Marker am Badge selbst
        # (data-defaulted, der Stern kommt per CSS). Ein "*" im Text liest MDX
        # als Markdown-Hervorhebung und zerreisst die Tabelle ueber mehrere
        # Zeilen; ein eigenes Element neben dem Badge rutscht in eine zweite
        # Zeile und macht diese Zeilen hoeher.
        if (old_id, new_id) in MAPPING_INFO["defaulted"]:
            badge = (
                f'<span class="rel-badge" data-rel="{rel}" data-defaulted="true" '
                'title="In der BSI-Datei als Standardwert markiert (relationship_defaulted)" '
                f'aria-label="{relationship_label(rel)}, in der BSI-Datei als Standardwert markiert">'
                f"{relationship_label(rel)}</span>"
            )
        else:
            badge = f'<span class="rel-badge" data-rel="{rel}">{relationship_label(rel)}</span>'
        lines.append(
            f"<tr><td>{old_cell}</td>"
            f"<td>{badge}</td>"
            f"<td>{control_link(new_id, control_index)}</td></tr>\n"
        )
    lines += [
        "</tbody>\n",
        "</table>\n",
        "</div>\n",
        "</div>\n",
        "\n",
        render_baustein_siblings(baustein_id, by_baustein, baustein_links),
        "\n",
        "[Alle Bausteine im Überblick](/vergleich/)\n",
        "\n",
        "Der alte Anforderungstext steht hier bewusst nicht, nur die Zuordnung "
        "nach der offiziellen BSI-Mapping-Datei "
        "(siehe [ADR-0005](https://github.com/grundschutz-docs/docs/blob/main/adr/0005-vorgaenger-anforderung-alt-neu.md)).\n",
    ]
    return "".join(lines)


RELATIONSHIP_HINTS = {
    "equal-to": "Dieselbe Anforderung wie die alte – höchstens in Schreibweise oder Grammatik verschieden.",
    "equivalent-to": "Inhaltlich deckungsgleich mit der alten Anforderung.",
    "subset-of": "Die alte Anforderung ist in der neuen vollständig enthalten – die neue deckt zusätzlich mehr ab.",
    "superset-of": "Die alte Anforderung deckte mehr ab als die neue – die neue erfasst nur einen Teilaspekt davon.",
    "intersects-with": "Alte und neue Anforderung überschneiden sich nur teilweise.",
}


# Kein Thema im engeren Sinn: laut tags.csv markiert der Tag Anforderungen, die
# in eine Produktbeschreibung gehoeren. Er steht auf der Themen-Seite trotzdem
# (die Pille auf den Katalogseiten verlinkt dorthin), aber getrennt am Ende.
KEIN_THEMA_TAGS = {"Produktbeschreibung"}


def collect_tag_index(catalog):
    """Tag -> [(id, titel, modalverb)] sowie Zahlen je Praktik.

    Zweiter, eigener Zaehlweg gegenueber render_tags_prop(): check_invariants()
    vergleicht die geschriebene Seite mit genau dieser Auswertung.
    """
    by_tag = {}
    tagged = set()
    total_by_practice = {}
    tagged_by_practice = {}
    for control in collect_controls(catalog):
        practice = control["id"].split(".")[0]
        total_by_practice[practice] = total_by_practice.get(practice, 0) + 1
        value = prop_value(control, "tags")
        names = [t.strip() for t in value.split(",") if t.strip()] if value else []
        if not names:
            continue
        tagged.add(control["id"])
        tagged_by_practice[practice] = tagged_by_practice.get(practice, 0) + 1
        for name in names:
            by_tag.setdefault(name, []).append(
                (control["id"], control.get("title", ""), part_prop_value(control, "statement", "modal_verb") or "")
            )
    return by_tag, tagged, total_by_practice, tagged_by_practice


def render_themen_page(catalog, control_index, tags_by_id):
    by_tag, tagged, total_by_practice, tagged_by_practice = collect_tag_index(catalog)
    total = sum(total_by_practice.values())

    slugs = {}
    for name in by_tag:
        slugs.setdefault(tag_slug(name), []).append(name)
    kollision = {k: v for k, v in slugs.items() if len(v) > 1}
    if kollision:
        raise SystemExit(f"Themen-Tags mit gleichem Anker: {kollision}")

    def sort_key(name):
        return name.casefold()

    themen = sorted((n for n in by_tag if n not in KEIN_THEMA_TAGS), key=sort_key)
    kein_thema = sorted((n for n in by_tag if n in KEIN_THEMA_TAGS), key=sort_key)

    anteile = {
        pid: round(100 * tagged_by_practice.get(pid, 0) / total_by_practice[pid])
        for pid in total_by_practice
    }
    low_value, high_value = min(anteile.values()), max(anteile.values())
    low = ", ".join(sorted(k for k, v in anteile.items() if v == low_value))
    high = ", ".join(sorted(k for k, v in anteile.items() if v == high_value))

    def section(name):
        rows = sorted(by_tag[name])
        lines = [f"## {name} {heading_anchor(tag_slug(name))}\n"]
        meta = [f"{len(rows)} Anforderungen" if len(rows) != 1 else "1 Anforderung"]
        syn = TAG_SYNONYMS.get(name)
        if syn:
            meta.append(f"verwandte Begriffe: {mdx_safe(syn)}")
        lines.append(f'<p class="themen-meta">{" · ".join(meta)}</p>\n')
        hint = tags_by_id.get(name)
        if hint:
            lines.append(f"{mdx_safe(hint)}\n")
        lines.append('<div data-pagefind-ignore>')
        lines.append('<table class="vergleich-table themen-table">')
        lines.append("<thead><tr><th>Anforderung</th><th>Pflicht</th></tr></thead>\n<tbody>")
        for cid, title, verb in rows:
            lines.append(
                f"<tr><td>{control_link(cid, control_index)}</td><td>{verb}</td></tr>"
            )
        lines.append("</tbody>\n</table>\n</div>\n")
        return "\n".join(lines)

    def chip(name):
        return (
            f'<li><a href="#{tag_slug(name)}">{name}'
            f'<span class="themen-count">{len(by_tag[name])}</span></a></li>'
        )

    lines = [
        "---\n",
        f"title: {yaml_quote('Themen im Katalog')}\n",
        f"description: {yaml_quote(f'Die {len(by_tag)} Themen-Tags des BSI-Katalogs mit den zugeordneten Anforderungen, von Lieferketten bis Passwortrichtlinie. Die Tags erfassen {len(tagged)} von {total} Anforderungen.')}\n",
        "---\n\n",
        pagefind_section("Themen"),
        "Das BSI versieht einen Teil der Anforderungen mit Themen-Tags. Diese Seite "
        "sammelt sie: je Thema die zugeordneten Anforderungen mit Pflichtgrad. "
        "Dieselben Tags stehen als Pillen an den Anforderungen und als Filter in "
        "der Suche.\n",
        f"**Vollständig ist das nicht.** Nur {len(tagged)} von {total} Anforderungen "
        f"tragen überhaupt einen Tag, und sehr ungleich verteilt: der Anteil je "
        f"Praktik reicht von {low_value} % ({low}) bis {high_value} % ({high}). "
        "Dass eine Anforderung bei einem Thema fehlt, heißt deshalb nicht, dass "
        "sie es nicht betrifft. Für eine vollständige Suche nach einem Begriff "
        "ist die Suche oben besser.\n",
        '<ul class="themen-index" data-pagefind-ignore>',
        *[chip(n) for n in themen],
        "</ul>\n",
        *[section(n) for n in themen],
    ]
    if kein_thema:
        lines.append("## Kein Thema im engeren Sinn {#kein-thema}\n")
        lines.append(
            "Dieser Tag beschreibt keinen Sachverhalt, sondern markiert, welche "
            "Anforderungen in eine Produktbeschreibung gehören. Er steht hier, "
            "weil die Pillen an den Anforderungen auf diese Seite verlinken.\n"
        )
        lines += [section(n) for n in kein_thema]
    (OUT_DIR / "themen.mdx").write_text("\n".join(lines))
    return len(by_tag), len(tagged)


# --- Zielobjekt-Seiten (ADR-0011) ---------------------------------------------
# Eine Seite je Zielobjektkategorie: direkt zugeordnete Anforderungen, dazu die
# von den uebergeordneten Kategorien geerbten (STM.2.1.4.1), gruppiert nach der
# Elternkategorie. Anforderungen ohne Kategorie (immer im Paket, Standard 300-1
# 3.4.1) werden nur gezaehlt. check_zielobjekte() liest die Seiten zurueck und
# rechnet auf zwei anderen Wegen nach.
PFLICHT_REIHENFOLGE = {"MUSS": 0, "SOLLTE": 1, "KANN": 2}


def natural_id_key(control_id):
    """ARCH.2.1.10 nach ARCH.2.1.9: die Zahlen als Zahlen vergleichen."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", control_id)]


def zielobjekt_model(catalog):
    """Je Kategorie: direkt zugeordnete Anforderungen und geerbte, nach Elternkategorie.

    Rueckgabe: (model, ohne_kategorie, controls). model[name] = {"direkt": [ids],
    "geerbt": [(elternname, [ids]), ...] (naechste Elternkategorie zuerst), "kinder": [namen]}.
    """
    controls = {}
    for control in collect_controls(catalog):
        controls[control["id"]] = control
    direkt_von = {cid: control_targets(c) for cid, c in controls.items()}
    ohne = sorted((cid for cid, ks in direkt_von.items() if not ks), key=natural_id_key)

    model = {}
    for name, info in TARGETS.items():
        direkt = [cid for cid, ks in direkt_von.items() if name in ks]
        geerbt, parent, gesehen = [], info["parent"], set()
        while parent and parent not in gesehen:
            gesehen.add(parent)
            ids = [cid for cid, ks in direkt_von.items() if parent in ks and cid not in direkt]
            geerbt.append((parent, ids))
            parent = TARGETS[parent]["parent"]
        model[name] = {
            "direkt": sorted(direkt, key=natural_id_key),
            "geerbt": [(p, sorted(ids, key=natural_id_key)) for p, ids in geerbt],
            "kinder": sorted(n for n, i in TARGETS.items() if i["parent"] == name),
        }
    return model, ohne, controls


def zielobjekt_zahlen(model, name, ohne_anzahl):
    direkt = len(model[name]["direkt"])
    geerbt = sum(len(ids) for _, ids in model[name]["geerbt"])
    return direkt, direkt + geerbt, direkt + geerbt + ohne_anzahl


def render_anforderungs_tabelle(teil, ids, controls, control_index, zusatz):
    """Tabelle der Anforderungen (ID und Titel, Pflicht, Stufe), MUSS zuerst, dann nach ID.
    zusatz(cid) liefert eine kleine Zeile unter dem Titel (oder ""): so bleibt die Tabelle auch
    auf dem Handy bei drei Spalten, statt eine vierte breite Spalte aufzumachen."""
    ids = sorted(
        ids,
        key=lambda cid: (
            PFLICHT_REIHENFOLGE.get(part_prop_value(controls[cid], "statement", "modal_verb"), 9),
            natural_id_key(cid),
        ),
    )
    lines = [
        f'<div class="zielobjekt-teil" data-teil="{attr_escape(teil)}" data-pagefind-ignore>\n',
        '<table class="vergleich-table themen-table anforderungs-tabelle">\n',
        "<thead><tr><th>Anforderung</th><th>Pflicht</th><th>Stufe</th></tr></thead>\n<tbody>\n",
    ]
    for cid in ids:
        control = controls[cid]
        sec_level = prop_value(control, "sec_level") or ""
        zeile = zusatz(cid)
        lines.append(
            f'<tr data-sec="{attr_escape(sec_level)}" data-id="{cid}">'
            f"<td>{control_link(cid, control_index)}"
            + (f' <span class="zeile-zusatz">{zeile}</span>' if zeile else "")
            + "</td>"
            f'<td>{part_prop_value(control, "statement", "modal_verb") or ""}</td>'
            # Auf dem Handy steht nur "Standard"/"Erhöht" (CSS), am Desktop das volle Wort des BSI.
            f'<td><span class="stufe-lang">{SEC_LEVEL_LABELS.get(sec_level, sec_level)}</span>'
            f'<span class="stufe-kurz">{SEC_LEVEL_KURZ.get(sec_level, sec_level)}</span></td></tr>\n'
        )
    lines.append("</tbody>\n</table>\n</div>\n")
    return "".join(lines)


def render_zielobjekt_table(teil, ids, controls, control_index, direkt_von, bezug):
    # bezug: die Kategorie, derentwegen die Anforderung in dieser Tabelle steht (die Seite selbst
    # oder die Elternkategorie); "auch fuer" nennt die jeweils andere. Bei zwei Kategorien (39
    # Anforderungen) sagt der Katalog nicht, ob "oder" oder "und" gemeint ist; die Seite nennt
    # die zweite Kategorie, damit das sichtbar bleibt.
    def zusatz(cid):
        auch = [k for k in direkt_von[cid] if k != bezug]
        if len(direkt_von[cid]) <= 1:
            return ""
        # Als HTML-Link: die Zeile steht in einer HTML-Tabelle, dort wird Markdown nicht gelesen.
        links = ", ".join(f'<a href="/zielobjekte/{tag_slug(k)}/">{mdx_safe(k)}</a>' for k in auch)
        return f"(auch für {links})"

    return render_anforderungs_tabelle(teil, ids, controls, control_index, zusatz)


def render_zielobjekt_pages(catalog, control_index):
    slugs = {}
    for name in TARGETS:
        slugs.setdefault(tag_slug(name), []).append(name)
    kollision = {k: v for k, v in slugs.items() if len(v) > 1}
    if kollision:
        raise SystemExit(f"Zielobjektkategorien mit gleicher Adresse: {kollision}")

    model, ohne, controls = zielobjekt_model(catalog)
    direkt_von = {cid: control_targets(c) for cid, c in controls.items()}
    ZIELOBJEKTE_OUT_DIR.mkdir(parents=True, exist_ok=True)
    for alt in ZIELOBJEKTE_OUT_DIR.glob("*.mdx"):
        alt.unlink()

    def plural(n):
        return "1 Anforderung" if n == 1 else f"{n} Anforderungen"

    for name, info in TARGETS.items():
        m = model[name]
        direkt, mit_vererbung, gesamt = zielobjekt_zahlen(model, name, len(ohne))
        definition = first_sentence(info["definition"])
        lines = [
            "---\n",
            f"title: {yaml_quote(f'Anforderungen für {name}')}\n",
            f"description: {yaml_quote(f'Alle Grundschutz++-Anforderungen für die Zielobjektkategorie {name}: {direkt} direkt zugeordnet, {mit_vererbung} mit den geerbten der übergeordneten Kategorien.')}\n",
            "---\n\n",
            pagefind_section("Zielobjekt"),
        ]
        if definition:
            lines.append(f"{mdx_safe(definition)}\n")
        if info["synonyms"]:
            lines.append(f"Auch genannt: {mdx_safe(info['synonyms'])}.\n")
        if info["example"]:
            lines.append(f"Beispiele: {mdx_safe(info['example'])}.\n")
        if info["parent"]:
            lines.append(f"Teil von [{info['parent']}](/zielobjekte/{tag_slug(info['parent'])}/).\n")
        lines.append(
            f"**{plural(mit_vererbung)}** gelten für ein Asset dieser Kategorie: "
            f"{direkt} direkt zugeordnet"
            + (f", {mit_vererbung - direkt} geerbt" if info["parent"] else "")
            + f". Dazu kommen die {len(ohne)} Anforderungen ohne Zielobjektkategorie, "
            f"die in jedes Anforderungspaket gehören: **zusammen {gesamt}**. "
            "Nach [STM.2.1.4.1](/grundschutzpp/stm/#STM.2.1.4.1) erhält ein Asset auch die "
            "Kategorien über seiner eigenen, [so rechnet die Übersicht](/zielobjekte/).\n"
        )
        lines.append(
            f"**Dieses Paket weitergeben:** [Im Export öffnen](/export/?ziel={urllib.parse.quote(name, safe='')}) "
            "als Excel, CSV oder Checkliste für Tickets und Wikis. Dort lassen sich weitere Kategorien dazunehmen.\n"
        )
        if m["kinder"]:
            kinder = ", ".join(f"[{k}](/zielobjekte/{tag_slug(k)}/)" for k in m["kinder"])
            lines.append(
                f"Unterkategorien: {kinder}. Deren eigene Anforderungen stehen nicht hier, "
                "sie gelten nur für die jeweilige Unterkategorie.\n"
            )
        # ADR-0011: der Katalog laesst offen, ob bei zwei Kategorien "oder" oder "und" gemeint
        # ist; jede Seite mit solchen Zeilen sagt, dass das unsere Lesart ist.
        if any(len(direkt_von[cid]) > 1 for cid in list(m["direkt"]) + [c for _, ids in m["geerbt"] for c in ids]):
            lines.append(
                "Anforderungen mit zwei Kategorien stehen bei beiden. Der Katalog sagt nicht, ob „oder“ oder "
                "„und“ gemeint ist; wir lesen es als „oder“. Das ist unsere Lesart, keine Aussage des BSI.\n"
            )
        lines.append(f"## Direkt zugeordnet ({direkt}) {heading_anchor('direkt')}\n")
        if m["direkt"]:
            lines.append(render_zielobjekt_table("direkt", m["direkt"], controls, control_index, direkt_von, name))
        else:
            lines.append("Keine Anforderung nennt diese Kategorie direkt.\n")
        for parent, ids in m["geerbt"]:
            lines.append(
                f"## Geerbt von {parent} ({len(ids)}) {heading_anchor('geerbt-' + tag_slug(parent))}\n"
            )
            lines.append(
                f"Gilt für ein Asset dieser Kategorie, weil {name} unter "
                f"[{parent}](/zielobjekte/{tag_slug(parent)}/) steht.\n"
            )
            lines.append(render_zielobjekt_table(f"geerbt:{parent}", ids, controls, control_index, direkt_von, parent))
        # Dokumente, die die Anforderungen dieser Kategorie (direkt und geerbt) nennen (ADR-0012).
        alle_ids = list(m["direkt"]) + [cid for _, ids in m["geerbt"] for cid in ids]
        dokus = {}
        for cid in alle_ids:
            d = part_prop_value(controls[cid], "statement", "documentation")
            if d:
                z = dokus.setdefault(d, [0, 0])
                z[0] += 1
                z[1] += part_prop_value(controls[cid], "statement", "modal_verb") == "MUSS"
        if dokus:
            lines.append(f"## Dokumente zu diesen Anforderungen ({len(dokus)}) {heading_anchor('dokumente')}\n")
            lines.append(
                f"Diese Anforderungen nennen {len(dokus)} Dokumenttypen, in denen das Ergebnis festzuhalten ist. "
                "Die Anforderungen ohne Zielobjektkategorie und die der Methodik-Praktiken nennen weitere, "
                "alle stehen unter [Dokumente im Katalog](/dokumente/).\n"
            )
            lines.append('<div data-pagefind-ignore>\n<table class="vergleich-table zahlen-tabelle" data-dokumente="zielobjekt">\n')
            lines.append("<thead><tr><th>Dokument</th><th>Anforderungen</th><th>davon MUSS</th></tr></thead>\n<tbody>\n")
            for dname, (anz, mus) in sorted(dokus.items(), key=lambda kv: (-kv[1][1], -kv[1][0], kv[0].casefold())):
                lines.append(
                    f'<tr data-slug="{tag_slug(dname)}"><td><a href="/dokumente/{tag_slug(dname)}/">{mdx_safe(dname)}</a></td>'
                    f"<td>{anz}</td><td>{mus}</td></tr>\n"
                )
            lines.append("</tbody>\n</table>\n</div>\n")
        lines.append(f"## Ohne Zielobjektkategorie ({len(ohne)}) {heading_anchor('ohne-kategorie')}\n")
        lines.append(
            f"{len(ohne)} Anforderungen nennen keine Kategorie. Nach dem BSI-Standard 300-1 (3.4.1) "
            "gehören sie in jedes Anforderungspaket. Sie stehen hier nicht einzeln, die Liste gibt es im "
            "[Export](/export/) (Auswahl: „ohne Zielobjektkategorie“).\n"
        )
        (ZIELOBJEKTE_OUT_DIR / f"{tag_slug(name)}.mdx").write_text("\n".join(lines))

    def begriffe(name):
        """Synonyme und Beispiele aus der BSI-Tabelle: so findet, wer "Firewall" oder "NAS" sagt,
        seine Kategorie. Leer, wenn das BSI nichts eintraegt (11 bzw. 13 von 39)."""
        info, teile = TARGETS[name], []
        if info["synonyms"]:
            teile.append(f"auch: {mdx_safe(info['synonyms'])}")
        if info["example"]:
            teile.append(f"z. B. {mdx_safe(info['example'])}")
        return f'<span class="zeile-zusatz">{" · ".join(teile)}</span>' if teile else ""

    def zeilen(name, tiefe):
        direkt, mit_vererbung, _ = zielobjekt_zahlen(model, name, len(ohne))
        zeile = (
            f'<tr data-tiefe="{tiefe}" data-slug="{tag_slug(name)}">'
            f'<td><a href="/zielobjekte/{tag_slug(name)}/">{name}</a>{begriffe(name)}</td>'
            f"<td>{direkt}</td><td>{mit_vererbung}</td></tr>\n"
        )
        return zeile + "".join(zeilen(k, tiefe + 1) for k in model[name]["kinder"])

    wurzeln = sorted(n for n, i in TARGETS.items() if not i["parent"])
    zwei = sum(1 for c in controls.values() if len(control_targets(c)) > 1)
    bsp = "Webserver"
    b_direkt, b_mit, b_gesamt = zielobjekt_zahlen(model, bsp, len(ohne))
    index = [
        "---\n",
        f"title: {yaml_quote('Anforderungen nach Zielobjektkategorie')}\n",
        f"description: {yaml_quote(f'Die {len(TARGETS)} Zielobjektkategorien des BSI mit den Anforderungen, die für ein Asset der Kategorie gelten, direkt und geerbt, von Webserver bis Cloud-Dienste.')}\n",
        "---\n\n",
        pagefind_section("Zielobjekt"),
        f"Wer ein System betreibt, fragt nicht nach einer Praktik, sondern: Was gilt für meinen "
        f"{bsp}? Diese Seiten beantworten das je Zielobjektkategorie, in der Hierarchie des BSI.\n",
        f"**Die Regel:** Ein Asset erhält auch die Kategorien über seiner eigenen "
        f"([STM.2.1.4.1](/grundschutzpp/stm/#STM.2.1.4.1), Schritt 2 der [Methodik](/methodik/)). "
        f"{bsp} steht unter {TARGETS[bsp]['parent']}. Für {bsp} nennt der Katalog {b_direkt} Anforderungen direkt, "
        f"mit den geerbten gelten {b_mit}. Dazu kommen die {len(ohne)} Anforderungen ohne Kategorie, die in jedes "
        f"Anforderungspaket gehören, zusammen {b_gesamt}. Nur auf die direkte Angabe zu schauen, würde "
        f"{b_mit - b_direkt} Anforderungen übersehen.\n",
        f"Anforderungen mit zwei Kategorien ({zwei}) stehen bei beiden. Der Katalog sagt nicht, ob „oder“ oder "
        "„und“ gemeint ist; wir lesen es als „oder“. Das ist unsere Lesart, keine Aussage des BSI.\n",
        f"Zu jeder Zahl kommen immer die {len(ohne)} Anforderungen ohne Zielobjektkategorie dazu. "
        "Welche [Dokumente](/dokumente/) die Anforderungen einer Kategorie nennen, steht auf ihrer Seite.\n",
        '<table class="vergleich-table zahlen-tabelle">\n'
        "<thead><tr><th>Kategorie</th><th>direkt</th><th>mit Vererbung</th></tr></thead>\n<tbody>\n"
        + "".join(zeilen(w, 0) for w in wurzeln)
        + "</tbody>\n</table>\n",
    ]
    (ZIELOBJEKTE_OUT_DIR / "index.mdx").write_text("\n".join(index))
    return len(TARGETS)


# --- Dokumenten-Landkarte (ADR-0012) -------------------------------------------
# Eine Seite je Dokumenttyp, den der Katalog im Feld "documentation" nennt, und eine
# Uebersicht nach BSI-Kategorie. "Dokumentiert in" heisst nur: In diesem Dokumenttyp ist das
# Ergebnis festzuhalten. Es ist weder ein Nachweis noch eine Pruefvorgabe, und `result` wird
# nicht als Nachweis ausgegeben (ADR-0012). Beschreibung, Kategorie und Zielgruppe stehen nur
# da, wo export_documents() sie der BSI-Tabelle zuordnen konnte.
DOKUMENT_QUELLE_URL = (
    "https://github.com/BSI-Bund/Stand-der-Technik-Bibliothek/blob/main/"
    "documentation/namespaces/documentation_guidelines.csv"
)
DOKUMENT_OHNE_KATEGORIE = "Ohne Kategorie im BSI"
DOKUMENT_OHNE_BESCHREIBUNG = "Ohne Beschreibung des BSI"


def dokument_gruppe(d):
    if not d["zuordnung"]:
        return DOKUMENT_OHNE_BESCHREIBUNG
    if d["kategorie"] in ("", "???"):
        return DOKUMENT_OHNE_KATEGORIE
    return d["kategorie"]


def render_dokument_pages(catalog, control_index, params_by_id, basethreats_by_id, predecessor_index, guidelines):
    rows = export_rows(catalog, params_by_id, basethreats_by_id, predecessor_index)
    dokumente = export_documents(rows, guidelines, [g["id"] for g in catalog["groups"]])
    slugs = {}
    for d in dokumente:
        slugs.setdefault(tag_slug(d["dokument"]), []).append(d["dokument"])
    kollision = {k: v for k, v in slugs.items() if len(v) > 1}
    if kollision:
        raise SystemExit(f"Dokumenttypen mit gleicher Adresse: {kollision}")

    _, _, controls = zielobjekt_model(catalog)
    direkt_von = {cid: control_targets(c) for cid, c in controls.items()}
    DOKUMENTE_OUT_DIR.mkdir(parents=True, exist_ok=True)
    for alt in DOKUMENTE_OUT_DIR.glob("*.mdx"):
        alt.unlink()

    def plural(n):
        return "1 Anforderung" if n == 1 else f"{n} Anforderungen"

    for d in dokumente:
        name = d["dokument"]
        ids = [cid for cid, c in controls.items() if part_prop_value(c, "statement", "documentation") == name]
        beschr = first_sentence(d["beschreibung"]) if d["beschreibung"] else ""
        lines = [
            "---\n",
            f"title: {yaml_quote(name)}\n",
            "description: "
            + yaml_quote(
                f"Der Dokumenttyp {name} im Grundschutz++-Katalog: {plural(d['anzahl'])}, davon {d['muss']} MUSS, "
                "mit der Beschreibung des BSI, soweit vorhanden."
            )
            + "\n",
            "---\n\n",
            pagefind_section("Dokument"),
        ]
        angaben = []
        if d["kategorie"] not in ("", "???"):
            angaben.append(f"BSI-Kategorie: {mdx_safe(d['kategorie'])}")
        if d["zielgruppe"] not in ("", "???"):
            angaben.append(f"Zielgruppe: {mdx_safe(d['zielgruppe'])}")
        if angaben:
            lines.append(" · ".join(angaben) + "\n")
        if d["beschreibung"]:
            lines.append("**Beschreibung des BSI**\n")
            lines.append("\n".join(f"> {mdx_safe(p)}" for p in d["beschreibung"].split("\n") if p.strip()) + "\n")
            hinweis = f"Quelle: [BSI, documentation_guidelines.csv]({DOKUMENT_QUELLE_URL}), CC BY-SA 4.0."
            if d["zuordnung"] == "schreibweise":
                hinweis += f" Der Katalog nennt das Dokument „{name}“, die Tabelle „{d['bsi_name']}“; sie unterscheiden sich nur in der Schreibweise."
            lines.append(hinweis + "\n")
        else:
            lines.append(
                "Zu diesem Dokumenttyp liefert das BSI keine Beschreibung: Der Katalog nennt ihn, "
                "die Dokumentationstabelle des BSI führt ihn unter diesem Namen nicht.\n"
            )
        lines.append(
            f"**{plural(d['anzahl'])}**, davon {d['muss']} MUSS, nennen {name} als Ort, an dem das Ergebnis "
            f"festzuhalten ist. Praktik{'en' if len(d['praktiken']) > 1 else ''}: {', '.join(d['praktiken'])}. "
            "Das ist kein Nachweis und keine Prüfvorgabe. "
            "Aus dem Katalog allein geht nicht hervor, ob daraus ein eigenes Dokument oder ein Abschnitt in einem "
            "anderen wird.\n"
        )

        def zusatz(cid):
            ziele = direkt_von[cid]
            return f"Zielobjekt: {mdx_safe(', '.join(ziele))}" if ziele else "ohne Zielobjektkategorie"

        # Nach Zielobjekt: aus welchen direkt zugeordneten Kategorien die Anforderungen kommen (ADR-0012).
        je_ziel, ohne_ziel = {}, 0
        for cid in ids:
            if direkt_von[cid]:
                for k in direkt_von[cid]:
                    je_ziel[k] = je_ziel.get(k, 0) + 1
            else:
                ohne_ziel += 1
        teile = [f"[{k}](/zielobjekte/{tag_slug(k)}/) ({n})" for k, n in sorted(je_ziel.items())]
        if ohne_ziel:
            teile.append(f"ohne Zielobjektkategorie ({ohne_ziel})")
        lines.append("Nach Zielobjekt: " + ", ".join(teile) + ".\n")
        lines.append(f"## Anforderungen ({d['anzahl']}) {heading_anchor('anforderungen')}\n")
        lines.append(render_anforderungs_tabelle("anforderungen", ids, controls, control_index, zusatz))
        lines.append("Alle Dokumenttypen: [Dokumente im Katalog](/dokumente/).\n")
        (DOKUMENTE_OUT_DIR / f"{tag_slug(name)}.mdx").write_text("\n".join(lines))

    gruppen = {}
    for d in dokumente:
        gruppen.setdefault(dokument_gruppe(d), []).append(d)
    ende = [DOKUMENT_OHNE_KATEGORIE, DOKUMENT_OHNE_BESCHREIBUNG]
    reihenfolge = sorted(
        (g for g in gruppen if g not in ende), key=lambda g: (-sum(d["muss"] for d in gruppen[g]), g)
    ) + [g for g in ende if g in gruppen]
    mit_dokument = sum(d["anzahl"] for d in dokumente)
    index = [
        "---\n",
        f"title: {yaml_quote('Dokumente im Katalog')}\n",
        f"description: {yaml_quote(f'Die {len(dokumente)} Dokumenttypen, die der Grundschutz++-Katalog nennt, mit der Beschreibung des BSI und den Anforderungen dahinter.')}\n",
        "---\n\n",
        pagefind_section("Dokument"),
        f"Bei {mit_dokument} von {len(controls)} Anforderungen nennt der Katalog einen Dokumenttyp, in dem das "
        f"Ergebnis festzuhalten ist, insgesamt {len(dokumente)} verschiedene. Diese Seiten ordnen sie: je Typ die "
        "Beschreibung des BSI und die Anforderungen, die ihn nennen.\n",
        "**Was „Dokumentiert in“ bedeutet:** der Dokumenttyp, in dem das Ergebnis festgehalten wird. Es ist kein "
        "Nachweis und keine Prüfvorgabe, und der Katalog sagt nicht, ob jeder Typ ein eigenes Dokument sein muss.\n",
        "**Für ein bestimmtes System:** Die Seite einer [Zielobjektkategorie](/zielobjekte/) nennt die Dokumente, "
        "die ihre Anforderungen verlangen, zum Beispiel für den [Webserver](/zielobjekte/webserver/).\n",
    ]
    for gruppe in reihenfolge:
        eintraege = sorted(gruppen[gruppe], key=lambda d: (-d["muss"], -d["anzahl"], d["dokument"].casefold()))
        index.append(f"## {gruppe} ({len(eintraege)}) {heading_anchor(tag_slug(gruppe))}\n")
        if gruppe == DOKUMENT_OHNE_BESCHREIBUNG:
            index.append("Der Katalog nennt diese Dokumenttypen, die Tabelle des BSI beschreibt sie unter diesem Namen nicht.\n")
        index.append('<table class="vergleich-table zahlen-tabelle">\n')
        index.append("<thead><tr><th>Dokument</th><th>Anforderungen</th><th>davon MUSS</th></tr></thead>\n<tbody>\n")
        for d in eintraege:
            zg = f'<span class="zeile-zusatz">{mdx_safe(d["zielgruppe"])}</span>' if d["zielgruppe"] not in ("", "???") else ""
            index.append(
                f'<tr data-slug="{tag_slug(d["dokument"])}"><td><a href="/dokumente/{tag_slug(d["dokument"])}/">{mdx_safe(d["dokument"])}</a>{zg}</td>'
                f'<td>{d["anzahl"]}</td><td>{d["muss"]}</td></tr>\n'
            )
        index.append("</tbody>\n</table>\n")
    (DOKUMENTE_OUT_DIR / "index.mdx").write_text("\n".join(index))
    return len(dokumente)


def render_vergleich_index(by_baustein, baustein_links):
    by_layer = {}
    for baustein_id, entries in by_baustein.items():
        by_layer.setdefault(baustein_id.split(".")[0], []).append((baustein_id, entries))

    total = sum(len(entries) for entries in by_baustein.values())
    rel_counts = {}
    for entries in by_baustein.values():
        for _, rel, _ in entries:
            rel_counts[rel] = rel_counts.get(rel, 0) + 1
    legend = [
        f"   - **{relationship_label(rel)}** ({rel_counts[rel]}): {RELATIONSHIP_HINTS[rel]}\n"
        for rel in RELATIONSHIP_LABELS
        if rel in rel_counts
    ]

    lines = [
        "---\n",
        f"title: {yaml_quote('Vergleich: Altes Kompendium ↔ Grundschutz++')}\n",
        f"description: {yaml_quote(f'Für {len(by_baustein)} Bausteine des IT-Grundschutz-Kompendiums (Edition 2023) die Nachfolge-Anforderungen im Grundschutz++-Katalog – {total} Zuordnungen aus der offiziellen BSI-Mapping-Datei.')}\n",
        "---\n",
        "\n",
        VERGLEICH_FILTER_IMPORT,
        "\n",
        pagefind_section("Vergleich"),
        "Grundschutz++ löst das bisherige IT-Grundschutz-Kompendium schrittweise "
        "ab (siehe [Status & Zeitplan](/grundschutzpp/zeitplan/)). Wer heute nach "
        "dem Kompendium arbeitet, will wissen: Was wird aus meiner Anforderung? "
        "Das BSI hat dafür eine Mapping-Datei veröffentlicht "
        "(`ITGS-to-GS++-mapping_collection.json`). Diese Seite macht sie lesbar: "
        f"{total} Zuordnungen von alten Anforderungen zu Grundschutz++-Anforderungen, "
        f"sortiert nach den {len(by_baustein)} Bausteinen, für die das BSI "
        f"Zuordnungen angibt (von {len(baustein_links)} Bausteinen im Kompendium; "
        f"für die übrigen {len(baustein_links) - len(by_baustein)} gibt es keine, "
        "siehe [unten](#ohne-zuordnung)).\n",
        "\n",
        render_mapping_notice(by_baustein, baustein_links, total),
        "## So gehst du vor\n",
        "\n",
        "1. Suche unten deinen Baustein, z. B. `OPS.1.1.5`, oder tippe die ID ins Filterfeld unten.\n",
        "2. Auf der Baustein-Seite siehst du je alter Anforderung die passende neue "
        "Anforderung im Katalog, mit Link direkt dorthin.\n",
        "3. Der Beziehungstyp sagt, wie genau die beiden zusammenpassen:\n",
        "\n",
        *legend,
        "\n",
        "Der alte Anforderungstext steht hier bewusst nicht (siehe "
        "[ADR-0005](https://github.com/grundschutz-docs/docs/blob/main/adr/0005-vorgaenger-anforderung-alt-neu.md)), "
        "nur Struktur und Links. Den Baustein selbst gibt es beim BSI als PDF, "
        "verlinkt in der Spalte „Original\".\n",
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
            '<div class="table-scroll" tabindex="0">\n',
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
        lines += ["</tbody>\n", "</table>\n", "</div>\n", "</div>\n", "\n"]

    ohne = sorted(set(baustein_links) - set(by_baustein))
    if ohne:
        lines += [
            '<div class="vergleich-section not-content">\n',
            f"## Bausteine ohne Zuordnung {heading_anchor('ohne-zuordnung')}\n",
            "\n",
            f"<p>Für diese {len(ohne)} Bausteine enthält die Mapping-Datei des BSI keine "
            "Zuordnung. Das heißt nicht, dass ihre Themen im neuen Katalog fehlen, "
            "sondern nur, dass das BSI sie nicht ausdrücklich zugeordnet hat. Ob "
            "und wo die Inhalte aufgehen, haben wir nicht Anforderung für "
            "Anforderung geprüft.</p>\n",
            "\n",
            '<div class="table-scroll" tabindex="0">\n',
            '<table class="vergleich-table">\n',
            "<thead><tr><th>Baustein</th><th>Original</th></tr></thead>\n",
            "<tbody>\n",
        ]
        for baustein_id in ohne:
            pdf = baustein_links.get(baustein_id)
            pdf_cell = (
                f'<a href="{pdf}" target="_blank" rel="noopener noreferrer">PDF beim BSI</a>'
                if pdf
                else "—"
            )
            lines.append(
                f'<tr><td><span class="old-id">{baustein_id}</span>'
                f' <span class="new-title">{baustein_title(baustein_id, pdf)}</span></td>'
                f"<td>{pdf_cell}</td></tr>\n"
            )
        lines += ["</tbody>\n", "</table>\n", "</div>\n", "</div>\n", "\n"]
    return "".join(lines)


def catalog_source(catalog):
    """Zitierfaehige Angaben zum Katalogstand aus den OSCAL-Metadaten."""
    meta = catalog.get("metadata") or {}
    version = (meta.get("version") or "")[:10]
    doc_ids = meta.get("document-ids") or []
    return {
        "titel": meta.get("title") or "Anwenderkatalog Grundschutz++",
        "version": version,
        "dokument_id": doc_ids[0].get("identifier") if doc_ids else None,
    }


def render_source_block(src, praktik_id=None):
    """Katalogstand und Zitierhinweis am Kopf jeder Katalogseite.

    Zwei verschiedene Fragen, die beide vor dem Inhalt kommen:

    "Ist das aktuell?" -- der Katalogstand stand bisher nirgends auf der
    Seite. Wer pruefen will, ob hier der heutige Katalog steht, musste ins
    Repo schauen.

    "Wie zitiere ich das?" -- ein ISB liest hier und belegt im Auditnachweis
    das BSI-Original, so wie es sein soll. Diese Seite zitierfaehig machen zu
    wollen waere falsch; das Zitieren des Originals leicht zu machen ist die
    richtige Antwort darauf. Die Anforderungs-ID ist der stabile Schluessel,
    die Katalogversion der Stand -- beides steht jetzt da, zusammengesetzt
    muss es niemand mehr selbst.

    Im <details>, weil es Referenzapparat ist: wichtig fuer den, der es
    braucht, unsichtbar fuer alle anderen.
    """
    zeile = f"Katalogstand: {format_iso_date(src['version'])}" if src["version"] else "Katalogstand unbekannt"
    doc = f"Dokument-ID {src['dokument_id']} (RFC 9562), " if src["dokument_id"] else ""
    # Wer ueber Suche oder ein Sprachmodell mitten in einer Praktik einsteigt, sieht die
    # ISB-Seite nie. Der Excel-Link fuehrt auf die Exportseite mit dieser Praktik
    # vorgewaehlt, die CSV laedt direkt (eine fertige xlsx je Praktik gibt es nicht, ihre
    # Bytes aenderten sich bei jedem Sync-Lauf).
    export_line = ""
    if praktik_id:
        export_line = (
            f'<p>Diese Praktik als Tabelle: <a href="/export/?praktik={praktik_id}">Excel exportieren</a> · '
            f'<a href="/downloads/grundschutzpp-anforderungen-{praktik_id.lower()}.csv" download>CSV</a></p>\n'
        )
    return (
        '<div class="source-note">\n'
        f"<p>{zeile} — Quelle: "
        '<a href="https://github.com/BSI-Bund/Stand-der-Technik-Bibliothek" '
        'target="_blank" rel="noopener noreferrer">BSI Stand-der-Technik-Bibliothek</a>.</p>\n'
        + (export_line if praktik_id else "")
        + "<details>\n<summary>Eine Anforderung von dieser Seite zitieren</summary>\n"
        "<p>Maßgeblich ist immer das Original, nicht diese Aufbereitung. "
        f"Zitierfähig ist: BSI, <em>{src['titel']}</em>, Version "
        f"{src['version'] or '—'}, {doc}"
        "Anforderung <em>&lt;ID&gt;</em> — wobei die ID die Kennung neben "
        "der jeweiligen Überschrift ist, etwa <code>GC.5.1.1</code>. "
        "Sie bleibt stabil, auch wenn das BSI eine Formulierung ändert.</p>\n"
        "</details>\n</div>\n\n"
    )


def format_iso_date(iso):
    """2026-09-10 -> 10. September 2026."""
    monate = (
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember",
    )
    try:
        d = date.fromisoformat(iso)
    except ValueError:
        return iso
    return f"{d.day}. {monate[d.month - 1]} {d.year}"


def write_mdx(path, frontmatter, body, section=None):
    needs_control_meta = "<ControlMeta" in body
    prefix = CONTROL_META_IMPORT + "\n" if needs_control_meta else ""
    marker = pagefind_section(section) if section else ""
    path.write_text(frontmatter + prefix + marker + body)


# --- Aenderungsprotokoll ------------------------------------------------------
# Vergleicht die veroeffentlichten Staende des BSI-Katalogs aus der Git-Historie des
# BSI-Repos und schreibt src/data/changelog.json. Die Seite /aenderungen/ liest nur
# diese Datei. Der Vergleich nennt Fakten ("hier stand vorher X, jetzt Y") und
# bewertet nichts.
#
# Inkrementell: je BSI-Commit, der den Katalog aendert, entsteht genau ein Eintrag,
# Schluessel ist der Commit. Ein Lauf berechnet nur Commits, die noch nicht in der
# Datei stehen, und laedt dafuer je zwei Staende des Katalogs (je ~5 MB). Fehlt die
# Historie (flacher Klon wie im Sync-Workflow bisher), bleibt die Datei unveraendert
# und der Lauf sagt es.
CHANGELOG_FILE = DATA_OUT_DIR / "changelog.json"
CHANGELOG_COMMIT_URL = "https://github.com/BSI-Bund/Stand-der-Technik-Bibliothek/commit"

# (Schluessel, Bezeichnung auf der Seite). Reihenfolge = Reihenfolge auf der Seite.
CHANGELOG_FIELDS = [
    ("titel", "Titel"),
    ("anforderung", "Anforderung"),
    ("erlaeuterung", "Erläuterung"),
    ("pflichtgrad", "Pflichtgrad"),
    ("stufe", "Sicherheitsstufe"),
    ("aufwand", "Aufwand"),
    ("ergebnis", "Ergebnis"),
    ("ergebnis_zusatz", "Ergebnis, Zusatz"),
    ("dokument", "Dokumentiert in"),
    ("zielobjekte", "Zielobjektkategorien"),
    ("gefaehrdungen", "Gefährdungen"),
    ("tags", "Tags"),
]
CHANGELOG_TEXT_FIELDS = {"titel", "anforderung", "erlaeuterung", "ergebnis", "ergebnis_zusatz"}


def _git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[:200]}")
    return r.stdout


def changelog_history(catalog_file):
    """[(commit, ISO-Datum)] aller Commits, die den Katalog aendern, aelteste zuerst.
    Leere Liste, wenn die Datei in keinem Git-Repo liegt."""
    path = Path(catalog_file).resolve()
    try:
        top = Path(_git(path.parent, "rev-parse", "--show-toplevel").strip())
    except RuntimeError:
        return None, None, []
    rel = path.relative_to(top.resolve()).as_posix()
    lines = _git(top, "log", "--format=%H%x09%cI", "--", rel).splitlines()
    return top, rel, [tuple(l.split("\t")) for l in reversed(lines) if l]


def changelog_load(top, rel, commit):
    return json.loads(_git(top, "show", f"{commit}:{rel}"))["catalog"]


def strip_internal(node):
    # Die internen UUIDs ("alt-identifier") aendern sich bei jedem Stand: kein Inhalt.
    if isinstance(node, dict):
        return {
            k: strip_internal([p for p in v if p.get("name") != "alt-identifier"] if k == "props" else v)
            for k, v in node.items()
        }
    if isinstance(node, list):
        return [strip_internal(x) for x in node]
    return node


def changelog_nodes(catalog):
    """id -> Knoten ohne Unteranforderungen."""
    return {c["id"]: {k: v for k, v in c.items() if k != "controls"} for g in catalog["groups"] for c in collect_controls(g)}


def changelog_normalize(catalog):
    """id -> {Feldschluessel: Wert} fuer die angezeigten Felder, plus Praktik und eine
    Signatur des ganzen Knotens (ohne die internen UUIDs, die sich bei jedem Stand
    aendern und kein Inhalt sind)."""
    params = build_params_index(catalog)
    out = {}

    def lst(value, sort=True):
        items = [x.strip() for x in (value or "").split(",") if x.strip()]
        return ", ".join(sorted(items) if sort else items)

    for group in catalog["groups"]:
        for c in collect_controls(group):
            own = {k: v for k, v in c.items() if k != "controls"}
            out[c["id"]] = {
                "praktik": group["id"],
                "felder": {
                    "titel": c.get("title", ""),
                    "anforderung": export_plain_text(part_text(c, "statement"), params),
                    "erlaeuterung": export_plain_text(part_text(c, "guidance"), params),
                    "pflichtgrad": part_prop_value(c, "statement", "modal_verb") or "",
                    "stufe": prop_value(c, "sec_level") or "",
                    "aufwand": prop_value(c, "effort_level") or "",
                    "ergebnis": part_prop_value(c, "statement", "result") or "",
                    "ergebnis_zusatz": part_prop_value(c, "statement", "result_specification") or "",
                    "dokument": part_prop_value(c, "statement", "documentation") or "",
                    "zielobjekte": lst(part_prop_value(c, "statement", "target_object_categories")),
                    "gefaehrdungen": lst(prop_value(c, "threats")),
                    "tags": lst(prop_value(c, "tags")),
                },
                "signatur": json.dumps(strip_internal(own), sort_keys=True, ensure_ascii=False),
            }
    return out


def changelog_word_diff(alt, neu):
    """Wortweiser Vergleich als Liste von [Zeichen, Text]: "=" gleich, "-" entfernt, "+" neu.

    Ein gleicher Abschnitt, der nur aus Leerraum besteht und zwischen zwei Aenderungen
    liegt, gehoert zur Aenderung: sonst waere "Ausgabe, Registrierung und Zuordnung"
    drei einzelne Treffer statt einer zusammenhaengenden Aenderung."""
    a = re.findall(r"\s+|\S+", alt)
    b = re.findall(r"\s+|\S+", neu)
    blocks = []  # [Art "e" gleich / "c" geaendert, Text alt, Text neu]
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        blocks.append(["e" if op == "equal" else "c", "".join(a[i1:i2]), "".join(b[j1:j2])])
    for k in range(1, len(blocks) - 1):
        if blocks[k][0] == "e" and not blocks[k][1].strip() and blocks[k - 1][0] == "c" and blocks[k + 1][0] == "c":
            blocks[k][0] = "c"
    merged = []
    for art, at, bt in blocks:
        if merged and merged[-1][0] == art == "c":
            merged[-1][1] += at
            merged[-1][2] += bt
        else:
            merged.append([art, at, bt])
    segs = []
    for art, at, bt in merged:
        if art == "e":
            segs.append(["=", at])
        else:
            if at:
                segs.append(["-", at])
            if bt:
                segs.append(["+", bt])
    return segs


def changelog_paths(a, b, pre=""):
    """Pfade (JSON-artig, z. B. "class" oder "parts[1]/prose"), an denen zwei Knoten verschieden sind."""
    if type(a) is not type(b):
        yield pre
    elif isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            sub = f"{pre}/{k}" if pre else k
            if k not in a or k not in b:
                yield sub
            else:
                yield from changelog_paths(a[k], b[k], sub)
    elif isinstance(a, list):
        if len(a) != len(b):
            yield pre
            return
        for i, (x, y) in enumerate(zip(a, b)):
            yield from changelog_paths(x, y, f"{pre}[{i}]")
    elif a != b:
        yield pre


def changelog_value_at(node, path):
    for tok in re.findall(r"/?([^/\[\]]+)|\[(\d+)\]", path):
        node = node[tok[0]] if tok[0] else node[int(tok[1])]
    return node


def changelog_entry(old_cat, new_cat, new_commit, new_date, old_commit, threat_labels):
    old, new = changelog_normalize(old_cat), changelog_normalize(new_cat)
    old_nodes, new_nodes = changelog_nodes(old_cat), changelog_nodes(new_cat)
    changes, technisch = [], {}
    for cid in sorted(set(old) & set(new)):
        o, n = old[cid], new[cid]
        felder = []
        for key, label in CHANGELOG_FIELDS:
            if o["felder"][key] != n["felder"][key]:
                f = {"feld": key, "name": label, "alt": o["felder"][key], "neu": n["felder"][key]}
                if key in CHANGELOG_TEXT_FIELDS and f["alt"] and f["neu"]:
                    f["diff"] = changelog_word_diff(f["alt"], f["neu"])
                if key == "gefaehrdungen":
                    ids = [x.strip() for x in (f["alt"] + "," + f["neu"]).split(",") if x.strip()]
                    f["bezeichnungen"] = {x: threat_labels[x] for x in dict.fromkeys(ids) if x in threat_labels}
                felder.append(f)
        if felder:
            changes.append({"id": cid, "titel": n["felder"]["titel"], "praktik": n["praktik"], "felder": felder})
        elif o["signatur"] != n["signatur"]:
            # Der Knoten ist anders, aber nichts davon steht auf der Seite (z. B. ein
            # interner Klassenname). Nach Feldpfad zusammengefasst, mit einem Beispiel.
            for pfad in changelog_paths(strip_internal(old_nodes[cid]), strip_internal(new_nodes[cid])):
                allg = re.sub(r"\[\d+\]", "[]", pfad)
                t = technisch.setdefault(allg, {"pfad": allg, "ids": [], "beispiel": None})
                t["ids"].append(cid)
                if t["beispiel"] is None:
                    t["beispiel"] = {
                        "id": cid,
                        "alt": json.dumps(changelog_value_at(strip_internal(old_nodes[cid]), pfad), ensure_ascii=False)[:160],
                        "neu": json.dumps(changelog_value_at(strip_internal(new_nodes[cid]), pfad), ensure_ascii=False)[:160],
                    }
    return {
        "commit": new_commit,
        "veroeffentlicht": new_date,
        "vorgaenger": old_commit,
        "katalog_version": new_cat["metadata"].get("version"),
        "neu": sorted(set(new) - set(old)),
        "entfernt": sorted(set(old) - set(new)),
        "aenderungen": changes,
        "technische_aenderungen": [
            {**t, "anzahl": len(t["ids"])} for t in sorted(technisch.values(), key=lambda t: (-len(t["ids"]), t["pfad"]))
        ],
    }


def update_changelog(catalog_file, threat_labels=None):
    """Haengt Eintraege fuer Katalog-Commits an, die noch nicht in changelog.json stehen."""
    threat_labels = load_basethreats() if threat_labels is None else threat_labels
    top, rel, history = changelog_history(catalog_file)
    data = json.loads(CHANGELOG_FILE.read_text()) if CHANGELOG_FILE.exists() else {"eintraege": []}
    known = {e["commit"] for e in data["eintraege"]} | ({data["basis"]["commit"]} if data.get("basis") else set())
    if len(history) < 2:
        print(
            "HINWEIS: Aenderungsprotokoll nicht aktualisiert: im Git-Verlauf des Katalogs gibt es "
            f"{len(history)} Commit(s) (flacher Klon?). changelog.json bleibt unveraendert.",
            file=sys.stderr,
        )
        return {"neu": 0, "gesamt": len(data["eintraege"])}
    if not data.get("basis"):
        data["basis"] = {"commit": history[0][0], "veroeffentlicht": history[0][1]}
        known.add(history[0][0])
    added_commits = []
    cache = {}

    def load(c):
        if c not in cache:
            cache[c] = changelog_load(top, rel, c)
        return cache[c]

    for (prev_c, _), (c, date_iso) in zip(history, history[1:]):
        if c in known:
            continue
        data["eintraege"].append(changelog_entry(load(prev_c), load(c), c, date_iso, prev_c, threat_labels))
        known.add(c)
        added_commits.append(c)
    data["eintraege"].sort(key=lambda e: e["veroeffentlicht"], reverse=True)
    data["stand"] = {"commit": history[-1][0], "veroeffentlicht": history[-1][1]}
    CHANGELOG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return {"neu": len(added_commits), "gesamt": len(data["eintraege"]), "commits": added_commits}


def check_zielobjekte(catalog):
    """Liest die Zielobjekt-Seiten zurueck und rechnet auf zwei anderen Wegen nach als
    render_zielobjekt_pages() (ADR-0011). Gleiche Regel wie bei check_export(): kein
    Test auf demselben Codepfad wie der Renderer.

    Weg 1: Anforderungen und direkte Kategorien aus dem *Rohbaum* des Katalogs, die
    Hierarchie ueber UUID/ChildOfUUID aus der frisch gelesenen BSI-Tabelle. Verglichen
    wird je Seite und Teil die Menge der IDs, nicht nur die Anzahl.
    Weg 2: die Zahlen auf der Uebersicht gegen die fertige Export-CSV, die Nutzende
    herunterladen (Spalten "Zielobjektkategorien" und "Gilt auch fuer Unterkategorien")."""
    problems = []
    with TARGETS_FILE.open(newline="", encoding="utf-8") as fh:
        zeilen = list(csv.DictReader(fh))
    name_von = {z["UUID"]: z["Zielobjekt"] for z in zeilen}
    eltern_von = {z["Zielobjekt"]: name_von.get(z["ChildOfUUID"]) for z in zeilen}

    def ueber(name):
        out, k = [], eltern_von.get(name)
        while k and k not in out:
            out.append(k)
            k = eltern_von.get(k)
        return out

    direkt_von = {}

    def sammle(knoten):
        for c in knoten.get("controls", []):
            st = next(p for p in c["parts"] if p["name"] == "statement")
            v = next((x["value"] for x in st["props"] if x["name"] == "target_object_categories"), "")
            direkt_von[c["id"]] = {x.strip() for x in v.split(",") if x.strip()}
            sammle(c)
        for g in knoten.get("groups", []):
            sammle(g)

    sammle(json.loads(CATALOG_FILE.read_text())["catalog"])
    ohne = {cid for cid, ks in direkt_von.items() if not ks}

    erwartet = {}
    for name in eltern_von:
        direkt = {cid for cid, ks in direkt_von.items() if name in ks}
        teile = {"direkt": direkt}
        for a in ueber(name):
            teile[f"geerbt:{a}"] = {cid for cid, ks in direkt_von.items() if a in ks} - direkt
        erwartet[tag_slug(name)] = teile

    # Seiten zurueckgelesen: je Teil die IDs der Tabellenzeilen.
    seiten = {}
    for datei in ZIELOBJEKTE_OUT_DIR.glob("*.mdx"):
        if datei.name == "index.mdx":
            continue
        teile, aktuell = {}, None
        for zeile in datei.read_text().splitlines():
            m = re.search(r'<div class="zielobjekt-teil" data-teil="([^"]*)"', zeile)
            if m:
                aktuell = m.group(1)
                teile[aktuell] = set()
            m = re.search(r'<tr data-sec="[^"]*" data-id="([^"]+)"', zeile)
            if m and aktuell is not None:
                teile[aktuell].add(m.group(1))
        seiten[datei.stem] = teile
    if set(seiten) != set(erwartet):
        problems.append(f"Zielobjekt-Seiten weichen von den Kategorien ab (nur Seite: {sorted(set(seiten) - set(erwartet))[:3]}, nur Tabelle: {sorted(set(erwartet) - set(seiten))[:3]})")
    for slug, teile in erwartet.items():
        ist = seiten.get(slug, {})
        for teil, ids in teile.items():
            # Ein leerer Teil bekommt keine Tabelle, das ist kein Fehler.
            if ist.get(teil, set()) != ids:
                problems.append(f"{slug}, Teil {teil}: {len(ist.get(teil, set()))} Zeilen auf der Seite, Nachrechnung {len(ids)}")
        for teil in set(ist) - set(teile):
            problems.append(f"{slug}: unerwarteter Teil {teil}")

    # Weg 2: Uebersicht gegen die Export-CSV.
    with (EXPORT_OUT_DIR / "grundschutzpp-anforderungen.csv").open(newline="", encoding="utf-8-sig") as f:
        tabelle = list(csv.reader(f, delimiter=";"))
    kopf, rumpf = tabelle[0], tabelle[1:]
    col = {n: i for i, n in enumerate(kopf)}
    csv_ohne = sum(1 for r in rumpf if r[col["Zielobjektkategorien"]] == EXPORT_NO_TARGET)
    if csv_ohne != len(ohne):
        problems.append(f"Export-CSV hat {csv_ohne} Anforderungen ohne Kategorie, der Katalog {len(ohne)}")
    uebersicht = {}
    for m in re.finditer(
        r'<tr data-tiefe="(\d+)" data-slug="([a-z0-9-]+)">.*?</a>.*?</td><td>(\d+)</td><td>(\d+)</td></tr>',
        (ZIELOBJEKTE_OUT_DIR / "index.mdx").read_text(),
    ):
        uebersicht[m.group(2)] = (int(m.group(1)), int(m.group(3)), int(m.group(4)))
    if set(uebersicht) != set(erwartet):
        problems.append("Zielobjekt-Uebersicht nennt nicht genau die Kategorien der Tabelle")
    for name in eltern_von:
        eigen = lambda r: {x for x in r[col["Zielobjektkategorien"]].split("; ") if x}
        unter = lambda r: {x for x in r[col["Gilt auch für Unterkategorien"]].split("; ") if x}
        gilt = sum(1 for r in rumpf if name in eigen(r) or name in unter(r))
        direkt = sum(1 for r in rumpf if name in eigen(r))
        # (Einrueckungstiefe = Zahl der Elternkategorien, direkt, mit Vererbung)
        soll = (len(ueber(name)), direkt, gilt)
        if uebersicht.get(tag_slug(name)) != soll:
            problems.append(f"{name}: Uebersicht {uebersicht.get(tag_slug(name))}, Export-CSV {soll}")
        # Die Saetze auf der Kategorieseite nennen dieselben Zahlen, "zusammen" inklusive der ohne Kategorie.
        seitentext = (ZIELOBJEKTE_OUT_DIR / f"{tag_slug(name)}.mdx").read_text()
        genannt = "**1 Anforderung**" if gilt == 1 else f"**{gilt} Anforderungen**"
        if f"{genannt} gelten" not in seitentext:
            problems.append(f"{name}: Seitentext nennt nicht {gilt} Anforderungen")
        if f"**zusammen {gilt + csv_ohne}**" not in seitentext:
            problems.append(f"{name}: Seitentext nennt nicht zusammen {gilt + csv_ohne}")

    # Der Export-Link auf jeder Kategorieseite: genau einer, und entschluesselt der Name der Kategorie.
    for name in eltern_von:
        text = (ZIELOBJEKTE_OUT_DIR / f"{tag_slug(name)}.mdx").read_text()
        ziele = re.findall(r"\]\(/export/\?ziel=([^)&]+)\)", text)
        if [urllib.parse.unquote(z) for z in ziele] != [name]:
            problems.append(f"{name}: Export-Link auf der Kategorieseite fehlt oder zeigt auf eine andere Kategorie ({ziele})")

    # Die Zahl der Anforderungen mit zwei Kategorien im Text der Uebersicht.
    m = re.search(r"Anforderungen mit zwei Kategorien \((\d+)\)", (ZIELOBJEKTE_OUT_DIR / "index.mdx").read_text())
    zwei = sum(1 for ks in direkt_von.values() if len(ks) > 1)
    if not m or int(m.group(1)) != zwei:
        problems.append(f"Uebersicht nennt {m.group(1) if m else 'keine'} Anforderungen mit zwei Kategorien, der Katalog {zwei}")

    # Jede Pille verlinkt auf eine vorhandene Seite.
    katalogtext = "\n".join(p.read_text() for p in OUT_DIR.glob("*.mdx"))
    verlinkt = {
        slug
        for attr in re.findall(r" targets=\{\[(.*?)\]\} ", katalogtext)
        for slug in re.findall(r'\{ name: "[^"]+", slug: "([^"]+)"', attr)
    }
    if not verlinkt:
        problems.append("Keine Pille mit Zielobjekt-Link auf den Katalogseiten gefunden")
    if not verlinkt <= set(seiten):
        problems.append(f"Pillen verlinken auf Zielobjekt-Seiten, die es nicht gibt: {sorted(verlinkt - set(seiten))[:3]}")

    if problems:
        raise SystemExit("Zielobjekt-Seiten passen nicht zum Katalog:\n  - " + "\n  - ".join(problems))
    print(f"Zielobjekt-Seiten ok: {len(seiten)} Seiten, je Teil gegen den Rohkatalog und die Export-CSV nachgerechnet")


def check_dokumente(catalog):
    """Liest die Dokument-Seiten zurueck und rechnet auf zwei anderen Wegen nach als
    render_dokument_pages() (ADR-0012), nach derselben Regel wie check_zielobjekte().

    Weg 1: je Dokumenttyp die Anforderungen und das Modalverb aus dem *Rohbaum* des Katalogs
    (nicht aus collect_controls() oder export_rows()). Verglichen wird je Seite die Menge der
    IDs, nicht nur die Anzahl, dazu die Saetze "N Anforderungen, davon M MUSS".
    Weg 2: die Zahlen der Uebersicht und die Zahl der Typen gegen die fertige Export-CSV, die
    Nutzende herunterladen (Spalten "Dokumentiert in" und "Pflichtgrad")."""
    problems = []
    erwartet = {}
    roh = {}  # id -> (Dokumenttyp, Modalverb, direkte Zielobjektkategorien)

    def sammle(knoten):
        for c in knoten.get("controls", []):
            st = next(p for p in c["parts"] if p["name"] == "statement")
            doku = next((x["value"] for x in st["props"] if x["name"] == "documentation"), "")
            verb = next(x["value"] for x in st["props"] if x["name"] == "modal_verb")
            ziele = next((x["value"] for x in st["props"] if x["name"] == "target_object_categories"), "")
            roh[c["id"]] = (doku, verb, {z.strip() for z in ziele.split(",") if z.strip()})
            if doku:
                e = erwartet.setdefault(tag_slug(doku), {"name": doku, "ids": set(), "muss": 0})
                e["ids"].add(c["id"])
                e["muss"] += verb == "MUSS"
            sammle(c)
        for g in knoten.get("groups", []):
            sammle(g)

    sammle(json.loads(CATALOG_FILE.read_text())["catalog"])

    seiten = {}
    for datei in DOKUMENTE_OUT_DIR.glob("*.mdx"):
        if datei.name == "index.mdx":
            continue
        text = datei.read_text()
        ids = set(re.findall(r'<tr data-sec="[^"]*" data-id="([^"]+)"', text))
        m = re.search(r"\*\*(\d+) Anforderung(?:en)?\*\*, davon (\d+) MUSS, nennen", text)
        seiten[datei.stem] = (ids, (int(m.group(1)), int(m.group(2))) if m else None)
    if set(seiten) != set(erwartet):
        problems.append(
            f"Dokument-Seiten weichen von den Dokumenttypen ab (nur Seite: {sorted(set(seiten) - set(erwartet))[:3]}, "
            f"nur Katalog: {sorted(set(erwartet) - set(seiten))[:3]})"
        )
    for slug, e in erwartet.items():
        ids, zahlen = seiten.get(slug, (set(), None))
        if ids != e["ids"]:
            problems.append(f"{e['name']}: {len(ids)} Zeilen auf der Seite, Nachrechnung {len(e['ids'])}")
        if zahlen != (len(e["ids"]), e["muss"]):
            problems.append(f"{e['name']}: Satz nennt {zahlen}, Nachrechnung {(len(e['ids']), e['muss'])}")

    # Weg 2: Uebersicht gegen die Export-CSV.
    with (EXPORT_OUT_DIR / "grundschutzpp-anforderungen.csv").open(newline="", encoding="utf-8-sig") as f:
        tabelle = list(csv.reader(f, delimiter=";"))
    kopf, rumpf = tabelle[0], tabelle[1:]
    col = {n: i for i, n in enumerate(kopf)}
    aus_csv = {}
    for r in rumpf:
        name = r[col["Dokumentiert in"]]
        if name:
            z = aus_csv.setdefault(tag_slug(name), [0, 0])
            z[0] += 1
            z[1] += r[col["Pflichtgrad"]] == "MUSS"
    uebersicht = {}
    text = (DOKUMENTE_OUT_DIR / "index.mdx").read_text()
    for m in re.finditer(r'<tr data-slug="([a-z0-9-]+)">.*?</td><td>(\d+)</td><td>(\d+)</td></tr>', text):
        uebersicht[m.group(1)] = [int(m.group(2)), int(m.group(3))]
    if uebersicht != aus_csv:
        falsch = sorted(k for k in set(uebersicht) | set(aus_csv) if uebersicht.get(k) != aus_csv.get(k))[:3]
        problems.append(f"Dokument-Uebersicht weicht von der Export-CSV ab (z. B. {falsch})")
    if {k: v for k, v in uebersicht.items()} != {k: [len(e["ids"]), e["muss"]] for k, e in erwartet.items()}:
        problems.append("Dokument-Uebersicht weicht vom Rohkatalog ab")
    gesamt = sum(e[0] for e in uebersicht.values())
    m = re.search(r"Bei (\d+) von (\d+) Anforderungen nennt der Katalog einen Dokumenttyp, .*?insgesamt (\d+) verschiedene", text, re.S)
    if not m or (int(m.group(1)), int(m.group(2)), int(m.group(3))) != (gesamt, len(rumpf), len(erwartet)):
        problems.append(f"Einleitung der Dokument-Uebersicht nennt {m.groups() if m else 'nichts'}, erwartet {(gesamt, len(rumpf), len(erwartet))}")

    # --- Zusammenspiel mit den Zielobjekten (ADR-0012) -----------------------------------------
    # (a) Pillen "Dokumentiert in": eine je Anforderung mit Dokument, auf eine vorhandene Seite.
    katalogtext = "\n".join(p.read_text() for p in OUT_DIR.glob("*.mdx"))
    pillen = re.findall(r'document=\{\{ name: "[^"]+", slug: "([^"]+)" \}\}', katalogtext)
    soll_pillen = sum(1 for d, _, _ in roh.values() if d)
    if len(pillen) != soll_pillen:
        problems.append(f"{len(pillen)} Pillen 'Dokumentiert in' auf den Katalogseiten, laut Katalog {soll_pillen}")
    if not set(pillen) <= set(seiten):
        problems.append(f"Pillen verlinken auf Dokument-Seiten, die es nicht gibt: {sorted(set(pillen) - set(seiten))[:3]}")
    je_pille = {}
    for slug in pillen:
        je_pille[slug] = je_pille.get(slug, 0) + 1
    if je_pille != {k: len(e["ids"]) for k, e in erwartet.items()}:
        problems.append("Pillen je Dokumenttyp weichen vom Rohkatalog ab")

    # (b) "Nach Zielobjekt" auf den Dokument-Seiten: je direkt zugeordneter Kategorie und ohne Kategorie.
    for slug, e in erwartet.items():
        soll = {}
        soll_ohne = 0
        for cid in e["ids"]:
            ks = roh[cid][2]
            if ks:
                for k in ks:
                    soll[k] = soll.get(k, 0) + 1
            else:
                soll_ohne += 1
        zeile = re.search(r"^Nach Zielobjekt: (.*)\.$", (DOKUMENTE_OUT_DIR / f"{slug}.mdx").read_text(), re.M)
        ist = {m.group(1): int(m.group(2)) for m in re.finditer(r"\[([^\]]+)\]\(/zielobjekte/[a-z0-9-]+/\) \((\d+)\)", zeile.group(1))} if zeile else None
        ist_ohne = re.search(r"ohne Zielobjektkategorie \((\d+)\)", zeile.group(1)) if zeile else None
        if ist != soll or (int(ist_ohne.group(1)) if ist_ohne else 0) != soll_ohne:
            problems.append(f"{e['name']}: 'Nach Zielobjekt' weicht von der Nachrechnung ab")

    # (c) Tabelle "Dokumente zu diesen Anforderungen" auf den Kategorieseiten: Weg 1 aus dem Rohkatalog
    # und der BSI-Hierarchie (UUID), Weg 2 aus der Export-CSV (Spalten "Zielobjektkategorien",
    # "Gilt auch fuer Unterkategorien", "Dokumentiert in").
    with TARGETS_FILE.open(newline="", encoding="utf-8") as fh:
        zeilen = list(csv.DictReader(fh))
    name_von = {z["UUID"]: z["Zielobjekt"] for z in zeilen}
    eltern_von = {z["Zielobjekt"]: name_von.get(z["ChildOfUUID"]) for z in zeilen}

    def mit_eltern(name):
        out, k = {name}, eltern_von.get(name)
        while k and k not in out:
            out.add(k)
            k = eltern_von.get(k)
        return out

    def parse_tabelle(text):
        m = re.search(r'<table[^>]*data-dokumente="zielobjekt">(.*?)</table>', text, re.S)
        if not m:
            return {}
        return {
            g.group(1): [int(g.group(2)), int(g.group(3))]
            for g in re.finditer(r'<tr data-slug="([a-z0-9-]+)">.*?</td><td>(\d+)</td><td>(\d+)</td></tr>', m.group(1))
        }

    for name in eltern_von:
        kette = mit_eltern(name)
        soll = {}
        for cid, (doku, verb, ks) in roh.items():
            if doku and ks & kette:
                z = soll.setdefault(tag_slug(doku), [0, 0])
                z[0] += 1
                z[1] += verb == "MUSS"
        csv_soll = {}
        for r in rumpf:
            eigen = {x for x in r[col["Zielobjektkategorien"]].split("; ") if x}
            unter = {x for x in r[col["Gilt auch für Unterkategorien"]].split("; ") if x}
            if r[col["Dokumentiert in"]] and (name in eigen or name in unter):
                z = csv_soll.setdefault(tag_slug(r[col["Dokumentiert in"]]), [0, 0])
                z[0] += 1
                z[1] += r[col["Pflichtgrad"]] == "MUSS"
        text = (ZIELOBJEKTE_OUT_DIR / f"{tag_slug(name)}.mdx").read_text()
        ist = parse_tabelle(text)
        if ist != soll:
            problems.append(f"{name}: Dokument-Tabelle weicht vom Rohkatalog ab (Seite {len(ist)} Typen, Nachrechnung {len(soll)})")
        if ist != csv_soll:
            problems.append(f"{name}: Dokument-Tabelle weicht von der Export-CSV ab")
        kopf = re.search(r"## Dokumente zu diesen Anforderungen \((\d+)\)", text)
        if (int(kopf.group(1)) if kopf else 0) != len(soll):
            problems.append(f"{name}: Ueberschrift der Dokument-Tabelle nennt nicht {len(soll)}")

    if problems:
        raise SystemExit("Dokument-Seiten passen nicht zum Katalog:\n  - " + "\n  - ".join(problems))
    print(f"Dokument-Seiten ok: {len(seiten)} Seiten, je Typ gegen den Rohkatalog und die Export-CSV nachgerechnet")


def check_sync_paths():
    """Jeder Ausgabeordner des Generators muss im add-paths des Sync-PRs stehen.

    Sonst nimmt der taegliche Sync-PR die neu erzeugten Seiten nicht mit: Der Generator laeuft im
    Workflow durch (er schreibt ja), aber der PR enthaelt nur einen Teil davon. Das ist schon einmal
    passiert (rollen/, vergleich/, src/data, public/downloads) und am 2026-10-29 wieder
    (zielobjekte/, dokumente/). Hier statt im Workflow, damit es lokal beim ersten Lauf auffaellt."""
    # Wurzel dieses Repos, nicht REPO_ROOT (das ist das Verzeichnis darueber, mit dem BSI-Klon).
    docs_root = Path(__file__).resolve().parent.parent
    workflow = docs_root / ".github" / "workflows" / "sync-catalog.yml"
    if not workflow.exists():  # z. B. in einem Export ohne .github; dann laut, nicht still
        print("Sync-Pfade: .github/workflows/sync-catalog.yml nicht gefunden, nicht geprueft", file=sys.stderr)
        return
    zeilen = workflow.read_text().splitlines()
    try:
        start = next(i for i, z in enumerate(zeilen) if z.strip().startswith("add-paths:"))
    except StopIteration:
        raise SystemExit("sync-catalog.yml hat kein add-paths: der Sync-PR wuerde alles mitnehmen oder nichts")
    eingetragen = []
    for z in zeilen[start + 1:]:
        if not z.startswith(" " * 12) and z.strip():
            break
        if z.strip():
            eingetragen.append(z.strip())
    ordner = [OUT_DIR, ROLLEN_OUT_DIR, VERGLEICH_OUT_DIR, ZIELOBJEKTE_OUT_DIR, DOKUMENTE_OUT_DIR, EXPORT_OUT_DIR]
    fehlen = []
    for d in ordner:
        rel = d.relative_to(docs_root).as_posix()
        if f"{rel}/**" not in eingetragen:
            fehlen.append(rel)
    if "src/data/*.json" not in eingetragen:
        fehlen.append("src/data")
    if fehlen:
        raise SystemExit(
            "Der Generator schreibt in Ordner, die im add-paths von .github/workflows/sync-catalog.yml fehlen: "
            + ", ".join(fehlen)
            + "\n  (der Sync-PR wuerde sie nicht mitnehmen; dort eintragen)"
        )
    print(f"Sync-Pfade ok: {len(ordner) + 1} Ausgabeordner stehen im add-paths des Sync-PRs")


def update_upstream_stand():
    """Schreibt src/data/upstream.json: der BSI-Commit, aus dem diese Seiten erzeugt wurden.

    Der CI-Job "Erzeugte Dateien == Generator" (.github/workflows/generated.yml) holt genau diesen Commit,
    laesst den Generator laufen und vergleicht mit dem, was im Repo steht. Dafuer muss der Stand
    festgehalten sein; ohne ihn waere "gleich" eine Frage des Tages.

    Es ist der juengste Commit, der eine der sechs Eingabedateien aendert, nicht der HEAD des BSI-Repos.
    Sonst wuerde jede Aenderung an einer anderen Datei dort (README, andere Kataloge) einen Sync-PR
    ausloesen, in dem sich nur dieser Hash aendert. Liegen die Eingaben nicht in einem Git-Repo (lokal mit
    Standardpfaden ohne Klon) oder hat die Arbeitskopie ungespeicherte Aenderungen an ihnen, wird nichts
    geschrieben und das laut gesagt: ein Stand, den niemand wiederherstellen kann, waere schlimmer als keiner."""
    dateien = [CATALOG_FILE, BASETHREATS_FILE, MAPPING_FILE, TAGS_FILE, TARGETS_FILE, DOCUMENTATION_FILE]
    try:
        top = Path(_git(CATALOG_FILE.resolve().parent, "rev-parse", "--show-toplevel").strip()).resolve()
        rels = [f.resolve().relative_to(top).as_posix() for f in dateien]
        unsauber = _git(top, "status", "--porcelain", "--", *rels).strip()
        sha = _git(top, "log", "-1", "--format=%H", "--", *rels).strip()
    except (RuntimeError, ValueError) as e:
        print(f"Upstream-Stand: nicht festgehalten ({e}); upstream.json bleibt unveraendert", file=sys.stderr)
        return None
    if unsauber or not sha:
        print("Upstream-Stand: Eingabedateien haben ungespeicherte Aenderungen oder keinen Commit; "
              "upstream.json bleibt unveraendert", file=sys.stderr)
        return None
    DATA_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_OUT_DIR / "upstream.json").write_text(
        json.dumps({"repository": EXPORT_SOURCE_URL, "commit": sha, "dateien": rels}, indent="\t", ensure_ascii=False) + "\n"
    )
    return sha


# --- Katalogzahlen in handgeschriebenen Seiten --------------------------------
# check_invariants() & Co. pruefen, was der Generator selbst schreibt. Diese
# Seiten schreibt niemand mit dem Generator, sie nennen aber Zahlen aus dem Katalog
# ("265", "149 MUSS", "11 Anforderungen"). Der taegliche Sync aendert den Katalog
# ohne sie anzufassen: dann steht die Zahl still falsch da, genau wie bei der
# Geschaeftsfuehrungs-Seite ("123 von 874"). Jede Aussage wird deshalb im Text
# gesucht und gegen eine eigene Rechnung aus dem Rohkatalog gehalten. Findet sich
# die Aussage nicht mehr (Satz umformuliert), ist das ebenfalls ein Fehler: dann
# muss das Muster hier nachgezogen werden, statt dass die Pruefung still ausfaellt.
# Nicht erfasst: Zahlen anderer BSI-Kataloge (WLAN, Lieferkette; kein Eingang des
# Generators) und Zahlen, die einen alten Stand beschreiben (befunde/muss-zahlen-gf-seite).
HANDWRITTEN_DOCS_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "docs"

_ZAHLWORT = {
    "de": {1: "ein", 2: "zwei", 3: "drei", 4: "vier", 5: "fünf", 6: "sechs", 7: "sieben", 8: "acht",
           9: "neun", 10: "zehn", 11: "elf", 12: "zwölf"},
    "en": {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
           9: "nine", 10: "ten", 11: "eleven", 12: "twelve"},
}
_MONATE_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
              "October", "November", "December"]


def _tausender(n, sep):
    return f"{n:,}".replace(",", sep)


def handwritten_catalog_facts(catalog, mapping_data, stats):
    """Die Zahlen, die handgeschriebene Seiten nennen, frisch aus dem Rohkatalog gerechnet."""
    controls = list(collect_controls(catalog))
    ids = {c["id"] for c in controls}
    praktik = lambda c: c["id"].split(".")[0]
    kategorie = lambda c: part_prop_value(c, "statement", "target_object_categories")
    verb = lambda c: part_prop_value(c, "statement", "modal_verb")

    zaehler = Counter((verb(c), prop_value(c, "sec_level")) for c in controls)
    muss_gesamt = sum(n for (v, _), n in zaehler.items() if v == "MUSS")
    kann_gesamt = sum(n for (v, _), n in zaehler.items() if v == "KANN")

    gefaehrdungen = [prop_value(c, "threats") for c in controls if prop_value(c, "threats")]
    genutzt = {k.strip() for c in controls if kategorie(c) for k in kategorie(c).split(",")}

    def prosa(teil):
        return [teil.get("prose", "")] + [s for sub in teil.get("parts", []) for s in prosa(sub)]

    def eintrag(c):
        # Titel plus der ganze Fliesstext der Anforderung (Aussage und Erlaeuterung).
        return " ".join([c["title"]] + [s for teil in c.get("parts", []) for s in prosa(teil)]).casefold()

    pentest = [c for c in controls if "penetrationstest" in eintrag(c)]

    # Anforderungen, auf die das Mapping des BSI zeigt UND die es im Katalog gibt.
    mit_vorgaenger = set()
    for gruppe in mapping_data["mapping-collection"]["mappings"]:
        for m in gruppe.get("maps", []):
            quelle, ziel = m.get("sources") or [{}], m.get("targets") or [{}]
            if m.get("relationship") and quelle[0].get("id-ref") and ziel[0].get("id-ref") in ids:
                mit_vorgaenger.add(ziel[0]["id-ref"])

    def tiefe(name):
        n = 1
        while TARGETS[name]["parent"]:
            name, n = TARGETS[name]["parent"], n + 1
        return n

    stand = catalog["metadata"]["last-modified"][:10]  # 2026-10-22
    jahr, monat, tag = (int(x) for x in stand.split("-"))
    ohne_kategorie = [c for c in controls if not kategorie(c)]
    return {
        "gesamt": len(controls),
        "praktiken": len({praktik(c) for c in controls}),
        "managementpraktiken": len({praktik(c) for c in controls} & MANAGEMENT_CYCLE_IDS),
        "themenfelder": len({praktik(c) for c in controls} - MANAGEMENT_CYCLE_IDS),
        "methodik": sum(1 for c in controls if praktik(c) in MANAGEMENT_CYCLE_IDS),
        "ohne_kategorie_praktiken": sum(1 for c in ohne_kategorie if praktik(c) not in MANAGEMENT_CYCLE_IDS),
        "mit_kategorie": len(controls) - len(ohne_kategorie),
        "muss_normal": zaehler[("MUSS", "normal-SdT")],
        "sollte_normal": zaehler[("SOLLTE", "normal-SdT")],
        "sollte_erhoeht": zaehler[("SOLLTE", "erhöht")],
        "kann_erhoeht": zaehler[("KANN", "erhöht")],
        "sollte_gesamt": zaehler[("SOLLTE", "normal-SdT")] + zaehler[("SOLLTE", "erhöht")],
        # "Alle N MUSS gehoeren zu normal-SdT": die Aussage gilt nur, solange das stimmt.
        "muss_alle_normal": str(muss_gesamt) if muss_gesamt == zaehler[("MUSS", "normal-SdT")] else "nicht alle normal-SdT",
        "kann_alle_erhoeht": str(kann_gesamt) if kann_gesamt == zaehler[("KANN", "erhöht")] else "nicht alle erhöht",
        "mit_gefaehrdungen": len(gefaehrdungen),
        "gefaehrdungen_verschieden": len({t.strip() for g in gefaehrdungen for t in g.split(",")}),
        "kategorien": len(TARGETS),
        "kategorien_alle_genutzt": str(len(TARGETS)) if genutzt == set(TARGETS) else f"nur {len(genutzt)} von {len(TARGETS)}",
        "wurzelknoten": sum(1 for info in TARGETS.values() if not info["parent"]),
        "ebenen": max(tiefe(n) for n in TARGETS),
        "pentest_anforderungen": len(pentest),
        "pentest_praktiken": len({praktik(c) for c in pentest}),
        "mit_vorgaenger": len(mit_vorgaenger),
        "bausteine_ohne_zuordnung": stats["bausteine_gesamt"] - stats["bausteine"],
        "stand_iso": stand,
        "stand_de": f"{tag:02d}.{monat:02d}.{jahr}",
        "stand_en": f"{tag} {_MONATE_EN[monat - 1]} {jahr}",
    }


def handwritten_claims(f):
    """(Datei, Muster, erwartete Gruppen): was die Seiten ueber den Katalog behaupten."""
    de = lambda n: _tausender(n, ".")
    en = lambda n: _tausender(n, ",")
    wd = lambda n: _ZAHLWORT["de"][n]
    we = lambda n: _ZAHLWORT["en"][n]
    s = str
    return [
        # methodik.mdx
        ("methodik.mdx", r"Anhang 1 des Standards definiert (\d+) davon", [s(f["kategorien"])]),
        ("methodik.mdx", r"Hierarchie aus (\w+) Wurzelknoten und (\w+) Ebenen", [wd(f["wurzelknoten"]), wd(f["ebenen"])]),
        ("methodik.mdx", r"Im Katalog sind das \*\*(\d+)\*\* Anforderungen", [s(f["methodik"])]),
        ("methodik.mdx", r"Im Katalog sind das \*\*(\d+)\*\*\.", [s(f["ohne_kategorie_praktiken"])]),
        ("methodik.mdx", r"tragen \*\*(\d+)\*\* Anforderungen die Kategorie", [s(f["mit_kategorie"])]),
        ("methodik.mdx", r"ergibt das die ([\d.]+) Anforderungen", [de(f["gesamt"])]),
        ("methodik.mdx", r"\(Stand (\d\d\.\d\d\.\d{4}), ([\d.]+) Anforderungen\)", [f["stand_de"], de(f["gesamt"])]),
        ("methodik.mdx", r"\| MUSS \| (\d+) \| normal-SdT \|", [s(f["muss_normal"])]),
        ("methodik.mdx", r"\| SOLLTE \| (\d+) \| normal-SdT \|", [s(f["sollte_normal"])]),
        ("methodik.mdx", r"\| SOLLTE \| (\d+) \| erhöht \|", [s(f["sollte_erhoeht"])]),
        ("methodik.mdx", r"\| KANN \| (\d+) \| erhöht \|", [s(f["kann_erhoeht"])]),
        ("methodik.mdx", r"tragen (\d+) von ([\d.]+) Anforderungen solche Angaben, insgesamt (\d+) verschiedene",
         [s(f["mit_gefaehrdungen"]), de(f["gesamt"]), s(f["gefaehrdungen_verschieden"])]),
        ("methodik.mdx", r"alle (\d+) Kategorien kommen vor", [f["kategorien_alle_genutzt"]]),
        # en/methodik.mdx
        ("en/methodik.mdx", r"Annex 1 of the standard defines (\d+) of them", [s(f["kategorien"])]),
        ("en/methodik.mdx", r"hierarchy of (\w+) root nodes and (\w+) levels", [we(f["wurzelknoten"]), we(f["ebenen"])]),
        ("en/methodik.mdx", r"In the catalog that is \*\*(\d+)\*\* requirements", [s(f["methodik"])]),
        ("en/methodik.mdx", r"In the catalog that is \*\*(\d+)\*\*\.", [s(f["ohne_kategorie_praktiken"])]),
        ("en/methodik.mdx", r"In the catalog, \*\*(\d+)\*\* requirements carry", [s(f["mit_kategorie"])]),
        ("en/methodik.mdx", r"that makes the ([\d,]+) requirements", [en(f["gesamt"])]),
        ("en/methodik.mdx", r"\(version (\d+ \w+ \d{4}), ([\d,]+) requirements\)", [f["stand_en"], en(f["gesamt"])]),
        ("en/methodik.mdx", r"\| MUSS \(must\) \| (\d+) \| normal-SdT \|", [s(f["muss_normal"])]),
        ("en/methodik.mdx", r"\| SOLLTE \(should\) \| (\d+) \| normal-SdT \|", [s(f["sollte_normal"])]),
        ("en/methodik.mdx", r"\| SOLLTE \(should\) \| (\d+) \| erhöht", [s(f["sollte_erhoeht"])]),
        ("en/methodik.mdx", r"\| KANN \(may\) \| (\d+) \| erhöht", [s(f["kann_erhoeht"])]),
        ("en/methodik.mdx", r"In the catalog, (\d+) of ([\d,]+) requirements carry such data, covering (\d+) distinct",
         [s(f["mit_gefaehrdungen"]), en(f["gesamt"]), s(f["gefaehrdungen_verschieden"])]),
        ("en/methodik.mdx", r"all (\d+) categories occur", [f["kategorien_alle_genutzt"]]),
        # rag.mdx
        ("rag.mdx", r"mit allen (\d+) Anforderungen", [s(f["gesamt"])]),
        ("rag.mdx", r"Bei (\d+) Anforderungen in (\d+) Praktiken", [s(f["gesamt"]), s(f["praktiken"])]),
        ("rag.mdx", r"kommt in (\w+) Anforderungen vor, verteilt auf (\w+) Praktiken",
         [wd(f["pentest_anforderungen"]), wd(f["pentest_praktiken"])]),
        ("rag.mdx", r"Bei (\d+) Anforderungen steht die ID der alten", [s(f["mit_vorgaenger"])]),
        ("rag.mdx", r"In der Datei stehen (\d+) MUSS-, (\d+) SOLLTE- und (\d+) KANN-Anforderungen",
         [s(f["muss_normal"]), s(f["sollte_gesamt"]), s(f["kann_erhoeht"])]),
        ("rag.mdx", r"Alle (\d+) MUSS-Anforderungen gehören zur Stufe \*normal-SdT\*, alle (\d+) KANN",
         [f["muss_alle_normal"], f["kann_alle_erhoeht"]]),
        ("rag.mdx", r"und (\d+) Bausteine haben noch keine", [s(f["bausteine_ohne_zuordnung"])]),
        # en/rag.mdx
        ("en/rag.mdx", r"with all (\d+) requirements", [s(f["gesamt"])]),
        ("en/rag.mdx", r"With (\d+) requirements in (\d+) practices", [s(f["gesamt"]), s(f["praktiken"])]),
        ("en/rag.mdx", r"appears in (\w+) requirements, spread over (\w+) practices",
         [we(f["pentest_anforderungen"]), we(f["pentest_praktiken"])]),
        ("en/rag.mdx", r"For (\d+) requirements, the ID of the old", [s(f["mit_vorgaenger"])]),
        ("en/rag.mdx", r"The file contains (\d+) MUSS, (\d+) SOLLTE and (\d+) KANN requirements",
         [s(f["muss_normal"]), s(f["sollte_gesamt"]), s(f["kann_erhoeht"])]),
        ("en/rag.mdx", r"All (\d+) MUSS requirements are at level \*normal-SdT\*, and all (\d+) KANN",
         [f["muss_alle_normal"], f["kann_alle_erhoeht"]]),
        ("en/rag.mdx", r"and (\d+) Bausteine have no mapping", [s(f["bausteine_ohne_zuordnung"])]),
        # rollen/isb.mdx und rollen/devs.mdx: erzeugt, aber diese Zahlen stehen fest im Generatortext
        ("rollen/isb.mdx", r"\(BSI, (\d+) Stück\)", [s(f["gefaehrdungen_verschieden"])]),
        ("rollen/isb.mdx", r"Die (\w+) Praktiken im Detail", [wd(f["managementpraktiken"])]),
        ("rollen/devs.mdx", r"kennt nur die (\d+) Themenfelder", [s(f["themenfelder"])]),
        # befunde/drei-sollte-mit-stufe-erhoeht.mdx
        ("befunde/drei-sollte-mit-stufe-erhoeht.mdx", r"\(Version (\d{4}-\d\d-\d\d), ([\d.]+) Anforderungen\)",
         [f["stand_iso"], de(f["gesamt"])]),
        ("befunde/drei-sollte-mit-stufe-erhoeht.mdx", r"\| MUSS \| normal-SdT \| (\d+) \|", [s(f["muss_normal"])]),
        ("befunde/drei-sollte-mit-stufe-erhoeht.mdx", r"\| SOLLTE \| normal-SdT \| (\d+) \|", [s(f["sollte_normal"])]),
        ("befunde/drei-sollte-mit-stufe-erhoeht.mdx", r"\| KANN \| erhöht \| (\d+) \|", [s(f["kann_erhoeht"])]),
        ("befunde/drei-sollte-mit-stufe-erhoeht.mdx", r"Alle (\d+) anderen Anforderungen dieser Stufe sind KANN", [s(f["kann_erhoeht"])]),
    ]


def handwritten_number_problems(catalog, mapping_data, stats, docs_dir=None):
    """Liste der Abweichungen zwischen Seitentext und Katalog (leer = alles stimmt)."""
    docs_dir = Path(docs_dir) if docs_dir else HANDWRITTEN_DOCS_DIR
    facts = handwritten_catalog_facts(catalog, mapping_data, stats)
    problems = []
    texts = {}
    for datei, muster, erwartet in handwritten_claims(facts):
        if datei not in texts:
            texts[datei] = (docs_dir / datei).read_text(encoding="utf-8")
        treffer = re.search(muster, texts[datei])
        if not treffer:
            problems.append(f"{datei}: Aussage nicht mehr gefunden ({muster}); Muster in handwritten_claims() nachziehen")
        elif list(treffer.groups()) != erwartet:
            problems.append(f"{datei}: steht {list(treffer.groups())}, der Katalog ergibt {erwartet} ({muster})")
    return problems


def check_handwritten_numbers(catalog, mapping_data, stats):
    problems = handwritten_number_problems(catalog, mapping_data, stats)
    if problems:
        raise SystemExit(
            "Zahlen in handgeschriebenen Seiten passen nicht zum Katalog:\n  - "
            + "\n  - ".join(problems)
            + "\nSeite anpassen (oder, wenn nur der Satz umformuliert wurde, das Muster in handwritten_claims())."
        )


def check_changelog(catalog, nur=None):
    """Rechnet changelog.json auf einem anderen Weg nach als update_changelog().

    nur: Menge von Commits, deren Eintraege vollstaendig nachgerechnet werden (dazu immer
    der neueste); None = alle. Im Normalbetrieb sind das nur die in diesem Lauf neu
    berechneten: ein aelterer Eintrag aendert sich nie und wurde beim Anlegen geprueft,
    und jede Nachrechnung laedt zwei Staende des Katalogs (je ~5 MB). Jeden Lauf alle zu
    pruefen wuerde den Sync-Workflow mit jedem neuen Stand teurer machen. Die Reihenfolge
    aller Eintraege wird immer geprueft. CHANGELOG_CHECK_ALL=1 in main() erzwingt alles.

    update_changelog() waehlt Felder gezielt aus (changelog_normalize). Hier wird jeder
    Stand stattdessen als flache Pfad->Wert-Tabelle des GANZEN Baums gelesen, ohne die
    Feldauswahl. Daran muessen sich ablesen lassen:
      A. Die Menge aller Anforderungen, die sich zwischen zwei Staenden irgendwie
         unterscheiden, ist genau "sichtbar geaendert" plus "technisch geaendert".
      B. Jedes gemeldete alt/neu steht so im jeweiligen Stand (bei Listenfeldern
         ohne Rolle der Reihenfolge); Texte bei eingesetzten Parametern.
      C. Die Wortvergleiche setzen sich zu alt und neu wieder zusammen.
      D. Der neueste Eintrag passt zum aktuell eingelesenen Katalog (wenn es derselbe
         Stand ist).
    """
    problems = []
    if not CHANGELOG_FILE.exists():
        raise SystemExit("Aenderungsprotokoll passt nicht zum Katalog:\n  - changelog.json fehlt")
    data = json.loads(CHANGELOG_FILE.read_text())
    top, rel, history = changelog_history(CATALOG_FILE)

    def flat(node, pre=""):
        out = {}
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "controls":
                    continue
                out.update(flat(v, f"{pre}/{k}"))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                if isinstance(v, dict) and v.get("name") == "alt-identifier":
                    continue
                # Elemente mit "name" (props, parts) heissen nach ihrem Namen, auch wenn sie
                # zusaetzlich eine id tragen (z. B. "GC.3.1.1_stm" fuer parts[statement]).
                key = (v.get("name") or v.get("id") or i) if isinstance(v, dict) else i
                out.update(flat(v, f"{pre}[{key}]"))
        else:
            out[pre] = node
        return out

    def tree(cat):
        out, labels = {}, {}
        def walk(n):
            for p in n.get("params", []):
                labels[p["id"]] = p.get("label", p["id"])
            for c in n.get("controls", []):
                out[c["id"]] = flat(c)
                walk(c)
            for g in n.get("groups", []):
                walk(g)
        walk(cat)
        return out, labels

    def subst(text, labels):
        if not text:
            return ""
        def one(m):
            return "[" + labels.get(m.group(1), m.group(1)) + "]"
        return " ".join(re.sub(r"\{\{\s*insert:\s*param,\s*([A-Za-z0-9._-]+)\s*\}\}", one, text).split())

    def pick(fl, labels, key):
        g = lambda path: fl.get(path) or ""
        s = "/parts[statement]"
        def lst(v):
            return ", ".join(sorted(x.strip() for x in v.split(",") if x.strip()))
        if key == "titel": return g("/title")
        if key == "anforderung": return subst(g(f"{s}/prose"), labels)
        if key == "erlaeuterung": return subst(g("/parts[guidance]/prose"), labels)
        if key == "pflichtgrad": return g(f"{s}/props[modal_verb]/value")
        if key == "stufe": return g("/props[sec_level]/value")
        if key == "aufwand": return g("/props[effort_level]/value")
        if key == "ergebnis": return g(f"{s}/props[result]/value")
        if key == "ergebnis_zusatz": return g(f"{s}/props[result_specification]/value")
        if key == "dokument": return g(f"{s}/props[documentation]/value")
        if key == "zielobjekte": return lst(g(f"{s}/props[target_object_categories]/value"))
        if key == "gefaehrdungen": return lst(g("/props[threats]/value"))
        if key == "tags": return lst(g("/props[tags]/value"))
        raise KeyError(key)

    with BASETHREATS_FILE.open(newline="", encoding="utf-8") as fh:
        threat_table = {r["ID"]: r["Begriff"] for r in csv.DictReader(fh)}
    by_commit = {c: d for c, d in history}
    prev_commit = data["basis"]["commit"] if data.get("basis") else None
    stand = None
    for e in sorted(data["eintraege"], key=lambda e: e["veroeffentlicht"]):
        if e["vorgaenger"] != prev_commit:
            problems.append(f"{e['commit'][:7]}: Vorgaenger {e['vorgaenger'][:7]} passt nicht zur Reihenfolge ({str(prev_commit)[:7]})")
        prev_commit = e["commit"]
        if nur is not None and e["commit"] not in nur and e["commit"] != data["stand"]["commit"]:
            continue  # alter Eintrag, beim Anlegen geprueft (siehe Docstring)
        if e["commit"] not in by_commit or e["vorgaenger"] not in by_commit:
            continue  # Historie nicht (mehr) lokal da; nur Pruefungen, die ohne sie gehen
        (o_tree, o_lab), (n_tree, n_lab) = tree(changelog_load(top, rel, e["vorgaenger"])), tree(changelog_load(top, rel, e["commit"]))
        # A: alle Unterschiede, generisch gefunden
        verschieden = {i for i in set(o_tree) & set(n_tree) if o_tree[i] != n_tree[i]}
        sichtbar = {a["id"] for a in e["aenderungen"]}
        technisch = {i for t in e["technische_aenderungen"] for i in t["ids"]}
        if verschieden != sichtbar | technisch:
            fehlt = sorted(verschieden - sichtbar - technisch)[:3]
            zuviel = sorted((sichtbar | technisch) - verschieden)[:3]
            problems.append(f"{e['commit'][:7]}: Menge der geaenderten Anforderungen weicht ab (fehlt im Protokoll: {fehlt}, zuviel: {zuviel})")
        if set(n_tree) - set(o_tree) != set(e["neu"]) or set(o_tree) - set(n_tree) != set(e["entfernt"]):
            problems.append(f"{e['commit'][:7]}: neue/entfernte Anforderungen stimmen nicht")
        if len(sichtbar) != len(e["aenderungen"]):
            problems.append(f"{e['commit'][:7]}: eine Anforderung kommt doppelt vor")
        # B und C: jede gemeldete Aenderung
        for a in e["aenderungen"]:
            for f in a["felder"]:
                alt, neu = pick(o_tree[a["id"]], o_lab, f["feld"]), pick(n_tree[a["id"]], n_lab, f["feld"])
                if f["alt"] != alt or f["neu"] != neu:
                    problems.append(f"{e['commit'][:7]} {a['id']} {f['name']}: alt/neu stimmen nicht mit dem Stand ueberein")
                if alt == neu:
                    problems.append(f"{e['commit'][:7]} {a['id']} {f['name']}: gemeldet, aber nicht verschieden")
                if "diff" in f:
                    if "".join(t for op, t in f["diff"] if op in "=-") != alt or "".join(t for op, t in f["diff"] if op in "=+") != neu:
                        problems.append(f"{e['commit'][:7]} {a['id']} {f['name']}: Wortvergleich setzt sich nicht zu alt/neu zusammen")
            if not a["felder"]:
                problems.append(f"{e['commit'][:7]} {a['id']}: Eintrag ohne Felder")
        for a in e["aenderungen"]:
            for f in a["felder"]:
                if f["feld"] == "gefaehrdungen":
                    ids = {x.strip() for x in (f["alt"] + "," + f["neu"]).split(",") if x.strip()}
                    if f.get("bezeichnungen") != {x: threat_table[x] for x in ids if x in threat_table}:
                        problems.append(f"{e['commit'][:7]} {a['id']}: Bezeichnungen der Gefaehrdungen stimmen nicht mit der BSI-Tabelle")
        for t in e["technische_aenderungen"]:
            if t["anzahl"] != len(t["ids"]) or len(set(t["ids"])) != len(t["ids"]):
                problems.append(f"{e['commit'][:7]} technische Aenderung {t['pfad']}: Anzahl/IDs widerspruechlich")
        stand = (e, n_tree, n_lab)

    # D: neuester Eintrag gegen den aktuellen Katalog
    if stand:
        e, n_tree, n_lab = stand
        cur_tree, cur_lab = tree(json.loads(CATALOG_FILE.read_text())["catalog"])
        if e["commit"] == data["stand"]["commit"] and e["commit"] == history[-1][0] and cur_tree == n_tree:
            for a in e["aenderungen"]:
                for f in a["felder"]:
                    if pick(cur_tree[a["id"]], cur_lab, f["feld"]) != f["neu"]:
                        problems.append(f"{a['id']} {f['name']}: neuer Wert im Protokoll weicht vom aktuellen Katalog ab")
        for a in (x for en in data["eintraege"] for x in en["aenderungen"]):
            if a["id"] not in cur_tree:
                problems.append(f"{a['id']}: steht im Protokoll, aber nicht im aktuellen Katalog")
    if problems:
        raise SystemExit("Aenderungsprotokoll passt nicht zum Katalog:\n  - " + "\n  - ".join(problems[:12]))
    n_ch = sum(len(e["aenderungen"]) for e in data["eintraege"])
    print(f"Aenderungsprotokoll ok: {len(data['eintraege'])} Staende, {n_ch} Aenderungen an Anforderungen")


def main():
    data = json.loads(CATALOG_FILE.read_text())
    catalog = data["catalog"]
    src = catalog_source(catalog)
    params_by_id = build_params_index(catalog)
    control_index = build_control_index(catalog)
    basethreats_by_id = load_basethreats()
    tags_by_id = load_tags()
    TARGETS.update(load_targets())
    mapping_data = json.loads(MAPPING_FILE.read_text())
    read_mapping_info(mapping_data)
    predecessor_index = build_predecessor_index(mapping_data)
    bausteine_data = json.loads(BAUSTEINE_LINKS_FILE.read_text())
    baustein_links = bausteine_data["bausteine"]
    BAUSTEIN_TITLES.update(bausteine_data.get("titel", {}))
    ohne_titel = sorted(set(baustein_links) - set(BAUSTEIN_TITLES))
    if ohne_titel:
        raise SystemExit(
            f"{len(ohne_titel)} Bausteine ohne offiziellen Titel in {BAUSTEINE_LINKS_FILE.name} "
            f"(\"titel\"): {ohne_titel[:5]}. Titel von der BSI-Seite (_source) nachtragen, "
            "nicht aus dem Dateinamen ableiten (siehe BAUSTEIN_TITLES)."
        )

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
            tags_by_id=tags_by_id,
            predecessor_index=predecessor_index,
            baustein_links=baustein_links,
            include_heading=False,
        )
        summary = first_sentence(group_description(group))
        meta_description = summary
        override = DESCRIPTION_OVERRIDES.get(group["id"])
        if override:
            if override["original"] == summary:
                meta_description = override["text"]
            else:
                print(
                    f"WARNUNG: Katalogtext von {group['id']} weicht von dem ab, "
                    "den DESCRIPTION_OVERRIDES ersetzt. Override wird nicht "
                    "angewendet; neue Fassung pruefen und Override anpassen.",
                    file=sys.stderr,
                )
        page_title = f"{group['id']} – {group['title']}"
        frontmatter = (
            "---\n"
            f"title: {yaml_quote(page_title)}\n"
            f"description: {yaml_quote(meta_description)}\n"
            "---\n\n"
        )
        write_mdx(OUT_DIR / f"{slug}.mdx", frontmatter, render_source_block(src, group["id"]) + body, section="Anforderung")

        entry = (group["id"], group["title"], slug, summary)
        (management if group["id"] in MANAGEMENT_CYCLE_IDS else themenfelder).append(entry)

    # Hieß vorher "Start" -- ein Navigationswort, das über den Inhalt der
    # Seite nichts aussagt und ohne jedes Keyword im Suchergebnis landete
    # (siehe Kommentar zu title in src/content/docs/index.mdx). Zahlen in
    # der description kommen aus denselben Listen, die ohnehin schon fuer
    # die Index-Abschnitte gebaut werden -- keine neue Datenquelle.
    index_summary = (
        f"Alle {len(management)} Praktiken des Managementsystems (PDCA-Zyklus) "
        f"und {len(themenfelder)} operativen Themenfelder von Grundschutz++ im "
        "Überblick, mit direktem Zugriff auf jede Anforderung."
    )
    index_lines = [
        "---\n"
        f"title: {yaml_quote('Grundschutz++ im Überblick')}\n"
        f"description: {yaml_quote(index_summary)}\n"
        "---\n\n",
        "Automatisch generiert aus dem OSCAL-Katalog. "
        "Nicht Teil des offiziellen BSI-Materials — eigene lesbare Aufbereitung.\n\n"
        "Alle Anforderungen als Tabelle: [als Excel-Datei exportieren](/export/). "
        "Nach System statt nach Praktik: [Anforderungen nach Zielobjektkategorie](/zielobjekte/). "
        "Nach Dokument: [Dokumente im Katalog](/dokumente/).\n\n",
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
        "---\n"
        f"title: {yaml_quote('Status & Zeitplan')}\n"
        f"description: {yaml_quote('Der Meilensteinplan des BSI für Grundschutz++: Pilotphase, Veröffentlichung auf der it-sa, Zertifizierbarkeit ab 2027 und Übergangszeit.')}\n"
        "---\n\n",
        "Grundschutz++ ersetzt das bisherige IT-Grundschutz-Kompendium nicht von "
        "heute auf morgen. Die Termine folgen dem "
        f"[Meilensteinplan des BSI]({BSI_MEILENSTEINE_URL}) (Stand Oktober 2026, "
        f"von uns am {BSI_MEILENSTEINE_STAND} abgerufen); das BSI passt ihn laufend an. "
        "Der bisherige IT-Grundschutz bleibt laut BSI in einer „mehrjährigen "
        "Übergangszeit“ anwendbar. Ein Enddatum dafür und ein Datum für die "
        "vollständige Ablösung des Kompendiums nennt das BSI nicht. Fest steht "
        "nur das Ende der Zertifizierbarkeit nach bisherigem IT-Grundschutz am "
        "30.11.2031.\n\n"
        "Zwischen den Meilensteinen ändert sich der Katalog laufend. Die "
        "Unterschiede zwischen den veröffentlichten Ständen stehen im "
        "[Änderungsprotokoll](/aenderungen/).\n",
        render_timeline(),
    ]
    (OUT_DIR / "zeitplan.mdx").write_text("\n".join(zeitplan_lines))

    themen_count, themen_tagged = render_themen_page(catalog, control_index, tags_by_id)
    zielobjekt_count = render_zielobjekt_pages(catalog, control_index)
    dokument_count = render_dokument_pages(
        catalog, control_index, params_by_id, basethreats_by_id, predecessor_index, load_documentation_guidelines()
    )

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
            render_baustein_page(baustein_id, entries, baustein_links, control_index, group_titles, by_baustein)
        )

    stats = write_landing_data(
        catalog, control_index, by_baustein, all_mappings, params_by_id, baustein_links
    )
    write_status_data()
    write_bausteine_data(by_baustein, baustein_links)
    changelog_stats = update_changelog(CATALOG_FILE, basethreats_by_id)
    upstream_commit = update_upstream_stand()
    export_stats = write_export_data(
        catalog, params_by_id, basethreats_by_id, predecessor_index, load_documentation_guidelines()
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
    check_export(catalog)
    check_zielobjekte(catalog)
    check_dokumente(catalog)
    check_sync_paths()
    check_handwritten_numbers(catalog, mapping_data, stats)
    check_changelog(
        catalog,
        None if os.environ.get("CHANGELOG_CHECK_ALL") else set(changelog_stats.get("commits", [])),
    )

    total = len(management) + len(themenfelder)
    print(f"{total} Gruppen-Seiten (.mdx) erzeugt in {OUT_DIR}")
    print(f"3 Rollen-Seiten (.mdx) erzeugt in {ROLLEN_OUT_DIR}")
    print(f"{len(by_baustein)} Baustein-Seiten + Übersicht erzeugt in {VERGLEICH_OUT_DIR}")
    print(f"{zielobjekt_count} Zielobjekt-Seiten + Übersicht erzeugt in {ZIELOBJEKTE_OUT_DIR}")
    print(f"{dokument_count} Dokument-Seiten + Übersicht erzeugt in {DOKUMENTE_OUT_DIR}")
    print(f"Startseiten-Daten: {stats}")
    print(f"Upstream-Stand: {upstream_commit[:7] if upstream_commit else 'nicht festgehalten'} (src/data/upstream.json)")
    print(f"Aenderungsprotokoll: {changelog_stats['neu']} neu, {changelog_stats['gesamt']} Staende in changelog.json")
    print(f"Export-Dateien in {EXPORT_OUT_DIR}: {export_stats}")

    def sidebar_group(label, entries):
        items = ",\n\t\t\t\t\t\t".join(
            f'{{ label: "{gid} {title}", slug: "grundschutzpp/{slug}" }}' for gid, title, slug, _ in entries
        )
        return f'{{\n\t\t\t\t\tlabel: "{label}",\n\t\t\t\t\titems: [\n\t\t\t\t\t\t{items},\n\t\t\t\t\t],\n\t\t\t\t}}'

    print("\nastro.config.mjs Sidebar-Snippet (manuell einfügen falls gewünscht):\n")
    print(sidebar_group("Managementsystem", management) + ",\n" + sidebar_group("Themenfelder", themenfelder))


if __name__ == "__main__":
    main()
