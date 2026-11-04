"""Jede Anforderungs-ID in den von Hand geschriebenen Seiten gibt es im Katalog.

Beispiele wie "NOT.4.10" stehen im Text, nicht in den Daten: benennt das BSI eine Anforderung um oder
streicht sie, veraltet das Beispiel, ohne dass ein Build rot wird. Gelesen werden die Seiten direkt unter
src/content/docs/ (deutsch und en/) und die Datei mit allen Anforderungen unter public/downloads/. Nur IDs
mit einem Praktik-Kuerzel des neuen Katalogs zaehlen; alte IDs des Kompendiums (SYS.1.1, ISMS.1) nicht.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DOCS = ROOT / "src" / "content" / "docs"
KATALOG = json.loads((ROOT / "public" / "downloads" / "grundschutzpp-anforderungen.json").read_text(encoding="utf-8"))
IDS = {a["id"] for a in KATALOG["anforderungen"]}
PRAKTIKEN = {p["id"] for p in KATALOG["praktiken"]}


class BeispielIds(unittest.TestCase):
    def test_ids_in_handgeschriebenen_seiten_existieren(self):
        self.assertGreater(len(IDS), 500)
        muster = re.compile(r"\b(?:" + "|".join(sorted(PRAKTIKEN)) + r")(?:\.\d+){2,}\b")
        seiten = sorted(DOCS.glob("*.mdx")) + sorted((DOCS / "en").glob("*.mdx"))
        fehlend = sorted({f"{s.relative_to(ROOT)}: {m.group(0)}" for s in seiten for m in muster.finditer(s.read_text(encoding="utf-8")) if m.group(0) not in IDS})
        self.assertEqual(fehlend, [])

    def test_es_werden_ids_gefunden(self):
        # Gegenprobe: ein Test, der nirgends eine ID findet, waere trivial gruen.
        muster = re.compile(r"\b(?:" + "|".join(sorted(PRAKTIKEN)) + r")(?:\.\d+){2,}\b")
        gefunden = [m.group(0) for s in DOCS.glob("*.mdx") for m in muster.finditer(s.read_text(encoding="utf-8"))]
        self.assertTrue(gefunden)


if __name__ == "__main__":
    unittest.main()
