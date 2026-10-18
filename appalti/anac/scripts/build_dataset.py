#!/usr/bin/env python3
"""Costruisce i dati della demo ANAC a partire dalle estrazioni grezze in data/raw/.

Uso (dalla cartella appalti/anac/):  python3 scripts/build_dataset.py

Legge:  data/raw/cpv_avanzata.json              avvisi trovati per codice CPV (rete 1)
        data/raw/frase_*__<tipologia>.json      avvisi trovati per frase esatta (rete 2)
        data/raw/extraction-date.txt            data dell'estrazione
Scrive: data/avvisi.json    un record per avviso, con le reti che lo hanno trovato
        data/avvisi_tema.json   solo gli avvisi che superano il filtro per tema (quelli mostrati nella pagina)
        data/sintesi.json   i numeri mostrati nella pagina
Nessun numero della pagina è scritto a mano: tutto si legge da sintesi.json.
"""
import glob, json, os, re, collections, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, 'data', 'raw')
OUT = os.path.join(BASE, 'data')

# I 23 codici CPV della rete 1 (approvati prima dell'estrazione)
CPV_RETE1 = """79416000 79416100 79416200 79340000 79341000 79341100 79341200 79341400 79342000
79952000 79952100 79950000 92111000 92111100 92111200 92111260 92400000 80530000
79300000 79320000 73110000 73210000 79411000""".split()

# Regola del tema, dichiarata nella pagina: l'oggetto dell'avviso parla di comunicazione...
TEMA_COM = re.compile(
    r"comunicazion|divulgazion|ufficio stampa|addett\w* (alla )?stampa|pubbliche relazioni|"
    r"relazioni con i media|media relation|social media|campagn\w+ (informativ|di comunicazion|promozional|pubblicitar)|"
    r"\bspot\b|giornalist|testat", re.I)
# ...e, in più, ha un riferimento scientifico o di ricerca
TEMA_SCI = re.compile(r"scientific|scienz|ricerc[ah]|ricercator", re.I)
# ...e non è un appalto di lavori
ESCLUDI = re.compile(r"\blavori\b", re.I)

OGGI = open(os.path.join(RAW, 'extraction-date.txt')).read().strip()[:10]


def tipo_scheda(c):
    c = c or ''
    if c.startswith('AD'): return 'affidamento diretto'
    if c.startswith('A'): return 'esito'
    if c.startswith('P'): return 'bando'
    if c.startswith('M'): return 'modifica'
    return 'altro'


def descrizione(x):
    for t in x.get('templates') or []:
        d = (t.get('template') or {}).get('metadata', {}).get('descrizione')
        if d: return d.strip()
    return ''


def walk_items(x):
    for t in x.get('templates') or []:
        secs = (t.get('template') or {}).get('sections') or []
        for s in secs:
            for it in s.get('items') or []:
                yield it


def committente(x):
    for t in x.get('templates') or []:
        for s in (t.get('template') or {}).get('sections') or []:
            for sa in (s.get('fields') or {}).get('soggetti_sa') or []:
                return sa.get('denominazione_amministrazione'), sa.get('codice_fiscale')
    return None, None


def num(v):
    try: return float(v)
    except (TypeError, ValueError): return 0.0


def record(x):
    den, cf = committente(x)
    cpv, aggiud, stimato = set(), [], 0.0
    for it in walk_items(x):
        for c in (it.get('cpv') if isinstance(it.get('cpv'), list) else [it.get('cpv')]):
            if isinstance(c, dict): c = c.get('codice') or c.get('code')
            if c: cpv.add(str(c)[:8])
        stimato += num(it.get('valore_complessivo_stimato'))
        for a in it.get('aggiudicatari') or []:
            for s in a.get('soggetti') or []:
                aggiud.append({'denominazione': s.get('denominazione'), 'cf': s.get('codice_fiscale'),
                               'importo': num(a.get('importo'))})
    return {
        'idAvviso': x['idAvviso'], 'idAppalto': x['idAppalto'], 'scheda': x['codiceScheda'],
        'tipo': tipo_scheda(x['codiceScheda']), 'pubblicazione': (x.get('dataPubblicazione') or '')[:10],
        'scadenza': (x.get('dataScadenza') or '')[:10] or None, 'oscurato': bool(x.get('oscurato')),
        'descrizione': descrizione(x), 'committente': den, 'cf_committente': cf,
        'cpv': sorted(cpv), 'valore_stimato': stimato or None,
        'aggiudicatari': aggiud, 'importo_aggiudicato': sum(a['importo'] for a in aggiud) or None,
    }


