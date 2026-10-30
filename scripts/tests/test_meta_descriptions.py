"""Titel und Beschreibungen, die in Suchergebnissen stehen.

1. /en/ versprach in title, description und og:title "in English" und "English-language rendering" des
   Katalogs, die Seite selbst sagt aber "Browse the requirements (German)". Das fuehrt zu Absprüngen.
2. Die 94 Vergleichsseiten hatten bis auf den Namen dieselbe Beschreibung. Wer nach einer alten
   Baustein-ID sucht, will im Snippet sehen, wohin der Baustein gegangen ist: das Themenfeld mit den
   meisten Nachfolgern (wie im ersten Absatz der Seite). Gegengerechnet aus der Mapping-Datei.
3. Die Dokumentseiten schrieben "mit der Beschreibung des BSI, soweit vorhanden", auch dort, wo es keine
   gibt, und verschenkten den ersten Satz der BSI-Beschreibung. Der Text stammt aus der Seite selbst.

Gelesen werden die vom Generator erzeugten Seiten (src/content/docs/...).
"""
import json
import os
import re
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent / "src" / "content" / "docs"


def frontmatter(text, feld):
    m = re.search(rf'^{feld}: "?(.*?)"?$', text, re.M)
    return m.group(1) if m else None


class EnglischeStartseite(unittest.TestCase):
    def test_versprechen_passt_zur_seite(self):
        text = (DOCS / "en" / "index.mdx").read_text(encoding="utf-8")
        kopf = text.split("hero:", 1)[0]
        self.assertIn("Browse the requirements (German)", text, "Annahme: die Seite sagt selbst, dass der Katalog deutsch ist")
        titel, beschreibung = frontmatter(kopf, "title"), frontmatter(kopf, "description")
        og = re.search(r"property: og:title\s+content: (.*)", kopf).group(1)
        for name, wert in [("title", titel), ("description", beschreibung), ("og:title", og)]:
            with self.subTest(name):
                self.assertNotIn("in English", wert)
                self.assertNotIn("English-language rendering", wert)
        self.assertIn("German", beschreibung, "die Beschreibung muss sagen, dass die Katalogseiten deutsch sind")


class Vergleichsbeschreibungen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.environ.get("GRUNDSCHUTZPP_MAPPING"):
            raise RuntimeError("GRUNDSCHUTZPP_MAPPING nicht gesetzt")
        mapping = json.loads(Path(os.environ["GRUNDSCHUTZPP_MAPPING"]).read_text())
        felder = {}  # alter Baustein -> neue ID -> Themenfeld
        for gruppe in mapping["mapping-collection"]["mappings"]:
            for m in gruppe.get("maps", []):
                quelle, ziel = m.get("sources") or [{}], m.get("targets") or [{}]
                alt, neu = quelle[0].get("id-ref"), ziel[0].get("id-ref")
                b = re.match(r"^([A-Z]+(?:\.[0-9]+)+)\.A", alt or "")
                if m.get("relationship") and b and neu:
                    felder.setdefault(b.group(1), set()).add(neu)
        cls.erwartet = {}
        for baustein, neue in felder.items():
            zaehler = {}
            for n in neue:
                zaehler[n.split(".")[0]] = zaehler.get(n.split(".")[0], 0) + 1
            cls.erwartet[baustein.lower().replace(".", "-")] = sorted(zaehler.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]

    def test_beschreibung_nennt_das_haupt_themenfeld(self):
        falsch = []
        seiten = [p for p in sorted((DOCS / "vergleich").glob("*.mdx")) if p.name != "index.mdx"]
        self.assertEqual({p.stem for p in seiten}, set(self.erwartet))
        for seite in seiten:
            beschreibung = frontmatter(seite.read_text(encoding="utf-8"), "description")
            if not re.search(rf"\b{self.erwartet[seite.stem]}\b", beschreibung):
                falsch.append(f"{seite.name}: erwartet {self.erwartet[seite.stem]} in {beschreibung!r}")
        self.assertEqual(falsch[:3], [], f"{len(falsch)} von {len(seiten)} Seiten ohne Themenfeld")


class Dokumentbeschreibungen(unittest.TestCase):
    def test_keine_leere_floskel_und_der_erste_satz_des_bsi(self):
        seiten = [p for p in sorted((DOCS / "dokumente").glob("*.mdx")) if p.name != "index.mdx"]
        self.assertGreater(len(seiten), 55)
        mit_floskel, mit_zitat, ohne_zitat = [], 0, 0
        for seite in seiten:
            text = seite.read_text(encoding="utf-8")
            beschreibung = frontmatter(text, "description")
            if "soweit vorhanden" in beschreibung:
                mit_floskel.append(seite.name)
            zitat = re.search(r"\*\*Beschreibung des BSI\*\*\n\n> (.+)", text)
            if zitat and "nicht die Outsourcing-Strategie" not in text:
                mit_zitat += 1
                satz = re.split(r"(?<=[.!?])\s", zitat.group(1).replace("\\", ""), maxsplit=1)[0]
                # Der Satz des BSI nennt oft nicht, um welches Dokument es geht: der Name steht davor.
                titel = frontmatter(text, "title")
                if not beschreibung.startswith(f"{titel}: {satz[:40]}"):
                    mit_floskel.append(f"{seite.name}: {beschreibung[:60]!r} beginnt nicht mit Name und BSI-Satz")
            else:
                ohne_zitat += 1
        self.assertGreater(mit_zitat, 40, "zu wenige Seiten mit BSI-Beschreibung gefunden")
        self.assertGreater(ohne_zitat, 3)
        self.assertEqual(mit_floskel[:4], [], f"{len(mit_floskel)} Seiten")


if __name__ == "__main__":
    unittest.main()
