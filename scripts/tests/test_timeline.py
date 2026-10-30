"""Der Banner zeigt an jedem Tag eine echte Phase, nicht den Auffang-Eintrag "Übergangszeit".

TIMELINE (scripts/generate_docs.py) hat einen offenen Eintrag "Übergangszeit" (kein Ende), der
nur dazu da ist, dass der Banner nie leer ist. Fehlt für einen Zeitraum eine eigene Phase, springt
der Banner auf diesen Eintrag und sagt "Grundschutz++ ist in der Übergangszeit": für den BSI die
mehrjährige Weiternutzung des alten IT-Grundschutzes, keine Projektphase von Grundschutz++.
Das passierte nach dem Ende der it-sa-Phase (29.10.2026) bis zum 31.12.2026: zwei Monate, in denen
jeder Lauf des Generators ein anderes status.json schrieb als im Repository stand, und
generated.yml rot wurde.

Der Test geht jeden Tag von Projektbeginn bis Ende 2027 durch. Danach ist "Übergangszeit" gewollt.
"""
import importlib.util
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
AUFFANG = "Übergangszeit"
ERSTER_TAG, LETZTER_TAG = date(2026, 4, 1), date(2027, 12, 31)


def lade_generator():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("generate_docs", ROOT / "scripts" / "generate_docs.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


class BannerPhase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = lade_generator()

    def test_jeder_tag_hat_eine_echte_phase(self):
        luecken, tag = [], ERSTER_TAG
        while tag <= LETZTER_TAG:
            phase = self.g.banner_phase(tag)
            if phase is None or phase[2] == AUFFANG:
                luecken.append(tag)
            tag += timedelta(days=1)
        # Gegenprobe: die Auswahl funktioniert, sie liefert fuer die meisten Tage eine Phase
        self.assertLess(len(luecken), (LETZTER_TAG - ERSTER_TAG).days)
        beschreibung = f"{luecken[0]} bis {luecken[-1]} ({len(luecken)} Tage)" if luecken else ""
        self.assertEqual(luecken, [], f"Banner springt auf '{AUFFANG}' oder bleibt leer: {beschreibung}")

    def test_nach_2027_bleibt_der_auffang_eintrag(self):
        # Die Gegenseite: ab 2028 ist der Auffang-Eintrag gewollt, und er traegt weiter ein "Ende nicht festgelegt".
        phase = self.g.banner_phase(date(2028, 6, 1))
        self.assertIsNotNone(phase)
        self.assertEqual(phase[2], AUFFANG)

    def test_meilenstein_ohne_datum_steht_in_der_zeitleiste_aber_nie_im_banner(self):
        # Der BSI-Meilensteinplan nennt "2027 ff.: Internationalisierung des GS++, Integration anderer
        # Managementsysteme" ohne Datum. Er steht mit der Angabe des BSI in der Zeitleiste und ist nie eine
        # Banner-Phase: das BSI nennt weder Beginn noch Ende.
        eintraege = [e for e in self.g.TIMELINE if "Internationalisierung" in e[2]]
        self.assertEqual(len(eintraege), 1)
        eintrag = eintraege[0]
        self.assertEqual(eintrag[6], "2027 ff.")
        self.assertFalse(eintrag[7], "kein Banner-Eintrag")
        tag = ERSTER_TAG
        while tag <= date(2031, 12, 31):
            self.assertIsNot(self.g.banner_phase(tag), eintrag)
            tag += timedelta(days=30)


if __name__ == "__main__":
    unittest.main()
