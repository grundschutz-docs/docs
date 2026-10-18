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
BSI_MEILENSTEINE_STAND = "18.10.2026"
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
        "Die Methodik soll am 27.10.2026 auf der it-sa veröffentlicht werden. Die Erkenntnisse aus der Erprobung fließen in sie ein.",
        "post-pilot refinement phase",
        "The methodology is due to be published at it-sa on 27 October 2026. Findings from the pilot feed into it.",
        None, True,
    ),
    (
        date(2026, 10, 27), date(2026, 10, 29),
        "Veröffentlichung der Methodik auf der it-sa",
        "Das BSI stellt die Methodik auf der it-sa 2026 in Nürnberg vor und der Community zur Anwendung bereit.",
        "launch week at it-sa",
        "The BSI presents the methodology at it-sa 2026 in Nuremberg and makes it available to the community.",
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
    predecessors = render_predecessors_prop(control["id"], predecessor_index, baustein_links)
    if not (modal_verb or sec_level or effort or threats or tags or predecessors):
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
    laufend = [
        entry
        for entry in TIMELINE
        if entry[7] and entry[0] <= today and (entry[1] is None or today <= entry[1])
    ]
    if not laufend:
        raise SystemExit(
            f"Keine Phase in TIMELINE umfasst heute ({today.isoformat()}). "
            "Die Status-Leiste haette nichts anzuzeigen -- TIMELINE in "
            "scripts/generate_docs.py fortschreiben."
        )
    # Kuerzeste Phase gewinnt; bei Gleichstand der spaetere Eintrag (siehe
    # Kommentar an TIMELINE).
    start, end, label, detail, label_en, detail_en, _range_text, _banner = min(
        reversed(laufend), key=lambda p: (p[1] - p[0]).days if p[1] else 10**6
    )

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
        '<div class="table-scroll">\n<table class="bsig-table">\n'
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
        GF_FILTER_IMPORT,
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
        # siehe GfFilter.astro), sie legt die Kriterien nur so hin, dass man
        # sie selbst anwenden kann.
        '<div class="table-scroll">\n'
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
        "- **[Vergleich: Altes Kompendium ↔ Grundschutz++](/vergleich/)** — "
        "jede Zuordnung zwischen alter und neuer Anforderung, mit "
        f"Beziehungstyp ({'/'.join(RELATIONSHIP_LABELS.values())}) und "
        "echten Links zu den Baustein-PDFs des BSI.\n"
        "- **Basisgefährdungen direkt am Control** — jede Anforderung zeigt "
        "die zugeordneten elementaren Gefährdungen (BSI, 47 Stück) als "
        "hoverbare Pille, ohne extra Nachschlagen in `basethreats.csv`.\n"
        "- **[Status & Zeitplan](/grundschutzpp/zeitplan/)** — Meilensteinplan "
        "des BSI, Übergangszeit, Zertifizierung.\n\n"
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
        render_baustein_summary(entries, group_titles),
        "\n",
        '<div class="vergleich-section not-content">\n',
        '<div class="table-scroll">\n',
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
            '<div class="table-scroll">\n',
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
            '<div class="table-scroll">\n',
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


def render_source_block(src):
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
    return (
        '<div class="source-note">\n'
        f"<p>{zeile} — Quelle: "
        '<a href="https://github.com/BSI-Bund/Stand-der-Technik-Bibliothek" '
        'target="_blank" rel="noopener noreferrer">BSI Stand-der-Technik-Bibliothek</a>.</p>\n'
        "<details>\n<summary>Eine Anforderung von dieser Seite zitieren</summary>\n"
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


def main():
    data = json.loads(CATALOG_FILE.read_text())
    catalog = data["catalog"]
    src = catalog_source(catalog)
    params_by_id = build_params_index(catalog)
    control_index = build_control_index(catalog)
    basethreats_by_id = load_basethreats()
    tags_by_id = load_tags()
    mapping_data = json.loads(MAPPING_FILE.read_text())
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
        write_mdx(OUT_DIR / f"{slug}.mdx", frontmatter, render_source_block(src) + body, section="Anforderung")

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
        "30.11.2031.\n",
        render_timeline(),
    ]
    (OUT_DIR / "zeitplan.mdx").write_text("\n".join(zeitplan_lines))

    themen_count, themen_tagged = render_themen_page(catalog, control_index, tags_by_id)

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
