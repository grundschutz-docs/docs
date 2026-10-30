"""Befunde: Frontmatter und <BefundMeta> sagen dasselbe, und "Betrifft" fuehrt zu den Seiten.

Jede Befund-Seite nennt typ, status, gefunden, betrifft und quelle zweimal: im Frontmatter (fuer
die Liste unter /befunde/) und als Props von <BefundMeta> (fuer die Anzeige auf der Seite). Beides
wird von Hand gepflegt und lief auseinander: editon-tippfehler-vergleichsseiten.mdx nannte
betrifft nur im Frontmatter, die Seite zeigte kein "Betrifft".
"""
import re
import unittest
from pathlib import Path

BEFUNDE = Path(__file__).resolve().parent.parent.parent / "src" / "content" / "docs" / "befunde"


def frontmatter_befund(text):
    fm = text.split("---")[1]
    felder = {}
    for schluessel in ("typ", "status", "gefunden", "quelle"):
        m = re.search(rf"^  {schluessel}: (.+)$", fm, re.M)
        felder[schluessel] = m.group(1).strip().strip("\"'") if m else None
    m = re.search(r"^  betrifft: \[(.*?)\]", fm, re.M | re.S)
    felder["betrifft"] = [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []
    return felder


def komponenten_props(text):
    m = re.search(r"<BefundMeta(.*?)/>", text, re.S)
    props = m.group(1)
    felder = {}
    for schluessel in ("typ", "status"):
        v = re.search(rf'{schluessel}="([^"]*)"', props)
        felder[schluessel] = v.group(1) if v else None
    v = re.search(r"gefunden=\{new Date\('([^']*)'\)\}", props)
    felder["gefunden"] = v.group(1) if v else None
    v = re.search(r'quelle="([^"]*)"', props)
    felder["quelle"] = v.group(1) if v else None
    v = re.search(r"betrifft=\{\[(.*?)\]\}", props, re.S)
    felder["betrifft"] = [x.strip().strip("'\"") for x in v.group(1).split(",") if x.strip()] if v else []
    return felder


class BefundeKonsistenz(unittest.TestCase):
    def test_frontmatter_und_komponente_stimmen_ueberein(self):
        seiten = [p for p in sorted(BEFUNDE.glob("*.mdx")) if p.name != "index.mdx"]
        self.assertGreater(len(seiten), 8)
        abweichungen = []
        for seite in seiten:
            text = seite.read_text(encoding="utf-8")
            fm, comp = frontmatter_befund(text), komponenten_props(text)
            for schluessel in fm:
                if fm[schluessel] != comp[schluessel]:
                    abweichungen.append(f"{seite.name}: {schluessel}: Frontmatter {fm[schluessel]!r}, Komponente {comp[schluessel]!r}")
        self.assertEqual(abweichungen, [])


if __name__ == "__main__":
    unittest.main()
