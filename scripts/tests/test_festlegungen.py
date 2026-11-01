"""Festlegungen (Blatt "Festlegungen" der Excel-Datei): Daten gegen den Katalog gerechnet.

1. Immer: die JSON-Datei ist in sich stimmig (Zahl, Platzhalter-Text und Reihenfolge gegen die eckigen
   Klammern im Anforderungstext, durchnummeriert, nur zwei Vorgaben).
2. Mit GRUNDSCHUTZPP_CATALOG (OSCAL-Katalog des BSI): gegen die Parameter im Rohkatalog, unabhaengig vom
   Generator gelesen.
"""
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
JSON = ROOT / "public" / "downloads" / "grundschutzpp-anforderungen.json"
KLAMMER = re.compile(r"\[([^\]]+)\]")


class FestlegungenImExport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.daten = json.loads(JSON.read_text(encoding="utf-8"))
        cls.f = cls.daten["festlegungen"]

    def test_platzhalter_wie_im_anforderungstext(self):
        erwartet = {a["id"]: KLAMMER.findall(a["anforderung"]) for a in self.daten["anforderungen"]}
        erwartet = {i: k for i, k in erwartet.items() if k}
        gefunden = {}
        for x in self.f:
            gefunden.setdefault(x["id"], []).append(x["platzhalter"])
        self.assertEqual(gefunden, erwartet)

    def test_durchnummeriert(self):
        je_id = {}
        for x in self.f:
            je_id.setdefault(x["id"], []).append(x["nr"])
        for i, nummern in je_id.items():
            self.assertEqual(nummern, list(range(1, len(nummern) + 1)), i)

    def test_nur_zwei_vorgegebene_werte(self):
        # Der Katalog legt nur zwei Werte selbst fest. Alles andere bleibt dem Anwender ueberlassen.
        self.assertEqual(
            sorted((x["id"], x["vorgabe"]) for x in self.f if x["vorgabe"]),
            [("GC.1.1", "BSI Grundschutz++"), ("NOT.1.1.4", "BSI-Standard 200-4")],
        )

    def test_zahlen_aus_der_analyse(self):
        self.assertEqual((len(self.f), len({x["id"] for x in self.f})), (224, 211))


@unittest.skipUnless(os.environ.get("GRUNDSCHUTZPP_CATALOG"), "GRUNDSCHUTZPP_CATALOG nicht gesetzt")
class FestlegungenGegenOscal(unittest.TestCase):
    def test_gegen_die_parameter_im_rohkatalog(self):
        cat = json.loads(Path(os.environ["GRUNDSCHUTZPP_CATALOG"]).read_text(encoding="utf-8"))["catalog"]
        raw = {}

        def walk(node):
            for c in node.get("controls", []) or []:
                if c.get("params"):
                    raw[c["id"]] = [(p.get("label"), ", ".join(p.get("values") or [])) for p in c["params"]]
                walk(c)
            for g in node.get("groups", []) or []:
                walk(g)

        walk(cat)
        daten = json.loads(JSON.read_text(encoding="utf-8"))
        je_id = {}
        for x in daten["festlegungen"]:
            je_id.setdefault(x["id"], []).append((x["platzhalter"], x["vorgabe"]))
        self.assertEqual(je_id, raw)


if __name__ == "__main__":
    unittest.main()
