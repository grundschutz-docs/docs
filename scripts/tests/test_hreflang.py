"""hreflang verspricht nur Seiten, die es gibt und die Suchmaschinen aufnehmen dürfen.

Gelesen wird der Build in dist/ (vorher `pnpm build`). Ohne Build wird der Test übersprungen.
Starlight schreibt für jede Seite einen Verweis auf die englische Fassung, auch wenn es nur den
Fallback gibt (deutscher Text unter /en/, noindex). src/starlightRouteData.ts nimmt diese Verweise
heraus; der Test hält das fest.
"""
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse

DIST = Path(__file__).resolve().parent.parent.parent / "dist"
LINK = re.compile(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"\s*/?>')


def seite_zu(url):
    pfad = urlparse(url).path
    return DIST / pfad.strip("/") / "index.html"


@unittest.skipUnless(DIST.is_dir(), "dist/ fehlt, erst bauen")
class Hreflang(unittest.TestCase):
    def seiten(self):
        return [p for p in DIST.rglob("index.html") if "pagefind" not in p.parts]

    def test_jedes_ziel_existiert_und_ist_indexierbar(self):
        fehler = []
        for seite in self.seiten():
            for sprache, url in LINK.findall(seite.read_text(encoding="utf-8")):
                ziel = seite_zu(url)
                if not ziel.is_file():
                    fehler.append(f"{seite.relative_to(DIST)}: hreflang={sprache} zeigt auf {url}, die Seite fehlt")
                elif "noindex" in ziel.read_text(encoding="utf-8"):
                    fehler.append(f"{seite.relative_to(DIST)}: hreflang={sprache} zeigt auf {url}, die auf noindex steht")
        self.assertEqual(fehler, [])

    def test_es_gibt_hreflang_auf_uebersetzten_seiten(self):
        # Gegenprobe: ein Test, der nichts findet, wäre trivial grün.
        html = (DIST / "methodik" / "index.html").read_text(encoding="utf-8")
        self.assertIn('hreflang="en"', html)


if __name__ == "__main__":
    unittest.main()
