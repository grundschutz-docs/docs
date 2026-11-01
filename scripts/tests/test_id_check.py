"""Daten des ID-Checks (/id-check/) stimmen mit dem Änderungsprotokoll und dem Katalog überein.

Gelesen wird der Build (dist/aenderungen/ids.json, vorher `pnpm build`); ohne Build wird übersprungen.
Der Check zeigt nur, was im Änderungsprotokoll steht. Darum wird hier jede Änderung dort gegen die
ausgelieferte Datei gerechnet, nicht gegen eine zweite, eigene Quelle.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
IDS = ROOT / "dist" / "aenderungen" / "ids.json"
CHANGELOG = ROOT / "src" / "data" / "changelog.json"
KATALOG = ROOT / "public" / "downloads" / "grundschutzpp-anforderungen.json"


@unittest.skipUnless(IDS.exists(), "dist/ fehlt, erst bauen")
class IdCheckDaten(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.daten = json.loads(IDS.read_text(encoding="utf-8"))
        cls.log = json.loads(CHANGELOG.read_text(encoding="utf-8"))

    def test_ids_sind_der_katalog(self):
        katalog = json.loads(KATALOG.read_text(encoding="utf-8"))
        self.assertEqual(self.daten["ids"], [a["id"] for a in katalog["anforderungen"]])

    def test_jede_aenderung_ist_enthalten(self):
        erwartet = sorted(
            (a["id"], e["veroeffentlicht"][:10], e["commit"][:7])
            for e in self.log["eintraege"] for a in e["aenderungen"]
        )
        vorhanden = sorted(
            (i, a["datum"], a["commit"]) for i, liste in self.daten["aenderungen"].items() for a in liste
        )
        self.assertEqual(vorhanden, erwartet)

    def test_felder_stimmen(self):
        for e in self.log["eintraege"]:
            for a in e["aenderungen"]:
                gefunden = [x for x in self.daten["aenderungen"][a["id"]] if x["commit"] == e["commit"][:7]]
                self.assertEqual(len(gefunden), 1, a["id"])
                self.assertEqual(gefunden[0]["felder"], [f["name"] for f in a["felder"]], a["id"])

    def test_stand_und_beginn(self):
        self.assertEqual(self.daten["stand"]["commit"], self.log["stand"]["commit"])
        self.assertEqual(self.daten["beginn"], self.log["basis"]["veroeffentlicht"][:10])

    def test_nur_geaenderte_ids_haben_eintraege(self):
        # Keine Platzhalter und keine Angaben der Nutzenden: nur IDs aus dem Katalog oder dem Änderungsprotokoll.
        bekannt = set(self.daten["ids"])
        for i in self.daten["aenderungen"]:
            self.assertIn(i, bekannt)


if __name__ == "__main__":
    unittest.main()
