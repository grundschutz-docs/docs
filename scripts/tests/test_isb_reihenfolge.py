"""rollen/isb.mdx: Grafik und Liste nennen die Praktiken in derselben Reihenfolge.

Die Grafik (PdcaCycle) folgt dem Ablauf PDCA: GC, STM, UMS, PERF, VRB (RISK in der Mitte). Die
Liste "Die sechs Praktiken im Detail" folgte der Katalog-Reihenfolge, in der VRB vor PERF steht,
und sagt "Dieselben sechs Praktiken als Liste": mit vertauschten Plaetzen von PERF und VRB.
"""
import re
import unittest
from pathlib import Path

ISB = Path(__file__).resolve().parent.parent.parent / "src" / "content" / "docs" / "rollen" / "isb.mdx"


class IsbReihenfolge(unittest.TestCase):
    def test_liste_folgt_der_grafik(self):
        text = ISB.read_text(encoding="utf-8")
        knoten = text.split("<PdcaCycle", 1)[1].split("/>", 1)[0].split("risk=", 1)[0]
        grafik = re.findall(r'\{ id: "([A-Z]+)"', knoten)
        risk = re.search(r'risk=\{\{ id: "([A-Z]+)"', text).group(1)
        liste = re.findall(r'<li><a href="/grundschutzpp/([a-z]+)/">', text)
        self.assertEqual(len(grafik), 5)
        self.assertEqual([g.upper() for g in liste], grafik + [risk])


if __name__ == "__main__":
    unittest.main()
