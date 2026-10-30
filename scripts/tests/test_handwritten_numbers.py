"""Katalogzahlen in handgeschriebenen Seiten (methodik, rag, Befunde) gegen den Katalog.

Der Generator prueft nur, was er selbst schreibt. Diese Seiten nennen Zahlen wie "265" oder
"149 von 1000" von Hand: aendert der taegliche Sync den Katalog, stuenden sie still falsch da.
check_handwritten_numbers() rechnet jede Aussage aus dem Katalog nach und sucht sie im Text.

Gebraucht werden dieselben Umgebungsvariablen wie fuer test_p0_fachlich.py.
"""
import copy
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DOCS = ROOT / "src" / "content" / "docs"


class HandgeschriebeneZahlen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.environ.get("GRUNDSCHUTZPP_CATALOG"):
            raise RuntimeError("GRUNDSCHUTZPP_CATALOG nicht gesetzt: ohne Katalog laesst sich nichts pruefen")
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("generate_docs", ROOT / "scripts" / "generate_docs.py")
        cls.g = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.g)
        cls.g.TARGETS.update(cls.g.load_targets())
        cls.catalog = json.loads(cls.g.CATALOG_FILE.read_text())["catalog"]
        cls.mapping = json.loads(cls.g.MAPPING_FILE.read_text())
        cls.stats = json.loads((ROOT / "src" / "data" / "landing.json").read_text())["stats"]

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.docs = Path(self.tmp.name) / "docs"
        shutil.copytree(DOCS, self.docs)

    def tearDown(self):
        self.tmp.cleanup()

    def problems(self, catalog=None, docs=None):
        return self.g.handwritten_number_problems(
            catalog or self.catalog, self.mapping, self.stats, docs or self.docs
        )

    def edit(self, rel, old, new):
        path = self.docs / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, f"{rel}: Testannahme stimmt nicht mehr")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_heutige_seiten_stimmen(self):
        self.assertEqual(self.problems(), [])

    def test_falsche_zahl_im_text_wird_gefunden(self):
        self.edit("methodik.mdx", "Im Katalog sind das **265**.", "Im Katalog sind das **266**.")
        meldungen = self.problems()
        self.assertEqual(len(meldungen), 1, meldungen)
        self.assertIn("methodik.mdx", meldungen[0])
        self.assertIn("266", meldungen[0])
        self.assertIn("265", meldungen[0])

    def test_umformulierte_aussage_faellt_auf(self):
        # Ohne das wuerde ein umgeschriebener Satz still aus der Pruefung fallen.
        self.edit("en/rag.mdx", "appears in eleven requirements", "shows up in eleven requirements")
        meldungen = self.problems()
        self.assertTrue(any("en/rag.mdx" in m and "nicht mehr gefunden" in m for m in meldungen), meldungen)

    def test_aenderung_im_katalog_wird_gefunden(self):
        # Ein MUSS wird SOLLTE: dann stimmen die Zahlen in methodik, rag und im Befund nicht mehr.
        geaendert = copy.deepcopy(self.catalog)
        for control in self.g.collect_controls(geaendert):
            if self.g.is_muss(control):
                for part in control["parts"]:
                    if part["name"] == "statement":
                        for p in part["props"]:
                            if p["name"] == "modal_verb":
                                p["value"] = "SOLLTE"
                break
        dateien = {m.split(":")[0] for m in self.problems(geaendert)}
        self.assertTrue({"methodik.mdx", "rag.mdx", "en/methodik.mdx", "en/rag.mdx"} <= dateien, dateien)


if __name__ == "__main__":
    unittest.main()
