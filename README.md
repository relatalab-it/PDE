# PDE — Public Data Explorer

Demo di **PDE**, il progetto di RELATA Lab che traduce una domanda in linguaggio naturale in interrogazioni ai dati pubblici e restituisce risposte verificabili, tracciabili fino alla fonte.

I report sono **brief giornalistici cross fonte** e usano più connettori open source. Le altre demo sono dimostrazioni su una sola fonte ciascuna. L'orchestrazione tra fonti diverse è l'obiettivo del progetto in corso.

## Cosa c'è

| Percorso | Demo | Fonte |
|---|---|---|
| `report/` | 15 brief giornalistici cross fonte generati da un'AI su dati pubblici, con query riproducibili e log delle operazioni (italiano e inglese) | SDMX: Eurostat, ISTAT, BCE, OCSE, Banca mondiale · CKAN: Comune di Genova, MIT |
| `open-data/maggioli/` | Estrazione e confronto di dati sugli incidenti stradali da portali open data in produzione di sei comuni (italiano e inglese) | CKAN |
| `open-data/comune-di-milano/` | Sei domande in italiano al portale Dati Milano del Comune di Milano: domande, passaggi dell'AI, query e risultati | CKAN |
| `territorio/planet-intelligence/` | Dati geografici di Milano trovati nel catalogo nazionale: caldo, verde, aria, mobilità | RNDT |
| `territorio/milano-evoluzione/` | Come è cresciuta Milano dal 1954 al 2024 | RNDT |
| `territorio/situas/` | Anagrafe dei comuni italiani dal 1861 a oggi: codici ISTAT, variazioni territoriali, dati demografici; caso d'uso sul Comune di Messina | SITUAS (ISTAT) |
| `appalti/anac/` | Appalti pubblici in linguaggio naturale: quattro esempi (bandi aperti, controllo di un CIG, codici scheda, chi compra comunicazione scientifica) con comandi, risultati e limiti (campione 2026) | ANAC |
| `parlamento/exp-audizioni/` | Audizioni della Camera dei deputati e soggetti auditi. Sperimentale: l'elaborazione contiene errori noti | Linked Open Data |

La pagina iniziale (`index.html`) elenca le demo. La demo sugli appalti pubblici (ANAC) è su una sola fonte.

## Grafica

La landing usa il tema Nexora (licenza MIT, © Harshad Mahadik, distribuito da ThemeWagon; file in `assets/landing/`). Le altre pagine condividono una cornice comune caricata da `assets/frame.js` (barra in alto e piè di pagina con il credito). Report e catalogo ricevono palette e font da `assets/style.css` e `assets/shell.js`; le demo territorio da `assets/territorio.css`.

## Struttura del repository

```
index.html        pagina iniziale
report/           catalogo e singoli report (report/NN_slug/)
open-data/        demo sui portali CKAN
territorio/       demo geografiche e SITUAS
appalti/          demo sugli appalti pubblici
parlamento/       demo parlamentare
assets/           stile e script condivisi dai report; frame.js/frame.css (barra e piè di pagina comuni a tutte le demo), territorio.css, landing/ (tema della pagina iniziale)
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
