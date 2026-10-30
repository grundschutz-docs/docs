#!/usr/bin/env python3
"""Vergleicht jede Zelle der Excel-Mappe mit den Dateien, die der Python-Generator schreibt.

Die Mappe entsteht in JavaScript (src/lib/xlsx/export-workbook.js), die CSV in Python
(scripts/generate_docs.py), beide aus denselben Daten. Stimmen sie Zelle für Zelle
überein, ist der JavaScript-Teil sehr wahrscheinlich richtig; ein Fehler müsste in
beiden Sprachen gleich gemacht worden sein. Gelesen wird die Mappe mit exceljs, einem
fremden Leser (XLSX_ORACLE_DIR).

  XLSX_ORACLE_DIR=/pfad python3 compare.py mappe.xlsx [praktik=GC,STM] [pflicht=MUSS] [stufe=...] [aufwand=1,2] [ziel=Webserver] [ohne=nein]

Die Filter müssen dieselben sein wie bei build-sample.mjs.
"""
import csv
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DL = ROOT / "public" / "downloads"
failures = []


def check(ok, text):
    print(("  ok   " if ok else "  FEHLER ") + text)
    if not ok:
        failures.append(text)


def main(xlsx, filters):
    f = {k: v.split(",") for k, v in (s.split("=") for s in filters)}
    out = subprocess.run(["node", str(Path(__file__).with_name("oracle-dump.mjs")), xlsx], capture_output=True, text=True, env={**os.environ})
    if out.returncode != 0:
        sys.exit("exceljs konnte die Datei nicht lesen: " + out.stderr[:300])
    sheets = {s["name"]: s["rows"] for s in json.loads(out.stdout)}

    with (DL / "grundschutzpp-anforderungen.csv").open(newline="", encoding="utf-8-sig") as fh:
        table = list(csv.reader(fh, delimiter=";"))
    chead, cbody = table[0], table[1:]
    col = {n: i for i, n in enumerate(chead)}
    # Auswahl wie auf der Exportseite (ExportTabelle.astro) und in build-sample.mjs.
    ohne_kategorie = "Ohne Zielobjektkategorie"

    def passt(r):
        if f.get("praktik") and r[col["Praktik"]].split(" ")[0] not in f["praktik"]:
            return False
        if f.get("pflicht") and r[col["Pflichtgrad"]] not in f["pflicht"]:
            return False
        if f.get("stufe") and r[col["Sicherheitsstufe"]] not in f["stufe"]:
            return False
        if f.get("aufwand") and r[col["Aufwand"]] not in f["aufwand"]:
            return False
        if f.get("ziel"):
            direkt = [x for x in r[col["Zielobjektkategorien"]].split("; ") if x]
            darunter = [x for x in r[col["Gilt auch für Unterkategorien"]].split("; ") if x]
            ohne = direkt == [ohne_kategorie]
            mit_ohne = f.get("ohne", [""])[0] != "nein"
            if not (any(t in f["ziel"] for t in direkt + darunter) or (ohne and mit_ohne)):
                return False
        return True

    cbody = [r for r in cbody if passt(r)]
    payload = json.loads((DL / "grundschutzpp-anforderungen.json").read_text(encoding="utf-8"))

    # --- Blatt Anforderungen gegen die CSV ------------------------------------------
    print("Blatt \"Anforderungen\" gegen die CSV des Generators")
    rows = sheets["Anforderungen"]
    xhead, xbody = rows[0], rows[1:]
    check(sorted(xhead) == sorted(chead), f"dieselben {len(chead)} Spalten wie die CSV (Reihenfolge darf abweichen)")
    check(len(xbody) == len(cbody), f"{len(xbody)} Zeilen in der Mappe, {len(cbody)} in der CSV")
    xi = {n: i for i, n in enumerate(xhead)}
    check([r[xi["ID"]] for r in xbody] == [r[col["ID"]] for r in cbody], "dieselben IDs in derselben Reihenfolge")
    diffs = []
    for xr, cr in zip(xbody, cbody):
        for name in chead:
            x = xr[xi[name]] if xi[name] < len(xr) else None
            c = cr[col[name]]
            if name == "Aufwand":
                ok = x == int(c)
            elif name == "Seite":
                ok = isinstance(x, dict) and x["hyperlink"] == c
            else:
                ok = (x is None and c == "") or x == c
            if not ok:
                diffs.append((cr[col["ID"]], name, x, c))
    check(not diffs, f"alle {len(xbody) * len(chead)} Zellen stimmen mit der CSV überein" + (f"; erste Abweichung: {diffs[0]}" if diffs else ""))
    arbeit = payload["arbeitsspalten"]
    check(all(xr[xi[n]] is None for xr in xbody for n in arbeit if xi[n] < len(xr)), f"Arbeitsspalten {arbeit} sind leer")

    # --- Blatt Dokumente: aus der CSV nachgezählt --------------------------------------
    print("\nBlatt \"Dokumente\" gegen eine Nachzählung aus der CSV")
    drows = sheets["Dokumente"]
    dhead, dbody = drows[0], drows[1:]
    di = {n: i for i, n in enumerate(dhead)}
    erwartet = {}
    for r in cbody:
        name = r[col["Dokumentiert in"]]
        if name:
            e = erwartet.setdefault(name, {"anzahl": 0, "muss": 0, "praktiken": set()})
            e["anzahl"] += 1
            e["muss"] += r[col["Pflichtgrad"]] == "MUSS"
            e["praktiken"].add(r[col["Praktik"]].split(" ")[0])
    order = [p["id"] for p in payload["praktiken"]]
    namen = [r[di["Dokument"]] for r in dbody]
    check(sorted(namen) == sorted(erwartet), f"{len(namen)} Dokumenttypen, dieselben wie in der CSV, keiner doppelt")
    # Bei gleicher Anzahl sortiert die Mappe deutsch (localeCompare), Python nach Zeichencode:
    # die Reihenfolge bei Gleichstand wird deshalb nicht verglichen, nur die Anzahl absteigend.
    zahlen = [r[di["Anforderungen"]] for r in dbody]
    check(zahlen == sorted(zahlen, reverse=True), "nach Anzahl der Anforderungen absteigend sortiert")
    bad = []
    for r in dbody:
        e = erwartet.get(r[di["Dokument"]])
        if not e or r[di["Anforderungen"]] != e["anzahl"] or r[di["davon MUSS"]] != e["muss"] \
                or r[di["Praktiken"]] != ", ".join(sorted(e["praktiken"], key=order.index)):
            bad.append(r[di["Dokument"]])
    check(not bad, "Anzahl, MUSS und Praktiken je Dokument stimmen" + (f" (falsch: {bad[:3]})" if bad else ""))
    check(sum(r[di["Anforderungen"]] for r in dbody) == sum(1 for r in cbody if r[col["Dokumentiert in"]]),
          f"Summe der Anforderungen = Zeilen mit Dokument in der CSV ({sum(1 for r in cbody if r[col['Dokumentiert in']])})")
    by_json = {d["dokument"]: d for d in payload["dokumente"]}
    bad = [r[di["Dokument"]] for r in dbody
           if (r[di["Beschreibung laut BSI-Tabelle"]] or "") != by_json[r[di["Dokument"]]]["beschreibung"]
           or (r[di["Kategorie"]] or "") != by_json[r[di["Dokument"]]]["kategorie"]]
    check(not bad, "Beschreibung und Kategorie stimmen mit den Daten des Generators überein" + (f" (falsch: {bad[:3]})" if bad else ""))
    # Jeder Dokumenttyp ohne Beschreibung muss das im Hinweis sagen.
    stumm = [r[di["Dokument"]] for r in dbody if not r[di["Beschreibung laut BSI-Tabelle"]] and not r[di["Hinweis zur Beschreibung"]]]
    check(not stumm, "jeder Dokumenttyp ohne Beschreibung erklärt im Hinweis, warum" + (f" (stumm: {stumm[:3]})" if stumm else ""))

    # --- Blatt Info: Lizenzfelder ---------------------------------------------------------
    print("\nBlatt \"Info & Lizenz\"")
    alle = " ".join(str(c if not isinstance(c, dict) else c["text"]) for r in sheets["Info & Lizenz"] for c in r if c)
    for feld in ("stand", "urheber", "werk", "original", "lizenz", "aenderungen", "weitergabe", "nicht_enthalten", "hinweis", "dokumente", "eigene_werte"):
        check(payload["lizenz"][feld] in alle, f"enthält lizenz.{feld}")
    lt = (DL / "LIZENZ.txt").read_text(encoding="utf-8")
    check(all(payload["lizenz"][k] in lt for k in ("urheber", "original", "lizenz_url", "stand")), "LIZENZ.txt nennt dieselben Angaben")

    print()
    if failures:
        print(f"{len(failures)} Abweichung(en).")
        sys.exit(1)
    print("Mappe und CSV stimmen überein.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
