# PDE — Public Data Explorer

Demo di **PDE**, il progetto di RELATA Lab che traduce una domanda in linguaggio naturale in interrogazioni ai dati pubblici e restituisce risposte verificabili, tracciabili fino alla fonte.

Sito: <https://relatalab-it.github.io/PDE/>

Le demo sono **proof of concept su singole fonti**, costruiti con connettori open source. L'orchestrazione tra fonti diverse è l'obiettivo del progetto in corso e non è ancora in queste pagine.

## Cosa c'è

| Percorso | Demo | Fonte |
|---|---|---|
| `report/` | 14 report statistici generati da un'AI su dati ufficiali, con query riproducibili e log delle operazioni (italiano e inglese) | SDMX: Eurostat, ISTAT, BCE, OCSE, Banca mondiale |
| `open-data/maggioli/` | Estrazione e confronto di dati sugli incidenti stradali da portali open data in produzione di sei comuni (italiano e inglese) | CKAN |
| `open-data/comune-di-milano/` | Sei domande in italiano al portale Dati Milano del Comune di Milano: domande, passaggi dell'AI, query e risultati | CKAN |
| `territorio/planet-intelligence/` | Dati geografici di Milano trovati nel catalogo nazionale: caldo, verde, aria, mobilità | RNDT |
| `territorio/milano-evoluzione/` | Come è cresciuta Milano dal 1954 al 2024 | RNDT |
| `parlamento/exp-audizioni/` | Audizioni della Camera dei deputati e soggetti auditi. Sperimentale: l'elaborazione contiene errori noti | Linked Open Data |

La pagina iniziale (`index.html`) elenca le demo. I connettori per il registro territoriale ISTAT (SITUAS) e per gli appalti pubblici (ANAC) non hanno ancora una demo pubblica.

## Struttura del repository

```
index.html        pagina iniziale
report/           catalogo e singoli report (report/NN_slug/)
open-data/        demo sui portali CKAN
territorio/       demo geografiche
parlamento/       demo parlamentare
assets/           stile e script condivisi dai report
spec/             metodologia con cui si producono i report
reports.json      elenco dei report, letto dal catalogo e dalla pagina iniziale
```

Ogni report in `report/NN_slug/` contiene la pagina (`index.html`), le query (`queries/`), i dati scaricati (`output/`), i metadati (`metadata/`) e il registro delle operazioni (`notes.md`).

## Metodologia dei report

La cartella `spec/` descrive il flusso con cui si produce un report: brief della storia, ipotesi nulla, piano dei dati, controllo di coerenza prima dei grafici, pagina HTML e verifica finale. L'orchestratore AI usa [opensdmx](https://github.com/ondata/opensdmx) per acquisire i dati dagli endpoint SDMX; il punto di partenza è `spec/specjournalism.md`.

## Provarlo in locale

Il sito è statico, senza build:

```
python3 -m http.server 8000
```

Poi apri <http://localhost:8000/>. Aprire i file direttamente dal disco (`file://`) non funziona, perché le pagine caricano dati con `fetch`.

## Componenti open source

| Componente | Fonte |
|---|---|
| [opensdmx](https://github.com/ondata/opensdmx) | SDMX |
| [ckan-mcp-server](https://github.com/ondata/ckan-mcp-server) | portali CKAN |
| [italianparliament-mcp](https://github.com/ondata/italianparliament-mcp) | Parlamento |
| [opensituas](https://github.com/ondata/opensituas) | SITUAS (ISTAT) |
| [openrndt](https://github.com/ondata/openrndt) | RNDT |
| [anac-pl-pp-cli](https://github.com/aborruso/anac-pl-pp-cli) | ANAC |

## Note

- Alcune pagine caricano librerie e caratteri da servizi esterni (jsDelivr, unpkg, cdnjs, Google Fonts). La demo `open-data/maggioli/` interroga anche portali e servizi in produzione: il loro contenuto può cambiare.
- I dati hanno le licenze delle fonti da cui provengono; ogni report indica le proprie.
- **Licenza**: per questo repository non è ancora definita. La demo `parlamento/exp-audizioni/` è distribuita con licenza MIT (vedi il suo `README.md`).
