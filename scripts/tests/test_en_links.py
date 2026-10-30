"""Englische Seiten sollen auf die englische Fassung verlinken, wenn es eine gibt.

Ausnahme: Datenschutz und Impressum verweisen mit Absicht auf die deutsche Fassung,
weil nur sie rechtlich massgeblich ist (steht im Text dieser Seiten).
"""
import re
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent / "src" / "content" / "docs"
ERLAUBT = {("datenschutz.mdx", "datenschutz"), ("impressum.mdx", "impressum")}
LINK = re.compile(r'(?:\]\(|href=")/([a-z0-9-]+)/?(?:#[^)")]*)?[)"]')


class EnglischeLinks(unittest.TestCase):
    def test_kein_link_auf_deutsche_seite_mit_englischer_fassung(self):
        englisch = {p.stem for p in (DOCS / "en").glob("*.mdx")}
        falsch = []
        for seite in sorted((DOCS / "en").glob("*.mdx")):
            for slug in LINK.findall(seite.read_text(encoding="utf-8")):
                if slug in englisch and (seite.name, slug) not in ERLAUBT:
                    falsch.append(f"{seite.name}: /{slug}/ statt /en/{slug}/")
        self.assertEqual(falsch, [])


if __name__ == "__main__":
    unittest.main()
