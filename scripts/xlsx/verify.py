#!/usr/bin/env python3
"""Prüft eine mit src/lib/xlsx erzeugte xlsx-Datei auf vier voneinander unabhängigen Wegen.

Hintergrund: Excel meldet bei einem Fehler in der XML-Struktur nur "Datei
reparieren", ohne zu sagen, was falsch ist, und wir können hier nicht jedes Mal
Excel öffnen. Diese Prüfung fängt die typischen Ursachen vorher ab:

  1. Schema:   jede XML-Datei gegen das ECMA-376-Schema (sml.xsd), mit xmllint.
               Findet vor allem falsche Reihenfolgen von Elementen.
  2. Paket:    zeigt jeder Verweis auf eine Datei, die es gibt, und ist jede Datei
               in [Content_Types].xml eingetragen.
  3. exceljs:  ein fremder Leser (scripts/xlsx/oracle-read.mjs) liest die Datei,
               und seine Sicht muss mit dem übereinstimmen, was hier direkt aus dem
               XML gelesen wird.
  4. LibreOffice: öffnet die Datei und schreibt sie als .fods (flaches XML) wieder
               aus. Darin müssen Blätter, Filter, Dropdowns und fixierte Zeilen stehen.

Die Prüfung ersetzt nicht den Test in Excel selbst. Sie macht eine Reparatur-
Meldung dort unwahrscheinlicher, schließt sie aber nicht aus.

Aufruf:
  OOXML_XSD_DIR=/pfad/zu/xsd XLSX_ORACLE_DIR=/pfad/zu/exceljs python3 verify.py datei.xlsx

  OOXML_XSD_DIR     Verzeichnis mit sml.xsd (ECMA-376 Teil 4, "Transitional":
                    https://ecma-international.org/wp-content/uploads/ECMA-376-4_5th_edition_december_2016.zip,
                    darin OfficeOpenXML-XMLSchema-Transitional.zip)
  XLSX_ORACLE_DIR   Verzeichnis, in dem `pnpm add exceljs@4.4.0` gelaufen ist (optional)
  SOFFICE           Pfad zu soffice (Standard: soffice im PATH; optional)
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import unescape

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
}
failures = []
notes = []


def check(ok, text):
    print(("  ok   " if ok else "  FEHLER ") + text)
    if not ok:
        failures.append(text)


def skip(text):
    print("  übersprungen: " + text)
    notes.append(text)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main(path):
    path = Path(path)
    work = Path(tempfile.mkdtemp(prefix="xlsx-verify-"))
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            z.extractall(work / "x")
        root = work / "x"
        print(f"{path.name}: {len(names)} Teile, {path.stat().st_size} Bytes")

        print("\n0. Zip-Aufbau")
        check(names[0] == "[Content_Types].xml", "[Content_Types].xml steht als erste Datei im ZIP")
        check(len(names) == len(set(names)), "keine doppelten Dateinamen")

        # --- 1. Schema ---------------------------------------------------------
        print("\n1. Schema (ECMA-376 sml.xsd, xmllint)")
        xsd_dir = os.environ.get("OOXML_XSD_DIR")
        xml_parts = [n for n in names if n.endswith((".xml", ".rels"))]
        for n in xml_parts:
            r = run(["xmllint", "--noout", str(root / n)])
            check(r.returncode == 0, f"wohlgeformt: {n}")
        if not xsd_dir or not (Path(xsd_dir) / "sml.xsd").exists():
            skip("Schema-Prüfung (OOXML_XSD_DIR zeigt nicht auf ein Verzeichnis mit sml.xsd)")
        else:
            schema = str(Path(xsd_dir) / "sml.xsd")
            for n in names:
                if n in ("xl/workbook.xml", "xl/styles.xml", "xl/sharedStrings.xml") or re.match(r"xl/worksheets/sheet\d+\.xml$", n):
                    target = root / n
                    if n == "xl/sharedStrings.xml":
                        # Bekannte Lücke: sml.xsd kennt xml:space an <t> nicht, obwohl der
                        # Standard es vorsieht und Excel es selbst schreibt. Nur dieses
                        # eine Attribut wird vor der Prüfung entfernt, alles andere bleibt.
                        text = target.read_text(encoding="utf-8").replace(' xml:space="preserve"', "")
                        target = work / "sharedStrings-ohne-xml-space.xml"
                        target.write_text(text, encoding="utf-8")
                    r = run(["xmllint", "--noout", "--schema", schema, str(target)])
                    check(r.returncode == 0, f"gültig nach Schema: {n}" + ("" if r.returncode == 0 else "\n      " + r.stderr.strip().splitlines()[0][:200]))

        # --- 2. Paket ----------------------------------------------------------
        print("\n2. Paket-Konsistenz")
        ct = ET.parse(root / "[Content_Types].xml").getroot()
        defaults = {d.get("Extension") for d in ct.findall("ct:Default", NS)}
        overrides = {o.get("PartName").lstrip("/") for o in ct.findall("ct:Override", NS)}
        for n in names:
            if n == "[Content_Types].xml":
                continue
            ext = n.rsplit(".", 1)[-1]
            check(n in overrides or ext in defaults, f"Inhaltstyp bekannt: {n}")
        for o in overrides:
            check(o in names, f"Override zeigt auf vorhandene Datei: {o}")
        external = []
        for rels in [n for n in names if n.endswith(".rels")]:
            base = Path(rels).parent.parent  # _rels/.rels -> ., xl/_rels/x.rels -> xl
            for rel in ET.parse(root / rels).getroot().findall("pr:Relationship", NS):
                if rel.get("TargetMode") == "External":
                    external.append(rel.get("Target", ""))
                    continue
                target = (base / rel.get("Target")).as_posix()
                target = os.path.normpath(target).replace("\\", "/")
                check(target in names, f"{rels}: {rel.get('Id')} -> {target}")

        bad = [t for t in external if not re.match(r"https?://[^\s]+$", t)]
        check(not bad, f"alle {len(external)} externen Ziele sind http(s)-Adressen" + (f" (erstes falsches: {bad[0][:60]})" if bad else ""))

        # --- Eigene Sicht auf die Blätter (direkt aus dem XML) ------------------
        wb = ET.parse(root / "xl/workbook.xml").getroot()
        sheet_names = [s.get("name") for s in wb.find("m:sheets", NS)]
        mine = []
        for i, name in enumerate(sheet_names, 1):
            sx = ET.parse(root / f"xl/worksheets/sheet{i}.xml").getroot()
            rows = sx.find("m:sheetData", NS).findall("m:row", NS)
            pane = sx.find("m:sheetViews/m:sheetView/m:pane", NS)
            af = sx.find("m:autoFilter", NS)
            dvs = [(d.get("sqref"), d.findtext("m:formula1", namespaces=NS)) for d in sx.findall("m:dataValidations/m:dataValidation", NS)]
            mine.append(
                {
                    "name": name,
                    "lastRow": len(rows),
                    "autoFilter": af.get("ref") if af is not None else None,
                    "frozen": {"x": int(pane.get("xSplit", 0)), "y": int(pane.get("ySplit", 0))} if pane is not None and pane.get("state") == "frozen" else None,
                    "validations": dvs,
                    "hyperlinks": len(sx.findall("m:hyperlinks/m:hyperlink", NS)),
                }
            )

        # --- 3. exceljs ----------------------------------------------------------
        print("\n3. Gegenprobe mit exceljs (fremder Leser)")
        oracle_dir = os.environ.get("XLSX_ORACLE_DIR")
        if not oracle_dir:
            skip("exceljs-Gegenprobe (XLSX_ORACLE_DIR nicht gesetzt)")
        else:
            r = run(["node", str(Path(__file__).with_name("oracle-read.mjs")), str(path)], env={**os.environ, "XLSX_ORACLE_DIR": oracle_dir})
            if r.returncode != 0:
                check(False, "exceljs konnte die Datei nicht lesen: " + r.stderr.strip()[:200])
            else:
                theirs = json.loads(r.stdout)["sheets"]
                check([s["name"] for s in theirs] == sheet_names, f"Blattnamen gleich: {sheet_names}")
                for a, b in zip(mine, theirs):
                    check(b["lastRow"] == a["lastRow"], f"[{a['name']}] Zeilenzahl: exceljs {b['lastRow']}, XML {a['lastRow']}")
                    check(b["hyperlinks"] == a["hyperlinks"], f"[{a['name']}] Hyperlinks: exceljs {b['hyperlinks']}, XML {a['hyperlinks']}")
                    check((b["frozen"] or None) == (a["frozen"] or None), f"[{a['name']}] fixierte Zeilen/Spalten: exceljs {b['frozen']}, XML {a['frozen']}")
                    check(bool(b["autoFilter"]) == bool(a["autoFilter"]), f"[{a['name']}] Autofilter: exceljs {bool(b['autoFilter'])}, XML {bool(a['autoFilter'])}")
                    check(len(b["validations"]) > 0 if a["validations"] else len(b["validations"]) == 0, f"[{a['name']}] Dropdowns vorhanden: exceljs {len(b['validations'])} Zellen, XML {len(a['validations'])} Regeln")

        # --- 4. LibreOffice ------------------------------------------------------
        print("\n4. Gegenprobe mit LibreOffice (öffnen und als flaches XML ausschreiben)")
        soffice = os.environ.get("SOFFICE") or shutil.which("soffice")
        if not soffice:
            skip("LibreOffice nicht gefunden")
        else:
            out = work / "lo"
            out.mkdir()
            r = run([soffice, f"-env:UserInstallation=file://{work}/profile", "--headless", "--convert-to", "fods", "--outdir", str(out), str(path)], timeout=180)
            fods = out / (path.stem + ".fods")
            check(fods.exists(), "LibreOffice öffnet die Datei und schreibt sie wieder aus" + ("" if fods.exists() else f" ({r.stderr.strip()[:150]})"))
            if fods.exists():
                lo = fods.read_text(encoding="utf-8")
                # Im XML steht "&" als "&amp;": vor dem Vergleich zurückübersetzen.
                tables = [unescape(t, {"&quot;": '"', "&apos;": "'"}) for t in re.findall(r'<table:table table:name="([^"]*)"', lo)]
                check(tables == sheet_names, f"Blattnamen in LibreOffice: {tables}")
                n_valid = len(re.findall(r"<table:content-validation ", lo))
                want_valid = sum(len(m["validations"]) for m in mine)
                check(n_valid >= want_valid, f"Dropdown-Regeln erkannt: LibreOffice {n_valid}, XML {want_valid}")
                n_af = len(re.findall(r'table:display-filter-buttons="true"', lo))
                want_af = sum(1 for m in mine if m["autoFilter"])
                check(n_af >= want_af, f"Autofilter erkannt: LibreOffice {n_af}, XML {want_af}")
                n_links = len(re.findall(r"<text:a xlink:href=", lo))
                want_links = sum(m["hyperlinks"] for m in mine)
                check(n_links == want_links, f"Hyperlinks: LibreOffice {n_links}, XML {want_links}")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print()
    if failures:
        print(f"{len(failures)} Prüfung(en) fehlgeschlagen.")
        sys.exit(1)
    print("Alle Prüfungen bestanden." + (f" ({len(notes)} übersprungen)" if notes else ""))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
