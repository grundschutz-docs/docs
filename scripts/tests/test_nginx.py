"""Startet ein echtes nginx mit docker/nginx.conf und prueft, was ausgeliefert wird.

Gebraucht wird ein nginx im PATH und seine mime.types (Standard /etc/nginx/mime.types,
sonst NGINX_MIME_TYPES). Fehlt nginx, schlaegt der Test fehl, statt still zu bestehen.

Nur die Zeilen `listen` und `root` der Konfiguration werden fuer den Test ersetzt.
"""
import gzip
import http.client
import os
import re
import shutil
import socket
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MIME_TYPES = os.environ.get("NGINX_MIME_TYPES", "/etc/nginx/mime.types")


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class NginxAuslieferung(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which("nginx"):
            raise RuntimeError("nginx nicht gefunden: ohne nginx laesst sich die Konfiguration nicht pruefen")
        cls.tmp = Path(tempfile.mkdtemp())
        cls.tmp.chmod(0o755)  # die nginx-Worker laufen unter einem anderen Benutzer
        site = cls.tmp / "html"
        (site / "downloads").mkdir(parents=True)
        (site / "index.html").write_text("<!doctype html><title>x</title>" + "x" * 2000)
        csv_quelle = next((ROOT / "public" / "downloads").glob("*.csv"))
        shutil.copy(csv_quelle, site / "downloads" / "anforderungen.csv")
        json_quelle = next((ROOT / "public" / "downloads").glob("*.json"))
        shutil.copy(json_quelle, site / "downloads" / "anforderungen.json")
        (site / "bild.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg">' + "<g/>" * 500 + "</svg>")

        cls.port = free_port()
        conf = (ROOT / "docker" / "nginx.conf").read_text()
        conf = re.sub(r"listen\s+80;", f"listen 127.0.0.1:{cls.port};", conf)
        conf = re.sub(r"root\s+/usr/share/nginx/html;", f"root {site};", conf)
        (cls.tmp / "site.conf").write_text(conf)
        (cls.tmp / "nginx.conf").write_text(
            f"pid {cls.tmp}/nginx.pid;\nerror_log {cls.tmp}/error.log warn;\nevents {{}}\n"
            f"http {{\n include {MIME_TYPES};\n default_type application/octet-stream;\n access_log off;\n"
            f" client_body_temp_path {cls.tmp}/b; proxy_temp_path {cls.tmp}/p; fastcgi_temp_path {cls.tmp}/f;\n"
            f" uwsgi_temp_path {cls.tmp}/u; scgi_temp_path {cls.tmp}/s;\n"
            f" include {cls.tmp}/site.conf;\n}}\n"
        )
        cls.test = subprocess.run(
            ["nginx", "-t", "-p", str(cls.tmp), "-c", str(cls.tmp / "nginx.conf")],
            capture_output=True,
            text=True,
        )
        cls.proc = subprocess.Popen(
            ["nginx", "-p", str(cls.tmp), "-c", str(cls.tmp / "nginx.conf"), "-g", "daemon off;"],
            stderr=subprocess.DEVNULL,
        )
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", cls.port), timeout=0.2).close()
                break
            except OSError:
                time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.proc.wait(timeout=10)
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def get(self, path):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("GET", path, headers={"Accept-Encoding": "gzip"})
        res = conn.getresponse()
        body = res.read()
        headers = {k.lower(): v for k, v in res.getheaders()}
        conn.close()
        return res.status, headers, body

    def test_konfiguration_ohne_warnung(self):
        self.assertEqual(self.test.returncode, 0, self.test.stderr)
        self.assertNotIn("duplicate MIME type", self.test.stderr)

    def test_csv_wird_als_csv_ausgeliefert_und_komprimiert(self):
        status, headers, body = self.get("/downloads/anforderungen.csv")
        self.assertEqual(status, 200)
        self.assertTrue(headers["content-type"].startswith("text/csv"), headers["content-type"])
        self.assertEqual(headers.get("content-encoding"), "gzip")
        gzip.decompress(body)  # ist wirklich gzip

    def test_json_behaelt_seinen_typ(self):
        # Absicherung gegen eine zu breite CSV-Regel: andere Downloads bleiben, was sie sind.
        status, headers, _ = self.get("/downloads/anforderungen.json")
        self.assertEqual(status, 200)
        self.assertTrue(headers["content-type"].startswith("application/json"), headers["content-type"])

    def test_svg_wird_komprimiert(self):
        status, headers, _ = self.get("/bild.svg")
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("content-encoding"), "gzip")

    def test_html_bleibt_komprimiert(self):
        # text/html komprimiert nginx immer, auch ohne Eintrag in gzip_types.
        status, headers, _ = self.get("/")
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("content-encoding"), "gzip")


if __name__ == "__main__":
    unittest.main()
