"""Der Feed des Änderungsprotokolls (/aenderungen/feed.xml) ist gültig und stimmt mit den Daten überein.

Der Feed wird von src/lib/feed.ts geschrieben, ohne Paket. Der klassische Fehler bei selbst
gebauten Feeds ist ein "&" oder "<" im Text, das nicht maskiert ist: ein Reader lehnt dann den
ganzen Feed ab. In den echten Daten kommt das nicht vor (der Feed enthält nur IDs, Zählungen und
Feldnamen), deshalb prüft der zweite Teil den Generator mit absichtlich schwierigen Daten.

Der erste Teil liest den fertigen dist/-Ordner und vergleicht ihn mit src/data/changelog.json.
Vor dem Lauf: pnpm run build.
"""
import json
import subprocess
import unittest
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DIST = ROOT / "dist"
ATOM = "{http://www.w3.org/2005/Atom}"
QUELLE = "Quelle: BSI Stand-der-Technik-Bibliothek (CC BY-SA 4.0)"


def lade_eintraege():
    return json.loads((ROOT / "src" / "data" / "changelog.json").read_text())["eintraege"]


def mit_aenderungen(e):
    return len(e["neu"]) + len(e["entfernt"]) + len(e["aenderungen"]) > 0


def feed_aus_generator(eintraege):
    """Ruft changelogFeed() aus src/lib/feed.ts mit beliebigen Daten auf (Node strippt die Typen)."""
    skript = (
        "import('./src/lib/feed.ts').then(m => process.stdout.write("
        "m.changelogFeed(JSON.parse(process.argv[1]), 'https://beispiel.test/')))"
    )
    return subprocess.run(
        ["node", "-e", skript, json.dumps(eintraege)], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


class FeedImBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        datei = DIST / "aenderungen" / "feed.xml"
        if not datei.exists():
            raise RuntimeError("dist/aenderungen/feed.xml fehlt: erst pnpm run build")
        cls.text = datei.read_text()
        cls.channel = ET.fromstring(cls.text).find("channel")
        cls.items = cls.channel.findall("item")
        cls.eintraege = sorted(
            [e for e in lade_eintraege() if mit_aenderungen(e)], key=lambda e: e["veroeffentlicht"], reverse=True
        )

    def test_ein_eintrag_je_stand_mit_aenderungen(self):
        self.assertEqual([i.findtext("guid") for i in self.items], ["bsi-commit-" + e["commit"] for e in self.eintraege])

    def test_staende_ohne_aenderung_fehlen(self):
        leer = [e["commit"] for e in lade_eintraege() if not mit_aenderungen(e)]
        self.assertTrue(leer, "Die Daten haben keinen Stand ohne Änderung mehr: Test prüft nichts")
        for commit in leer:
            self.assertNotIn(commit[:7], self.text)

    def test_ids_sind_eindeutig_und_keine_links(self):
        guids = [i.findtext("guid") for i in self.items]
        self.assertEqual(len(guids), len(set(guids)))
        for i in self.items:
            self.assertEqual(i.find("guid").get("isPermaLink"), "false")

    def test_links_zeigen_auf_vorhandene_anker(self):
        seite = (DIST / "aenderungen" / "index.html").read_text()
        for i, e in zip(self.items, self.eintraege):
            anker = "stand-" + e["commit"][:7]
            self.assertTrue(i.findtext("link").endswith("/aenderungen/#" + anker), i.findtext("link"))
            self.assertIn(f'id="{anker}"', seite)

    def test_datum_ist_das_des_bsi_nicht_die_build_zeit(self):
        for i, e in zip(self.items, self.eintraege):
            soll = datetime.fromisoformat(e["veroeffentlicht"].replace("Z", "+00:00"))
            self.assertEqual(parsedate_to_datetime(i.findtext("pubDate")), soll)
        self.assertEqual(self.channel.findtext("lastBuildDate"), self.items[0].findtext("pubDate"))

    def test_zahl_im_titel_ist_die_zahl_der_aenderungen(self):
        for i, e in zip(self.items, self.eintraege):
            self.assertIn(f"{len(e['aenderungen'])} geänderte Anforderung", i.findtext("title"))

    def test_kein_wortlaut_des_bsi_im_feed(self):
        # Nur IDs, Feldnamen und Zählungen: der alte und neue Text der Änderungen steht nicht drin.
        for e in self.eintraege:
            for a in e["aenderungen"]:
                for f in a["felder"]:
                    for text in (f.get("alt", ""), f.get("neu", "")):
                        if len(text) >= 30:
                            self.assertNotIn(text[:30], self.text)

    def test_quelle_steht_in_jedem_eintrag_und_im_kanal(self):
        self.assertIn(QUELLE, self.channel.findtext("description"))
        for i in self.items:
            self.assertIn(QUELLE, i.findtext("description"))

    def test_selbstverweis_und_sprache(self):
        self.assertEqual(self.channel.find(ATOM + "link").get("rel"), "self")
        self.assertTrue(self.channel.find(ATOM + "link").get("href").endswith("/aenderungen/feed.xml"))
        self.assertEqual(self.channel.findtext("language"), "de")

    def test_startseite_verweist_auf_den_feed(self):
        for seite in ("index.html", "en/index.html"):
            html = (DIST / seite).read_text()
            self.assertIn('rel="alternate" type="application/rss+xml"', html, seite)
            self.assertIn("/aenderungen/feed.xml", html, seite)


class GeneratorMitSchwierigenDaten(unittest.TestCase):
    """Ein Feed, der bei Sonderzeichen ungültig wird, wird von Readern komplett abgelehnt."""

    SCHWIERIG = [
        {
            "commit": "abcdef1234567890" * 2 + "abcdefgh",
            "veroeffentlicht": "2026-11-05T08:00:00Z",
            "neu": [{}],
            "entfernt": [{}, {}],
            "aenderungen": [
                {"id": "A&B.1 <x>", "felder": [{"name": 'Ergebnis & "Zusatz" <neu>'}, {"name": "Steuer\x01zeichen\x0b"}]},
            ],
        },
    ]

    def test_sonderzeichen_ergeben_gueltiges_xml(self):
        wurzel = ET.fromstring(feed_aus_generator(self.SCHWIERIG))
        beschreibung = wurzel.find("channel/item/description").text
        self.assertIn("A&B.1 <x>", beschreibung)
        self.assertIn('Ergebnis & "Zusatz" <neu>', beschreibung)
        self.assertNotIn("\x01", beschreibung)

    def test_neu_und_entfernt_stehen_im_titel(self):
        titel = ET.fromstring(feed_aus_generator(self.SCHWIERIG)).findtext("channel/item/title")
        self.assertIn("1 geänderte Anforderung", titel)
        self.assertIn("1 neue Anforderung", titel)
        self.assertIn("2 entfernte Anforderungen", titel)

    def test_mehr_als_zwoelf_ids_werden_gekuerzt(self):
        e = dict(self.SCHWIERIG[0])
        e["aenderungen"] = [{"id": f"X.{n}", "felder": [{"name": "Titel"}]} for n in range(20)]
        beschreibung = ET.fromstring(feed_aus_generator([e])).findtext("channel/item/description")
        self.assertIn("X.11", beschreibung)
        self.assertNotIn("X.12,", beschreibung)
        self.assertIn("und 8 weitere", beschreibung)

    def test_ohne_staende_bleibt_der_feed_gueltig(self):
        wurzel = ET.fromstring(feed_aus_generator([]))
        self.assertEqual(wurzel.findall("channel/item"), [])


if __name__ == "__main__":
    unittest.main()
