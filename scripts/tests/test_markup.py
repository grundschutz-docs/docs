"""Struktur des gebauten HTML, die axe nicht prueft.

Gepruft wird gegen einen fertigen Build (dist/, oder Pfad in DIST), ueber alle Seiten:

1. Hoechstens ein <figcaption> je <figure> (HTML-Spezifikation).
2. Der Export-Bereich ist keine ganze aria-live-Region: sonst liest Hilfstechnik bei jeder
   Aenderung den Bereich samt allen Knoepfen vor. Live ist nur der Zaehler.
3. Jedes fokussierbare Element mit data-tooltip (Pille ohne Link) bietet den Tooltip-Text
   auch als aria-label an: der Tooltip ist reines CSS (::after) und fuer Hilfstechnik unsichtbar.
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


if __name__ == "__main__":
    unittest.main()