def load(path):
    d = json.load(open(path, encoding='utf-8'))
    return d.get('content') or []


avvisi = {}
rete1 = set()
for x in load(os.path.join(RAW, 'cpv_avanzata.json')):
    r = avvisi.setdefault(x['idAvviso'], record(x)); r.setdefault('reti', [])
    if 'cpv' not in r['reti']: r['reti'].append('cpv')
    rete1.add(x['idAvviso'])

frasi = collections.OrderedDict()
for p in sorted(glob.glob(os.path.join(RAW, 'frase_*__*.json'))):
    m = re.match(r'frase_(.+)__(.+)\.json$', os.path.basename(p))
    frase, tip = m.group(1).replace('_', ' '), m.group(2)
    items = load(p)
    ids = set()
    for x in items:
        r = avvisi.setdefault(x['idAvviso'], record(x)); r.setdefault('reti', [])
        tag = 'frase: ' + frase
        if tag not in r['reti']: r['reti'].append(tag)
        ids.add(x['idAvviso'])
    f = frasi.setdefault(frase, {'frase': frase, 'per_tipologia': {}, 'ids': set()})
    f['per_tipologia'][tip] = len(items)
    f['ids'] |= ids

# Importi e aggiudicatari: il comando `affidamenti` li estrae per ogni lotto (anche per gli affidamenti diretti,
# dove il dettaglio dell'avviso non li espone). Si agganciano per id_avviso.
affid = collections.defaultdict(list)
for p in sorted(glob.glob(os.path.join(RAW, 'affid_*.json'))):
    try: rows = json.load(open(p, encoding='utf-8'))
    except ValueError: continue
    for row in rows:
        affid[row['id_avviso']].append(row)
for idv, rows in affid.items():
    r = avvisi.get(idv)
    if not r: continue
    seen, ag = set(), []
    for row in rows:
        k = (row.get('cig'), row.get('cf_aggiudicatario'), row.get('importo'))
        if k in seen: continue
        seen.add(k)
        ag.append({'denominazione': row.get('aggiudicatario'), 'cf': row.get('cf_aggiudicatario'),
                   'importo': num(row.get('importo')), 'cig': row.get('cig')})
    r['aggiudicatari'] = ag
    r['importo_aggiudicato'] = sum(a['importo'] for a in ag) or None

for r in avvisi.values():
    r['tema_comunicazione'] = bool(TEMA_COM.search(r['descrizione']))
    r['tema_scientifico'] = (r['tema_comunicazione'] and bool(TEMA_SCI.search(r['descrizione']))
                            and not ESCLUDI.search(r['descrizione']))
    r['fuori_rete_cpv'] = 'cpv' not in r['reti']
    r['cpv_in_rete1'] = [c for c in r['cpv'] if c in CPV_RETE1]

