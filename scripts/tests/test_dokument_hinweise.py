"""Hinweise des Generators auf Auffaelligkeiten in documentation_guidelines.csv (BSI_CSV_HINWEISE).

Der Mechanismus: ein Eintrag gilt nur, solange die Tabelle des BSI noch genau diesen Text hat. Aendert das
BSI ihn oder faellt die Zeile weg, bricht der Generator mit einer Meldung ab, statt einen Hinweis zu
zeigen, der nicht mehr stimmt. Der erste Eintrag war "Outsourcing-Strategie" (Definition beschrieb die
Informationssicherheitsstrategie); das BSI hat den Text am 23.11.2026 geaendert, der Eintrag ist entfallen.
Der Mechanismus wird hier mit einem Beispieleintrag gegen den aktuellen Text der Zeile geprueft.
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
NAME = "Outsourcing-Strategie"
HINWEIS = "Beispielhinweis fuer den Test."


class DokumentHinweise(unittest.TestCase):
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

    def seiten(self, guidelines, hinweise):
        alt = self.g.BSI_CSV_HINWEISE
        self.g.BSI_CSV_HINWEISE = hinweise
        try:
            with tempfile.TemporaryDirectory() as tmp:
                self.g.DOKUMENTE_OUT_DIR = Path(tmp)
                self.g.render_dokument_pages(self.catalog, *self.args, guidelines)
                return {p.name: p.read_text(encoding="utf-8") for p in Path(tmp).glob("*.mdx")}
        finally:
            self.g.BSI_CSV_HINWEISE = alt

    def beispiel(self, guidelines):
        anfang = guidelines[NAME]["beschreibung"][:30]
        return {NAME: {"beginnt_mit": anfang, "hinweis": HINWEIS}}

    def test_aktuell_traegt_keine_seite_einen_hinweis(self):
        self.assertEqual(self.g.BSI_CSV_HINWEISE, {})
        seiten = self.seiten(self.guidelines, self.g.BSI_CSV_HINWEISE)
        self.assertGreater(len(seiten), 50)
        self.assertEqual([n for n, t in seiten.items() if "**Hinweis:**" in t], [])

    def test_eintrag_erscheint_nur_auf_der_eigenen_seite(self):
        seiten = self.seiten(self.guidelines, self.beispiel(self.guidelines))
        self.assertEqual([n for n, t in seiten.items() if HINWEIS in t], ["outsourcing-strategie.mdx"])

    def test_hinweis_verfaellt_wenn_das_bsi_den_text_aendert(self):
        hinweise = self.beispiel(self.guidelines)
        geaendert = copy.deepcopy(self.guidelines)
        geaendert[NAME]["beschreibung"] = "Eine Strategie für ausgelagerte Dienste."
        with self.assertRaises(SystemExit) as fehler:
            self.seiten(geaendert, hinweise)
        self.assertIn(NAME, str(fehler.exception))
        self.assertIn("veraltet", str(fehler.exception))


if __name__ == "__main__":
    unittest.main()
