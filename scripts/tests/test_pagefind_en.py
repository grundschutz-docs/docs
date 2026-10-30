"""Der englische Suchindex soll nur englische Seiten enthalten.

Starlight baut fuer jede nicht uebersetzte Seite eine Fallback-Route unter /en/ mit dem
deutschen Text. Head.astro setzt dort noindex, Pagefind beachtet das aber nicht. Gepruft wird
gegen einen fertigen Build (dist/, oder Pfad in DIST):

  Pagefind-Seiten der Sprache en  ==  Seiten unter dist/en/, die kein noindex tragen

Beide Seiten der Gleichung kommen aus verschiedenen Quellen (Pagefind-Index, HTML).
"""
import json
import os
import re
import unittest
from pathlib import Path

DIST = Path(os.environ.get("DIST", Path(__file__).resolve().parent.parent.parent / "dist"))


class PagefindEnglisch(unittest.TestCase):
    def test_nur_echte_englische_seiten_im_index(self):
        if not DIST.is_dir():
            raise RuntimeError(f"{DIST} fehlt: erst bauen (pnpm build)")
        seiten = list((DIST / "en").rglob("index.html"))
        echt = [p for p in seiten if 'name="robots" content="noindex' not in p.read_text(encoding="utf-8")]
        # Gegenprobe: der Test muss Fallback-Seiten ueberhaupt sehen, sonst beweist er nichts.
        self.assertGreater(len(seiten) - len(echt), 0, "keine Fallback-Seiten gefunden")
        entry = json.loads((DIST / "pagefind" / "pagefind-entry.json").read_text())
        self.assertEqual(entry["languages"]["en"]["page_count"], len(echt))


if __name__ == "__main__":
    unittest.main()