lista = sorted(avvisi.values(), key=lambda r: r['pubblicazione'], reverse=True)
json.dump(lista, open(os.path.join(OUT, 'avvisi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

json.dump([r for r in lista if r['tema_scientifico']], open(os.path.join(OUT, 'avvisi_tema.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- sintesi
tutti = lista
com_ampio = [r for r in tutti if r['tema_comunicazione']]
com = [r for r in tutti if r['tema_scientifico']]
com_tipo = collections.Counter(r['tipo'] for r in com)
tot_frasi = set().union(*[f['ids'] for f in frasi.values()]) if frasi else set()
recuperati = [r for r in com if r['fuori_rete_cpv']]
frasi_com = [r for r in com if any(t.startswith('frase') for t in r['reti'])]


def top(counter, n=10):
    return [{'nome': k, 'n': v} for k, v in counter.most_common(n)]


c_comm = collections.Counter(r['committente'] for r in com if r['committente'])
imp_agg = collections.defaultdict(float)
for r in com:
    for a in r['aggiudicatari']:
        if a['denominazione'] and a['importo']: imp_agg[a['denominazione']] += a['importo']
agg_top = [{'nome': k, 'importo': round(v)} for k, v in sorted(imp_agg.items(), key=lambda kv: -kv[1])[:10]]
imp_comm = collections.defaultdict(float)
for r in com:
    if r['committente'] and r['importo_aggiudicato']: imp_comm[r['committente']] += r['importo_aggiudicato']
comm_imp_top = [{'nome': k, 'importo': round(v)} for k, v in sorted(imp_comm.items(), key=lambda kv: -kv[1])[:10]]
aperti = [r for r in com if r['tipo'] == 'bando' and r['scadenza'] and r['scadenza'] >= OGGI]

sintesi = {
    'estratto_il': OGGI, 'periodo_da': '2026-01-01',
    'rete_cpv': {'codici': len(CPV_RETE1), 'avvisi': len(rete1),
                 'appalti': len({avvisi[i]['idAppalto'] for i in rete1})},
    'rete_frasi': {'frasi': [{'frase': f['frase'], 'per_tipologia': f['per_tipologia'], 'avvisi_distinti': len(f['ids'])}
                              for f in frasi.values()], 'avvisi_distinti': len(tot_frasi),
                   'fuori_dalla_rete_cpv': len([i for i in tot_frasi if i not in rete1])},
    'totale_avvisi_distinti': len(tutti),
    'tema_comunicazione_ampio': {'avvisi': len(com_ampio)},
    'tema_scientifico': {'avvisi': len(com), 'per_tipo': dict(com_tipo),
                         'trovati_dalla_rete_cpv': len([r for r in com if not r['fuori_rete_cpv']]),
                         'trovati_solo_dalle_frasi': len(recuperati),
                         'trovati_dalle_frasi': len(frasi_com)},
    'committenti_per_avvisi': top(c_comm, 12),
    'committenti_per_importo': comm_imp_top,
    'aggiudicatari_per_importo': agg_top,
    'importo_aggiudicato_totale': round(sum(r['importo_aggiudicato'] or 0 for r in com)),
    'avvisi_con_importo': len([r for r in com if r['importo_aggiudicato']]),
    'bandi_aperti': len(aperti),
    'oscurati': len([r for r in tutti if r['oscurato']]),
}
json.dump(sintesi, open(os.path.join(OUT, 'sintesi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(sintesi, ensure_ascii=False, indent=1)[:4500])

# ---- esempi aggiuntivi (piccoli, per la pagina): scala della piattaforma, parole vs frase esatta, CIG, scheda
def _j(name):
    return json.load(open(os.path.join(RAW, name), encoding='utf-8'))

def _desc(x):
    return descrizione(x)

extra = {}
try:
    sc = _j('extra_scala.json')['count']
    extra['scala'] = {'bandi': sc['bandi'], 'esiti': sc['esiti'], 'affidamenti_diretti': sc['affidamenti-diretti'],
                      'totale': sum(sc.values())}
except (OSError, ValueError):
    pass
try:
    ia = {}
    for chiave, f in (('parole', 'extra_bandi_ia.json'), ('frase_esatta', 'extra_bandi_ia_esatta.json')):
        c = _j(f).get('content') or []
        con = [x for x in c if 'intelligenza artificiale' in _desc(x).lower()]
        aperti = [x for x in c if (x.get('dataScadenza') or '')[:10] >= OGGI]
        ia[chiave] = {'avvisi': len(c), 'con_la_frase_nell_oggetto': len(con), 'aperti': len(aperti),
                      'aperti_con_la_frase': len([x for x in aperti if 'intelligenza artificiale' in _desc(x).lower()]),
                      'esempi_senza_la_frase': [_desc(x)[:110] for x in c if 'intelligenza artificiale' not in _desc(x).lower()][:4]}
        if chiave == 'frase_esatta':
            ia[chiave]['elenco_aperti'] = [{'scadenza': (x.get('dataScadenza') or '')[:10], 'committente': committente(x)[0],
                                            'oggetto': _desc(x)[:140]} for x in aperti]
    # avvisi con la frase nell'oggetto che la ricerca per parole ha trovato e quella esatta no
    ids_esatta = {x['idAvviso'] for x in (_j('extra_bandi_ia_esatta.json').get('content') or [])}
    ia['persi_dalla_frase_esatta'] = [
        {'scadenza': (x.get('dataScadenza') or '')[:10], 'committente': committente(x)[0], 'oggetto': _desc(x)}
        for x in (_j('extra_bandi_ia.json').get('content') or [])
        if 'intelligenza artificiale' in _desc(x).lower() and x['idAvviso'] not in ids_esatta]
    extra['intelligenza_artificiale'] = ia
except (OSError, ValueError):
    pass
try:
    extra['cig'] = _j('extra_cig.json')
    extra['scheda_AD3'] = _j('extra_scheda_AD3.json')[0]
except (OSError, ValueError, IndexError):
    pass
sintesi['extra'] = extra
json.dump(sintesi, open(os.path.join(OUT, 'sintesi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
