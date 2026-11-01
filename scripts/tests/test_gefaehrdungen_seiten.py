"""Gefaehrdungs-Seiten (/gefaehrdungen/): je Seite die Anforderungen, die der Katalog der Gefaehrdung zuordnet.

Gerechnet wird gegen die Export-JSON (Spalte "Gefaehrdungen" je Anforderung), also gegen einen anderen Weg als
check_gefaehrdungen() im Generator, der den Rohkatalog liest. Gelesen werden die erzeugten .mdx-Seiten.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SEITEN = ROOT / "src" / "content" / "docs" / "gefaehrdungen"
EXPORT = ROOT / "public" / "downloads" / "grundschutzpp-anforderungen.json"


def slug(tid):
    return re.sub(r"[^a-z0-9]+", "-", tid.lower()).strip("-")


class GefaehrdungsSeiten(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        daten = json.loads(EXPORT.read_text(encoding="utf-8"))
        cls.je = {}
        cls.muss = {}
        for r in daten["anforderungen"]:
            for g in r["gefaehrdungen"]:
                tid = g.split(" – ")[0]
                cls.je.setdefault(tid, set()).add(r["id"])
                cls.muss[tid] = cls.muss.get(tid, 0) + (r["pflichtgrad"] == "MUSS")

    def test_eine_seite_je_gefaehrdung(self):
        self.assertEqual({d.stem for d in SEITEN.glob("*.mdx")} - {"index"}, {slug(t) for t in self.je})

    def test_anforderungen_je_seite_wie_im_export(self):
        for tid, ids in self.je.items():
            with self.subTest(tid):
                text = (SEITEN / f"{slug(tid)}.mdx").read_text(encoding="utf-8")
                self.assertEqual(sorted(re.findall(r'data-id="([^"]+)"', text)), sorted(ids))
                self.assertIn(f"## Anforderungen ({len(ids)})", text)
                self.assertIn(f"{self.muss[tid]} MUSS", text)

    def test_keine_bewertung_in_den_seiten(self):
        # Rote Linie: die Seiten sagen, was der Katalog zuordnet, nicht was wichtig ist oder gilt.
        for d in SEITEN.glob("*.mdx"):
            # Nur unser eigener Text: das Zitat der BSI-Definition (Zeilen mit ">") und die Tabelle mit den
            # Titeln der Anforderungen (ab "## Anforderungen") gehoeren dem BSI.
            kopf = d.read_text(encoding="utf-8").split("## Anforderungen")[0]
            text = "\n".join(z for z in kopf.split("\n") if not z.startswith(">")).lower()
            for wort in ("wichtigste", "kritisch", "empfehlen", "sie müssen", "ihr müsst"):
                self.assertNotIn(wort, text, f"{d.name}: {wort!r}")

    def test_zahlen_der_analyse(self):
        self.assertEqual(len(self.je), 47)
        self.assertEqual(len(self.je["G 0.18"]), 385)


if __name__ == "__main__":
    unittest.main()
