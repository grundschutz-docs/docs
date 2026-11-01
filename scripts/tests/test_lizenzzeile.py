"""Jede gebaute Seite trägt die Lizenzzeile (CC BY-SA 4.0 verlangt Urheber, Lizenz, Quelle, Hinweis auf Bearbeitung).

Gelesen wird der Build in dist/ (vorher `pnpm build`). Ohne Build wird der Test übersprungen.
Auf /methodik/ gilt die Zeile zum BSI-Standard 300-1, weil der nicht unter CC BY-SA steht.
"""
import unittest
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent.parent / "dist"
METHODIK = {DIST / "methodik" / "index.html", DIST / "en" / "methodik" / "index.html"}
# Weiterleitungen und 404-Seiten sind keine Inhaltsseiten.
AUSNAHMEN = {DIST / "404.html"}


@unittest.skipUnless(DIST.is_dir(), "dist/ fehlt, erst bauen")
class Lizenzzeile(unittest.TestCase):
    def seiten(self):
        return [p for p in DIST.rglob("*.html") if p not in AUSNAHMEN and "pagefind" not in p.parts]

    def test_jede_seite_hat_die_zeile(self):
        ohne = []
        for seite in self.seiten():
            html = seite.read_text(encoding="utf-8")
            if "data-license-line" not in html:
                # Weiterleitungen (meta refresh) haben keinen Footer.
                if 'http-equiv="refresh"' in html:
                    continue
                ohne.append(str(seite.relative_to(DIST)))
        self.assertEqual(ohne, [])

    def test_katalogzeile_nennt_lizenz_und_quelle(self):
        for seite in self.seiten():
            if seite in METHODIK:
                continue
            html = seite.read_text(encoding="utf-8")
            if "data-license-line" not in html:
                continue
            with self.subTest(seite=str(seite.relative_to(DIST))):
                self.assertIn("CC BY-SA 4.0", html)
                self.assertIn("BSI-Bund/Stand-der-Technik-Bibliothek", html)

    def test_methodik_nennt_die_nutzungsbedingungen(self):
        for seite in METHODIK:
            if not seite.exists():
                continue
            html = seite.read_text(encoding="utf-8")
            zeile = html.split("data-license-line", 1)[1].split("</p>", 1)[0]
            with self.subTest(seite=str(seite.relative_to(DIST))):
                self.assertIn("Nutzungsbedingungen", zeile + "terms of use")
                self.assertNotIn("CC BY-SA", zeile)


if __name__ == "__main__":
    unittest.main()
