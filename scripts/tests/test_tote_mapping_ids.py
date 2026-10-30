"""Vergleichsseiten: Ziel-IDs des BSI-Mappings, die im Katalog nicht stehen, sind gekennzeichnet.

Die Mapping-Datei des BSI (Entwurf, Stand 21.07.2026) nennt Ziel-IDs, die der Katalog nicht hat. Der
Generator schrieb sie stillschweigend als reinen Text ohne Link und ohne Titel, obwohl die Uebersicht
"mit Link direkt dorthin" verspricht. Jetzt steht dabei, dass die ID nicht im Katalog steht, mit Link auf
den Befund.

Verglichen werden zwei unabhaengige Quellen: die geschriebenen Seiten und eine Nachrechnung aus
Mapping-Datei und Katalog.
"""
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
VERGLEICH = ROOT / "src" / "content" / "docs" / "vergleich"
BADGE = "nicht im aktuellen Katalog"
SPAN = re.compile(r'<span class="new-id">([^<]+)</span>(.{0,260})', re.S)


def katalog_ids(knoten):
    for c in knoten.get("controls", []):
        yield c["id"]
        yield from katalog_ids(c)
    for g in knoten.get("groups", []):
        yield from katalog_ids(g)


class ToteMappingIds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.environ.get("GRUNDSCHUTZPP_CATALOG"):
            raise RuntimeError("GRUNDSCHUTZPP_CATALOG nicht gesetzt")
        ids = set(katalog_ids(json.loads(Path(os.environ["GRUNDSCHUTZPP_CATALOG"]).read_text())["catalog"]))
        mapping = json.loads(Path(os.environ["GRUNDSCHUTZPP_MAPPING"]).read_text())
        ziele = set()
        for gruppe in mapping["mapping-collection"]["mappings"]:
            for m in gruppe.get("maps", []):
                quelle, ziel = m.get("sources") or [{}], m.get("targets") or [{}]
                if m.get("relationship") and quelle[0].get("id-ref") and ziel[0].get("id-ref"):
                    ziele.add(ziel[0]["id-ref"])
        cls.erwartet = ziele - ids
        cls.vorkommen = []  # (Seite, ID, Text danach)
        for seite in sorted(VERGLEICH.glob("*.mdx")):
            for m in SPAN.finditer(seite.read_text(encoding="utf-8")):
                cls.vorkommen.append((seite.name, m.group(1), m.group(2)))

    def test_es_gibt_tote_ids_und_sie_stehen_auf_den_seiten(self):
        # Gegenprobe: ohne tote IDs im Mapping bewiese der Test nichts.
        self.assertGreater(len(self.erwartet), 5)
        self.assertEqual({v[1] for v in self.vorkommen}, self.erwartet)

    def test_jede_tote_id_ist_gekennzeichnet(self):
        ohne = [f"{s}: {i}" for s, i, danach in self.vorkommen if BADGE not in danach]
        self.assertEqual(ohne[:5], [], f"{len(ohne)} von {len(self.vorkommen)} ohne Kennzeichnung")

    def test_kennzeichnung_verweist_auf_den_befund(self):
        falsch = [f"{s}: {i}" for s, i, danach in self.vorkommen if "/befunde/mapping-datei-ist-entwurf/" not in danach]
        self.assertEqual(falsch[:5], [])


if __name__ == "__main__":
    unittest.main()
