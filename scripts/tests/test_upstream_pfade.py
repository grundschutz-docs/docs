"""Die Pfade der BSI-Eingabedateien stehen an drei Stellen: src/data/upstream.json (schreibt der Generator),
.github/workflows/sync-catalog.yml und .github/workflows/generated.yml (je als GRUNDSCHUTZPP_*-Variablen,
dazu der sparse-checkout). Verschiebt das BSI eine Datei, muss alles zusammen angepasst werden; dieser Test
meldet, wenn eine Kopie abweicht, statt dass der naechste Sync still das Falsche holt.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
UPSTREAM = json.loads((ROOT / "src" / "data" / "upstream.json").read_text(encoding="utf-8"))
WORKFLOWS = {name: (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8") for name in ("sync-catalog.yml", "generated.yml")}
VAR = re.compile(r"^\s+GRUNDSCHUTZPP_\w+:\s*upstream/(\S+)\s*$", re.M)
SPARSE = re.compile(r"sparse-checkout:\s*\|\n((?:\s+\S+\n)+)")


class UpstreamPfade(unittest.TestCase):
    def test_workflows_lesen_dieselben_dateien_wie_upstream_json(self):
        erwartet = set(UPSTREAM["dateien"])
        self.assertEqual(len(erwartet), 6, "upstream.json nennt sechs Eingabedateien")
        for name, text in WORKFLOWS.items():
            with self.subTest(workflow=name):
                self.assertEqual(set(VAR.findall(text)), erwartet)

    def test_sparse_checkout_deckt_jede_datei_ab(self):
        for name, text in WORKFLOWS.items():
            with self.subTest(workflow=name):
                treffer = SPARSE.search(text)
                self.assertIsNotNone(treffer, f"{name}: kein sparse-checkout gefunden")
                ordner = [z.strip() for z in treffer.group(1).splitlines() if z.strip()]
                for datei in UPSTREAM["dateien"]:
                    self.assertTrue(any(datei.startswith(o + "/") for o in ordner), f"{name}: {datei} liegt in keinem Ordner des sparse-checkout")

    def test_pin_ist_ein_commit(self):
        self.assertRegex(UPSTREAM["commit"], r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
