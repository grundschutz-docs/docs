"""Unter "Was ich nicht geprueft habe" steht nur, was nicht geprueft wurde.

Das erste Bullet dort sagte, die 39 Zielobjektkategorien seien geprueft (alle kommen vor, stimmen
mit der CSV des BSI ueberein): eine Pruef-Aussage unter der Ueberschrift "nicht geprueft", auf
Deutsch und auf Englisch. Die Aussage bleibt, steht jetzt im Abschnitt zu den Kategorien. Sie
bleibt in der Datei, weil check_handwritten_numbers() sie gegen den Katalog prueft.
"""
import re
import unittest
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent.parent / "src" / "content" / "docs"
FAELLE = [
    ("methodik.mdx", "## Was ich nicht geprüft habe", "alle 39 Kategorien kommen vor"),
    ("en/methodik.mdx", "## What I have not checked", "all 39 categories occur"),
]


class NichtGeprueft(unittest.TestCase):
    def test_keine_pruefaussage_unter_nicht_geprueft(self):
        for datei, ueberschrift, aussage in FAELLE:
            with self.subTest(datei=datei):
                text = (DOCS / datei).read_text(encoding="utf-8")
                self.assertIn(ueberschrift, text)
                self.assertIn(aussage, text, "die Aussage darf nicht verloren gehen")
                abschnitt = re.split(r"^## ", text.split(ueberschrift, 1)[1], maxsplit=1, flags=re.M)[0]
                self.assertNotIn(aussage, abschnitt)


if __name__ == "__main__":
    unittest.main()
