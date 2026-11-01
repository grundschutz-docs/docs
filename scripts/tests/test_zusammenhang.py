"""Verweise zwischen Anforderungen auf den Praktikseiten ("Voraussetzung laut Katalog", "Verwandt laut Katalog").

Ohne Katalog pruefbar: Jeder Verweis zeigt auf eine Anforderung, die es mit genau diesem Anker auf genau dieser
Seite gibt, und keine Anforderung verweist auf sich selbst. Gegen den Rohkatalog rechnet check_zusammenhang() im
Generator (laeuft bei jedem Sync).
"""
import re
import unittest
from pathlib import Path

SEITEN = Path(__file__).resolve().parent.parent.parent / "src" / "content" / "docs" / "grundschutzpp"
ANKER = re.compile(r"\{#([A-Z]+(?:\.[0-9]+)+)\}")
ZEILE = re.compile(r'<p class="zusammenhang[^"]*" data-art="([a-z_]+)"[^>]*>(.*?)</p>')
LINK = re.compile(r'href="/grundschutzpp/([a-z]+)/#([A-Z0-9.]+)"')
UEBERSCHRIFT = re.compile(r"^#{3,6} ([A-Z]+(?:\.[0-9]+)+) – .*\{#\1\}\s*$", re.M)


class Verweise(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.anker = {}  # ID -> Seite
        cls.zeilen = []  # (Seite, ID der Anforderung, Art, [(Zielseite, Ziel-ID)])
        for datei in sorted(SEITEN.glob("*.mdx")):
            text = datei.read_text(encoding="utf-8")
            for a in ANKER.findall(text):
                cls.anker[a] = datei.stem
            treffer = list(UEBERSCHRIFT.finditer(text))
            for i, m in enumerate(treffer):
                ende = treffer[i + 1].start() if i + 1 < len(treffer) else len(text)
                for art, inhalt in ZEILE.findall(text[m.end():ende]):
                    cls.zeilen.append((datei.stem, m.group(1), art, LINK.findall(inhalt)))

    def test_es_gibt_verweise(self):
        self.assertTrue(self.zeilen)
        self.assertEqual({z[2] for z in self.zeilen}, {"voraussetzung", "voraussetzung_von", "verwandt"})

    def test_jeder_verweis_trifft_einen_anker_auf_der_richtigen_seite(self):
        falsch = []
        for seite, cid, art, ziele in self.zeilen:
            self.assertTrue(ziele, f"{cid}: {art} ohne Link")
            for zielseite, ziel in ziele:
                if self.anker.get(ziel) != zielseite:
                    falsch.append((cid, art, ziel, zielseite))
        self.assertEqual(falsch, [])

    def test_kein_selbstverweis_und_keine_doppelten(self):
        for seite, cid, art, ziele in self.zeilen:
            ids = [z for _, z in ziele]
            self.assertNotIn(cid, ids, f"{cid} verweist auf sich selbst ({art})")
            self.assertEqual(len(ids), len(set(ids)), f"{cid}: doppelte Verweise ({art})")


if __name__ == "__main__":
    unittest.main()
