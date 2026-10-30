"""Prueft die Geschaeftsfuehrungs-Seite und den Export-Hinweis gegen BSI-Standard 300-1.

Aufruf (der Katalog muss angegeben werden, kein stilles Ueberspringen):

    GRUNDSCHUTZPP_CATALOG=<pfad>/Grundschutz++-resolved_catalog.json \\
    GRUNDSCHUTZPP_BASETHREATS=... GRUNDSCHUTZPP_TAGS=... GRUNDSCHUTZPP_TARGETS=... \\
    GRUNDSCHUTZPP_MAPPING=... GRUNDSCHUTZPP_DOCUMENTATION=... \\
    python3 -m unittest discover -s scripts/tests

Die Zahlen werden hier unabhaengig vom Generator aus dem Roh-JSON gezaehlt.
"""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_docs", ROOT / "scripts" / "generate_docs.py")
    module = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
    return module


def walk_controls(node):
    for control in node.get("controls", []):
        yield control
        yield from walk_controls(control)
    for group in node.get("groups", []):
        yield from walk_controls(group)


def statement_prop(control, name):
    for part in control.get("parts", []):
        if part.get("name") == "statement":
            for prop in part.get("props", []):
                if prop["name"] == name:
                    return prop["value"]
    return None


def sec_level(control):
    for prop in control.get("props", []):
        if prop["name"] == "sec_level":
            return prop["value"]
    return None


class GeschaeftsfuehrungSeite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalog_path = os.environ.get("GRUNDSCHUTZPP_CATALOG")
        if not catalog_path:
            raise RuntimeError("GRUNDSCHUTZPP_CATALOG nicht gesetzt: ohne Katalog laesst sich nichts pruefen")
        cls.catalog = json.loads(Path(catalog_path).read_text())["catalog"]
        generator = load_generator()
        cls.tmp = tempfile.TemporaryDirectory()
        generator.ROLLEN_OUT_DIR = Path(cls.tmp.name)
        groups = cls.catalog["groups"]
        groups_by_id = {g["id"]: g for g in groups}
        entries = [(g["id"], g["title"], g["id"].lower(), "") for g in groups]
        management = [e for e in entries if e[0] in generator.MANAGEMENT_CYCLE_IDS]
        themenfelder = [e for e in entries if e[0] not in generator.MANAGEMENT_CYCLE_IDS]
        generator.render_geschaeftsfuehrung_page(management, themenfelder, groups_by_id)
        cls.page = (Path(cls.tmp.name) / "geschaeftsfuehrung.mdx").read_text()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_kein_wirkungsloser_filter(self):
        # Alle MUSS sind normal-SdT: ein Filter nach Sicherheitsstufe filtert nichts
        # (Standard) oder blendet die ganze Seite aus (erhoeht).
        self.assertNotIn("GfFilter", self.page)
        self.assertNotIn("gf-sec", self.page)

    def test_zahlen_stehen_im_text(self):
        controls = list(walk_controls(self.catalog))
        muss = [c for c in controls if statement_prop(c, "modal_verb") == "MUSS"]
        muss_normal = [c for c in muss if sec_level(c) == "normal-SdT"]
        self.assertEqual(len(muss), len(muss_normal), "Annahme der Seite: alle MUSS sind normal-SdT")
        self.assertIn(f"{len(muss_normal)} von {len(muss)} MUSS-Anforderungen", self.page)


class ExportHinweis(unittest.TestCase):
    def test_kein_schutzbedarf_gleich_stufe(self):
        # BSI-Standard 300-1 (3.4.2): Schutzbedarf hoch fuehrt zur Risikobeurteilung,
        # die Stufe "erhoeht" ist ein Pool optionaler KANN. Beides ist nicht 1:1.
        source = (ROOT / "src" / "components" / "ExportTabelle.astro").read_text()
        self.assertNotIn("Bei höherem Schutzbedarf gilt die erhöhte Stufe", source)
        self.assertNotIn("Dann beide anhaken", source)


if __name__ == "__main__":
    unittest.main()
