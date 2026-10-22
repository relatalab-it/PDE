"""Trasformazioni del report 16: legge output/*.csv e stampa i dati incorporati nella pagina.

Uso: python3 -I queries/transform.py   (dalla cartella del report)
Nessun valore è scritto a mano: tutto deriva dai CSV in output/.
"""
import csv, json

def rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def num(s):
    return float(s) if s not in ('', None) else None

A = rows('output/A_istat_asia.csv')
B = rows('output/B_eurostat_sbs_sectors.csv')
C = rows('output/C_eurostat_sbs_sizeclass.csv')

CODES = [('5813', 'J5813', '58.13'), ('5814', 'J5814', '58.14'), ('6391', 'J6391', '63.91'),
         ('7022', 'M7022', '70.22'), ('7320', 'M7320', '73.20')]
GEOS = ['EU27_2020', 'IT', 'DE', 'FR', 'ES']

# A: ISTAT, per codice, imprese senza (0), con (1) dipendenti, totale (9)
a = {(r['ECON_ACTIVITY_NACE_2007'], r['Y_ENTER_WITH_EMPLOYEES']): num(r['OBS_VALUE']) for r in A}
# B: Eurostat, per codice NACE e geo
b = {(r['nace_r2'], r['geo']): num(r['OBS_VALUE']) for r in B}
bflag = {(r['nace_r2'], r['geo']): (r['OBS_FLAG'], r['CONF_STATUS']) for r in B}
# C: Eurostat, per gruppo NACE, classe, geo
c = {(r['nace_r2'], r['size_emp'], r['geo']): num(r['OBS_VALUE']) for r in C}

out = {}
out['A_year'] = A[0]['TIME_PERIOD'][:4]
out['B_year'] = B[0]['TIME_PERIOD'][:4]
out['C_year'] = C[0]['TIME_PERIOD'][:4]
out['A_total'] = [a[(i, '9')] for i, _, _ in CODES]
out['A_with'] = [a[(i, '1')] for i, _, _ in CODES]
out['A_without'] = [a[(i, '0')] for i, _, _ in CODES]
out['A_with_share'] = [round(a[(i, '1')] / a[(i, '9')] * 100, 1) for i, _, _ in CODES]
out['A_sum_total'] = sum(out['A_total'])
out['A_sum_with'] = sum(out['A_with'])
out['A_with_share_all'] = round(out['A_sum_with'] / out['A_sum_total'] * 100, 1)
out['B_it'] = [b[(n, 'IT')] for _, n, _ in CODES]
out['B_it_sum'] = sum(out['B_it'])
out['B_eu'] = [b[(n, 'EU27_2020')] for _, n, _ in CODES]          # None = riservato
out['B_eu_flags'] = [bflag[(n, 'EU27_2020')] for _, n, _ in CODES]
out['B_eu_sum_available'] = sum(v for v in out['B_eu'] if v is not None)
out['B_eu_70_22_share'] = round(b[('M7022', 'EU27_2020')] / out['B_eu_sum_available'] * 100, 1)
out['B_ratio_B_over_A'] = [round(b[(n, 'IT')] / a[(i, '9')] * 100, 1) for i, n, _ in CODES]
out['B_ratio_all'] = round(out['B_it_sum'] / out['A_sum_total'] * 100, 1)
out['B_share'] = {g: [None if b[(n, 'EU27_2020')] is None else round(b[(n, g)] / b[(n, 'EU27_2020')] * 100, 1)
                       for _, n, _ in CODES] for g in ['IT', 'DE', 'FR', 'ES']}
out['B_countries'] = {g: [b[(n, g)] for _, n, _ in CODES] for g in GEOS}

GROUPS = ['J581', 'J639', 'M702', 'M732']
CLASSES = ['0_1', '2-9', '10-19', '20-49', '50-249', 'GE250']
out['C'] = {}
for g in ['EU27_2020', 'IT']:
    for n in GROUPS:
        tot = c[(n, 'TOTAL', g)]
        vals = [c.get((n, s, g)) for s in CLASSES]
        pub = sum(v for v in vals if v is not None)
        # quote sul totale delle classi pubblicate: per M732 UE27 il TOTAL (30.000, bandiera u) è
        # arrotondato e inferiore alla somma delle classi, quindi non è usato come denominatore
        out['C'][f'{n}|{g}'] = {
            'total_published': tot,
            'sum_of_published_classes': pub,
            'classes': vals,
            'shares': [None if v is None else round(v / pub * 100, 1) for v in vals],
        }
print(json.dumps(out, indent=1))
