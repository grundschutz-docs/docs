"""build-sample.mjs und compare.py (scripts/xlsx/) koennen alle Filter der Exportseite.

Beide Skripte bauen und pruefen die Excel-Mappe fuer eine Auswahl: die Mappe entsteht in JavaScript,
compare.py liest sie mit exceljs und vergleicht jede Zelle mit der CSV des Generators. Bisher
kannten sie nur praktik und pflicht; bei stufe, aufwand, ziel und ohne bildete compare.py die
falsche Auswahl und meldete Abweichungen, die keine sind (oder build-sample ignorierte den Filter).

Gebraucht werden node und exceljs (XLSX_ORACLE_DIR, siehe Kopf von scripts/xlsx/verify.py).
Fehlt etwas, schlaegt der Test fehl, statt still zu bestehen.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GESAMT = 1000

# (Name, Filter, erwartet weniger als alle Zeilen)
FAELLE = [
    ("praktik und pflicht (bisher schon)", ["praktik=GC,STM", "pflicht=MUSS"]),
    ("stufe", ["stufe=Standard-Sicherheitsstufe"]),
    ("aufwand", ["aufwand=1,2"]),
    ("ziel mit Vererbung", ["ziel=Webserver"]),
    ("ziel ohne die Anforderungen ohne Kategorie", ["ziel=Webserver", "ohne=nein"]),
    ("alle Filter zusammen", ["praktik=BER,KONF", "stufe=Standard-Sicherheitsstufe", "aufwand=2,3", "ziel=Webserver", "ohne=nein"]),
]


class XlsxFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which("node"):
            raise RuntimeError("node nicht gefunden")
        cls.oracle = os.environ.get("XLSX_ORACLE_DIR")
        if not cls.oracle or not (Path(cls.oracle) / "node_modules" / "exceljs").exists():
            raise RuntimeError("XLSX_ORACLE_DIR fehlt oder enthaelt kein exceljs (npm install exceljs@4.4.0)")
        cls.tmp = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_mappe_und_csv_stimmen_fuer_jeden_filter(self):
        env = {**os.environ, "XLSX_ORACLE_DIR": self.oracle}
        for name, filter_ in FAELLE:
            with self.subTest(name):
                datei = str(Path(self.tmp.name) / (re.sub(r"\W+", "_", name) + ".xlsx"))
                bau = subprocess.run(["node", "scripts/xlsx/build-sample.mjs", datei, *filter_], cwd=ROOT, env=env, capture_output=True, text=True)
                self.assertEqual(bau.returncode, 0, bau.stderr[-300:])
                zeilen = int(re.search(r": (\d+) Anforderungen", bau.stdout).group(1))
                self.assertTrue(0 < zeilen < GESAMT, f"der Filter {filter_} wirkt nicht: {zeilen} von {GESAMT} Zeilen")
                vergleich = subprocess.run([sys.executable, "-B", "scripts/xlsx/compare.py", datei, *filter_], cwd=ROOT, env=env, capture_output=True, text=True)
                self.assertEqual(vergleich.returncode, 0, "\n".join(vergleich.stdout.splitlines()[-8:]))


if __name__ == "__main__":
    unittest.main()
