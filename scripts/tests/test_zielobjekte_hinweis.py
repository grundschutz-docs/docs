"""ADR-0011: Anforderungen mit zwei Zielobjektkategorien stehen auf beiden Kategorieseiten.

Der Katalog sagt nicht, ob "oder" oder "und" gemeint ist. Die Seiten lesen es als "oder" und
sagen, dass das unsere Lesart ist, keine Aussage des BSI. Das stand nur auf der Uebersichtsseite
(zielobjekte/index.mdx), nicht auf den Seiten, auf denen die Zeilen "(auch fuer ...)" stehen.
Ausserdem war die zweite Kategorie dort nur Text, kein Link.

Gelesen werden die vom Generator erzeugten Seiten unter src/content/docs/zielobjekte/.
"""
import re
import unittest
from pathlib import Path

SEITEN = Path(__file__).resolve().parent.parent.parent / "src" / "content" / "docs" / "zielobjekte"
HINWEIS = "wir lesen es als „oder“. Das ist unsere Lesart, keine Aussage des BSI."
AUCH_FUER = re.compile(r"\(auch für ([^)]*)\)")


class ZweiKategorien(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seiten = {p.name: p.read_text(encoding="utf-8") for p in sorted(SEITEN.glob("*.mdx")) if p.name != "index.mdx"}
        cls.mit_auch = {n: t for n, t in cls.seiten.items() if AUCH_FUER.search(t)}
        assert len(cls.seiten) == 39, f"{len(cls.seiten)} Kategorieseiten gefunden"
        assert cls.mit_auch, "keine Seite mit (auch für …) gefunden: der Test prueft sonst nichts"

    def test_jede_betroffene_seite_nennt_die_lesart(self):
        fehlt = [n for n, t in self.mit_auch.items() if HINWEIS not in t]
        self.assertEqual(fehlt, [])

    def test_seite_ohne_zwei_kategorien_hat_den_hinweis_nicht(self):
        zuviel = [n for n, t in self.seiten.items() if n not in self.mit_auch and HINWEIS in t]
        self.assertEqual(zuviel, [])

    def test_zweite_kategorie_ist_verlinkt(self):
        unverlinkt = []
        for name, text in self.mit_auch.items():
            for treffer in AUCH_FUER.findall(text):
                if "<a href=" not in treffer:
                    unverlinkt.append(f"{name}: {treffer}")
        self.assertEqual(unverlinkt[:5], [])


if __name__ == "__main__":
    unittest.main()
