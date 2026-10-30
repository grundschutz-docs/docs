"""Hinweis auf der Seite "Outsourcing Strategie": der Text der BSI-Tabelle beschreibt ein anderes Dokument.

In documentation_guidelines.csv beginnt die Definition der Zeile "Outsourcing-Strategie" mit
"Informationssicherheitsstrategie:" und beschreibt dieses Dokument. Die Seite zeigt den Text des BSI
unveraendert und sagt dazu, was daran auffaellt.

Der Hinweis hat ein eingebautes Verfallsdatum: er gilt nur, solange die Tabelle noch genau diesen
Text hat. Aendert das BSI ihn, bricht der Generator mit einer Meldung ab, statt einen Hinweis zu
zeigen, der nicht mehr stimmt.
"""
import copy
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


class OutsourcingHinweis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.environ.get("GRUNDSCHUTZPP_CATALOG"):
            raise RuntimeError("GRUNDSCHUTZPP_CATALOG nicht gesetzt")
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("generate_docs", ROOT / "scripts" / "generate_docs.py")
        g = cls.g = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(g)
        g.TARGETS.update(g.load_targets())
        cls.catalog = json.loads(g.CATALOG_FILE.read_text())["catalog"]
        mapping = json.loads(g.MAPPING_FILE.read_text())
        g.read_mapping_info(mapping)
        cls.args = (
            g.build_control_index(cls.catalog),
            g.build_params_index(cls.catalog),
            g.load_basethreats(),
            g.build_predecessor_index(mapping),
        )
        cls.guidelines = g.load_documentation_guidelines()

    def seiten(self, guidelines):
        with tempfile.TemporaryDirectory() as tmp:
            self.g.DOKUMENTE_OUT_DIR = Path(tmp)
            self.g.render_dokument_pages(self.catalog, *self.args, guidelines)
            return {p.name: p.read_text(encoding="utf-8") for p in Path(tmp).glob("*.mdx")}

    def test_seite_nennt_den_befund_und_zeigt_den_bsi_text_unveraendert(self):
        seite = self.seiten(self.guidelines)["outsourcing-strategie.mdx"]
        self.assertIn("nach unserer Lesart dieses Dokument, nicht die Outsourcing-Strategie", seite)
        self.assertIn("(/befunde/dokumenttypen-katalog-und-csv/#outsourcing-strategie)", seite)
        self.assertIn("Informationssicherheitsstrategie: Ein übergeordnetes Dokument", seite)

    def test_andere_seiten_haben_den_hinweis_nicht(self):
        seiten = self.seiten(self.guidelines)
        self.assertGreater(len(seiten), 50)
        mit = [n for n, t in seiten.items() if "nicht die Outsourcing-Strategie" in t]
        self.assertEqual(mit, ["outsourcing-strategie.mdx"])

    def test_hinweis_verfaellt_wenn_das_bsi_den_text_aendert(self):
        geaendert = copy.deepcopy(self.guidelines)
        geaendert["Outsourcing-Strategie"]["beschreibung"] = "Eine Strategie für ausgelagerte Dienste."
        with self.assertRaises(SystemExit) as fehler:
            self.seiten(geaendert)
        self.assertIn("Outsourcing-Strategie", str(fehler.exception))
        self.assertIn("veraltet", str(fehler.exception))


if __name__ == "__main__":
    unittest.main()
