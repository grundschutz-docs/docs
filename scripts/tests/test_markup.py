"""Struktur des gebauten HTML, die axe nicht prueft.

Gepruft wird gegen einen fertigen Build (dist/, oder Pfad in DIST), ueber alle Seiten:

1. Hoechstens ein <figcaption> je <figure> (HTML-Spezifikation).
2. Der Export-Bereich ist keine ganze aria-live-Region: sonst liest Hilfstechnik bei jeder
   Aenderung den Bereich samt allen Knoepfen vor. Live ist nur der Zaehler.
3. Jedes fokussierbare Element mit data-tooltip (Pille ohne Link) bietet den Tooltip-Text
   auch als aria-label an: der Tooltip ist reines CSS (::after) und fuer Hilfstechnik unsichtbar.
5. Jede ID unter "Betrifft" auf einer Befund-Seite ist ein Link (Anforderung, Vergleichsseite oder
   "Bausteine ohne Zuordnung"), nicht nur Code.
4. Die englische Seite zu NIS2 (/en/operating-in-germany/) ist von jeder englischen Seite aus ueber
   den Footer erreichbar, von deutschen Seiten aus nicht (dort gibt es sie nicht).
"""
import os
import unittest
from html.parser import HTMLParser
from pathlib import Path

DIST = Path(os.environ.get("DIST", Path(__file__).resolve().parent.parent.parent / "dist"))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Pruefer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []  # (tag, attrs)
        self.figcaptions = []  # je offener Figure: Anzahl Figcaptions
        self.figure_tiefe = []  # Index in self.stack der offenen Figures
        self.mehrere_figcaptions = 0
        self.tooltips_ohne_label = []
        self.export_result_live = False
        self.count_in_live = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "figure":
            self.figcaptions.append(0)
        elif tag == "figcaption" and self.figcaptions:
            self.figcaptions[-1] += 1
            if self.figcaptions[-1] == 2:
                self.mehrere_figcaptions += 1
        if "data-tooltip" in a and "tabindex" in a and tag != "a":
            if a["data-tooltip"] and a["data-tooltip"] not in (a.get("aria-label") or ""):
                self.tooltips_ohne_label.append(f"<{tag} {a.get('data-tooltip')[:40]!r}>")
        classes = (a.get("class") or "").split()
        if "export-result" in classes and ("aria-live" in a or a.get("role") == "status"):
            self.export_result_live = True
        if a.get("id") == "export-count":
            self.count_in_live = any(
                "aria-live" in attrs_ or attrs_.get("role") == "status" for _, attrs_ in self.stack
            )
        if tag not in VOID:
            self.stack.append((tag, a))

    def handle_endtag(self, tag):
        if tag == "figure" and self.figcaptions:
            self.figcaptions.pop()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


class GebautesHtml(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DIST.is_dir():
            raise RuntimeError(f"{DIST} fehlt: erst bauen (pnpm build)")
        cls.seiten = {}
        for datei in sorted(DIST.rglob("*.html")):
            pruefer = Pruefer()
            pruefer.feed(datei.read_text(encoding="utf-8"))
            cls.seiten[str(datei.relative_to(DIST))] = pruefer
        assert len(cls.seiten) > 400, "zu wenige Seiten im Build"

    def test_hoechstens_ein_figcaption_je_figure(self):
        falsch = [s for s, p in self.seiten.items() if p.mehrere_figcaptions]
        self.assertEqual(falsch, [])

    def test_export_bereich_ist_keine_live_region(self):
        p = self.seiten["export/index.html"]
        self.assertIsNotNone(p.count_in_live, "Zaehler #export-count nicht gefunden")
        self.assertFalse(p.export_result_live, ".export-result ist als ganze Region live")
        self.assertTrue(p.count_in_live, "der Zaehler #export-count ist nicht live")

    def test_tooltips_stehen_auch_im_aria_label(self):
        falsch = {s: p.tooltips_ohne_label[:2] for s, p in self.seiten.items() if p.tooltips_ohne_label}
        self.assertEqual(falsch, {})


class EnglischeNavigation(unittest.TestCase):
    ZIEL = 'href="/en/operating-in-germany/"'

    @classmethod
    def setUpClass(cls):
        if not DIST.is_dir():
            raise RuntimeError(f"{DIST} fehlt: erst bauen (pnpm build)")
        cls.html = {str(p.relative_to(DIST)): p.read_text(encoding="utf-8") for p in sorted(DIST.rglob("*.html"))}

    def test_jede_englische_seite_verlinkt_im_footer_auf_nis2(self):
        en = {s: h for s, h in self.html.items() if s.startswith("en/")}
        self.assertGreater(len(en), 100)
        ohne = [s for s, h in en.items() if self.ZIEL not in h.split("<footer", 1)[-1]]
        self.assertEqual(ohne[:5], [])

    def test_deutsche_seiten_verlinken_nicht_darauf(self):
        mit = [s for s, h in self.html.items() if not s.startswith("en/") and self.ZIEL in h]
        self.assertEqual(mit[:5], [])


class BefundBetrifft(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DIST.is_dir():
            raise RuntimeError(f"{DIST} fehlt: erst bauen (pnpm build)")
        cls.seiten = {
            str(p.relative_to(DIST)): p.read_text(encoding="utf-8")
            for p in sorted((DIST / "befunde").glob("*/index.html"))
        }

    def test_betrifft_ids_sind_links(self):
        import re

        gesehen, ohne_link = 0, []
        for seite, html in self.seiten.items():
            m = re.search(r"<dt[^>]*>Betrifft</dt>\s*<dd[^>]*>(.*?)</dd>", html, re.S)
            if not m:
                continue
            for code in re.findall(r"<code[^>]*>(.*?)</code>", m.group(1)):
                gesehen += 1
                if not re.search(rf"<a [^>]*href=\"[^\"]+\"[^>]*>\s*<code[^>]*>{re.escape(code)}</code>", m.group(1)):
                    ohne_link.append(f"{seite}: {code}")
        self.assertGreater(gesehen, 25, "zu wenige Betrifft-IDs gefunden")
        self.assertEqual(ohne_link[:5], [])


if __name__ == "__main__":
    unittest.main()
