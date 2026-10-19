#!/usr/bin/env python3
"""Trasformazioni del report 15: legge i CSV in ../output/ e stampa gli array JSON
incorporati nella pagina index.html. Nessun CSV viene modificato.

Uso (dalla cartella del report):  python3 -I queries/transform.py
"""
import collections
import csv
import json
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")


def rows(name, enc="utf-8"):
    with open(os.path.join(OUT, name), encoding=enc, newline="") as f:
        return list(csv.DictReader(f))


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


res = {}

# ── A: ISTAT, comune di Genova (010025), annuale ────────────────────────────
ist = collections.defaultdict(dict)
for r in rows("A_istat_genova.csv"):
    ist[(r["DATA_TYPE"], r["RESULT"])][int(r["TIME_PERIOD"])] = int(r["OBS_VALUE"])
years = sorted(ist[("ROADACC", "9")])
res["A_years"] = years
res["A_incidenti"] = [ist[("ROADACC", "9")][y] for y in years]
res["A_feriti"] = [ist[("KILLINJ", "F")][y] for y in years]
res["A_morti"] = [ist[("KILLINJ", "M")][y] for y in years]

# ── B1: Comune di Genova, sinistri per via e gravità 2010-2016 ──────────────
b1 = rows("B1_comune_sinistri_2010_2016.csv", "latin-1")
agg = collections.defaultdict(lambda: [0, 0, 0, 0])  # con feriti, senza, prognosi, mortali
for r in b1:
    a = agg[norm(r["Strada"])]
    a[0] += int(r["SommaDiCon feriti"])
    a[1] += int(r["SommaDiSenza feriti"])
    a[2] += int(r["SommaDiCon feriti in prognosi riservata"])
    a[3] += int(r["SommaDiMortali"])
tot = {k: sum(v) for k, v in agg.items()}
top = sorted(tot, key=lambda k: (-tot[k], k))[:15]
res["B_top_vie"] = top
res["B_top_senza"] = [agg[k][1] for k in top]
res["B_top_feriti"] = [agg[k][0] for k in top]
res["B_top_prognosi"] = [agg[k][2] for k in top]
res["B_top_mortali"] = [agg[k][3] for k in top]
res["B_top_totale"] = [tot[k] for k in top]
res["B_n_vie"] = len(agg)
res["B_n_sinistri"] = sum(tot.values())
mort = sorted(agg, key=lambda k: (-agg[k][3], -tot[k], k))[:8]
res["B_mortali_vie"] = mort
res["B_mortali_val"] = [agg[k][3] for k in mort]
res["B_mortali_totale"] = [tot[k] for k in mort]

# totali annui del Comune per il cross-check con ISTAT
cross = collections.defaultdict(lambda: {"con_lesioni": 0, "totale": 0})
for r in b1:
    c = cross[int(r["Anno"])]
    c["con_lesioni"] += (int(r["SommaDiCon feriti"])
                         + int(r["SommaDiCon feriti in prognosi riservata"])
                         + int(r["SommaDiMortali"]))
    c["totale"] += int(r["SommaDiTotale"])

# ── B2: Comune di Genova, anno 2017 (etichette diverse, serie non unita) ────
b2 = rows("B2_comune_sinistri_2017.csv", "latin-1")
agg2 = collections.defaultdict(lambda: [0, 0, 0, 0])  # illesi, feriti, prognosi, mortali
for r in b2:
    a = agg2[norm(r["Strada"])]
    a[0] += int(r["illesi"])
    a[1] += int(r["Feriti"])
    a[2] += int(r["P.Riservata"])
    a[3] += int(r["Mortali"])
    c = cross[2017]
    c["con_lesioni"] += int(r["Feriti"]) + int(r["P.Riservata"]) + int(r["Mortali"])
    c["totale"] += int(r["Totale"])
tot2 = {k: sum(v) for k, v in agg2.items()}
top2 = sorted(tot2, key=lambda k: (-tot2[k], k))[:10]
res["B2_top_vie"] = top2
res["B2_top_totale"] = [tot2[k] for k in top2]
res["B2_overlap_top10"] = len(set(top[:10]) & set(top2))
res["B2_righe_duplicate_unite"] = len(b2) - len(agg2)
res["cross_years"] = sorted(cross)
res["cross_comune_con_lesioni"] = [cross[y]["con_lesioni"] for y in sorted(cross)]
res["cross_comune_totale"] = [cross[y]["totale"] for y in sorted(cross)]
res["cross_istat_incidenti"] = [ist[("ROADACC", "9")][y] for y in sorted(cross)]

# ── C: MIT, incidenti per strada, provincia di Genova ───────────────────────
c = [r for r in rows("C_mit_incidenti_per_strada.csv") if r["PROVINCIA"] == "Genova"]


def num(v):
    return None if v.strip() in ("", "-") else int(v)


c.sort(key=lambda r: -(num(r["2018"]) or 0))
res["C_strade"] = [norm(r["NOME STRADA"]) for r in c]
res["C_codici"] = [r["CODICE"] for r in c]
res["C_2018"] = [num(r["2018"]) for r in c]
res["C_estesa_km"] = [float(r["ESTESA"]) for r in c]
res["C_n_strade"] = len(c)

print(json.dumps(res, ensure_ascii=False, indent=1))
