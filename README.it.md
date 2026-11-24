# Delphi — Academic Engine

Un motore a riga di comando che gestisce l'intero ciclo di vita di un documento accademico lungo: inizializza la struttura, raccoglie le fonti, guida la scrittura, fa il lint del Markdown e compila il risultato. Il progetto è dato su disco; la scrittura è delegata a NotebookLM, ancorata alle fonti che sono state caricate.

## Indice

- [I comandi](#i-comandi)
- [Come funziona](#come-funziona)
- [Decisioni](#decisioni)
- [Mappa del repository](#mappa-del-repository)
- [Eseguirlo](#eseguirlo)
- [Limiti](#limiti)

## I comandi

| Comando | Cosa fa |
|---|---|
| `init` | crea lo scheletro di un progetto: il manifest dei chunk, i metadati e l'albero delle cartelle per una tesi o un paper |
| `setup` | crea un notebook su NotebookLM, carica le fonti ed esegue la ricerca web per quel progetto |
| `fetch` | cerca e scarica un libro per titolo, autore o ISBN |
| `sources` | elenca le fonti attive di un progetto |
| `curate` | disattiva, riattiva o rimuove fonti |
| `generate` | genera il contenuto del progetto a chunk, in parallelo, da ruoli, materie e prompt personalizzati |
| `lint` | controlla l'integrità del Markdown e corregge ciò che si può correggere meccanicamente |
| `export` | compila il progetto in PDF (typst o web), DOCX o EPUB, conservando le citazioni |
| `status` | mostra lo stato dei notebook associati ai progetti |
| `clear_all` | fa garbage collection delle risorse non più necessarie |
| `create-launcher` | genera il launcher per una generazione in batch |

## Come funziona

### Il progetto è dato

Un progetto è una cartella sotto `Projects/` con `delphi.json` (metadati: titolo, autore, università, versione) e `chunks.json` (il piano ordinato del documento, una voce per sezione, con ruolo e materia). Tutto il resto è generato da quel piano. `Projects/` contiene anche progetti reali, che valgono da esempi di come si presenta un manifest per un libro reale: sei capitoli, ventidue sezioni.

Trattare un libro come un manifest invece che come una cartella di file è ciò che rende possibile il resto: la generazione può riprendere dal chunk 17, `curate` può parlare di «le fonti del capitolo 3», e l'export può ricostruire qualunque formato dallo stesso piano.

### La generazione gira su NotebookLM

`generate` non chiama un'API di un modello. Pilota **NotebookLM** tramite il client Python `notebooklm`, autenticato con una sessione browser salvata (`NotebookLMClient.from_storage`). La ragione è l'ancoraggio: NotebookLM risponde dai documenti caricati in quel notebook, quindi il capitolo viene scritto contro le fonti e non contro la memoria del modello sulla letteratura. Il prezzo è che la pipeline dipende da un prodotto web e dalla sua sessione, non da un'API stabile.

### Prima il lint, poi l'export

`lint` è un linter Markdown scritto per uno scopo: il documento deve sopravvivere a pandoc e a typst. Controlla header setext, fence mermaid malformate, liste incollate, indentazione delle liste, label fantasma, sequenze di righe vuote, simboli orfani, documenti senza H2, blocchi matematici vuoti. Con `--fix` ripara ciò che è meccanico, e non tocca mai la prosa: la struttura si corregge per regola, il contenuto non si riscrive con una regex.

### L'export

`export` compila il piano in pandoc e poi in **typst** per il PDF, con script Node per unire i PDF e costruire le immagini di copertina; DOCX ed EPUB passano da pandoc con un foglio di stile. Le citazioni vengono da un file BibTeX letto nel progetto, quindi la bibliografia si rigenera invece di essere incollata.

## Decisioni

**Un manifest di chunk invece di un mucchio di file.** Il documento è generato a pezzi da un servizio remoto che può fallire, andare in timeout o smettere di esistere; un piano su disco rende ogni passo riprendibile e ogni output sostituibile.

**NotebookLM invece di un'API di modello.** L'ancoraggio alle fonti caricate è tutto il punto: un capitolo che cita la bibliografia deve essere scritto con la bibliografia davanti. Il compromesso è dichiarato — una sessione web invece di un contratto d'API.

**Typst invece di LaTeX.** Un'installazione TeX completa è un prerequisito pesante per chi vuole solo un PDF; typst è un binario singolo, compila in secondi ed è sufficiente per un libro con la copertina.

**La struttura si corregge per regola, il contenuto mai.** Il linter con `--fix` esiste perché il Markdown si rompe sempre allo stesso modo quando cresce — indentazione, fence, righe vuote. Riscrivere la prosa con una regex è il modo in cui un documento comincia a mentire su se stesso.

**Gli strumenti esterni si cercano prima nel PATH.** `pandoc` e `typst` vengono cercati nel sistema prima di qualunque copia inclusa, così lo stesso codice funziona come CLI e come skill invocata da un agente.

## Mappa del repository

```
delphi_cli.py        la CLI Typer: undici comandi
core/academic/lib/   modello di progetto, parser BibTeX, servizio citazioni, linter, compilatore
core/export_module/  script Node per merge dei PDF e copertine, fogli di stile print ed EPUB
core/*.py            motore NotebookLM e integrazioni
Projects/            progetti reali, ciascuno con delphi.json e chunks.json
agent.md             istruzioni per un agente AI che pilota Delphi
```

## Eseguirlo

```bash
pip install -r requirements.txt
python delphi_cli.py --help
```

Oltre alle dipendenze Python, il passo di export richiede **pandoc**, **typst** e **Node.js** nel PATH; `paths.py` ricade su una copia inclusa quando mancano. I comandi NotebookLM richiedono una sessione autenticata, creata una volta e riusata.

Sequenza tipica per un documento nuovo:

```bash
python delphi_cli.py init
python delphi_cli.py setup --project "My Project"
python delphi_cli.py generate --project "My Project"
python delphi_cli.py lint --project "My Project" --fix
python delphi_cli.py export --project "My Project" --format pdf
```

## Limiti

| Cosa | Impatto | Stato |
|---|---|---|
| Il client NotebookLM non è ufficiale | pilota un prodotto web tramite una sessione salvata: un cambio di interfaccia o una sessione scaduta fermano la generazione finché non viene rinnovata | accettato, per progetto |
| `fetch` usa Z-Library | le fonti vengono da una biblioteca ombra, quindi la posizione legale dipende dalla giurisdizione e dal materiale | accettato, vale la pena dichiararlo |
| pandoc, typst e Node non sono nei `requirements.txt` | un'installazione pulita fallisce al passo di export, non all'import | aperto, la prima cosa da sistemare |
| Nessun test automatico | il linter ha regole ma non fixture: le regressioni si trovano sul documento | aperto |
| `Projects/` contiene documenti reali | il repository fa anche da archivio, quindi il contenuto viaggia col codice | accettato |
| La qualità di un capitolo generato non è misurata | non c'è un controllo di copertura o coerenza per chunk, solo il linter delle citazioni | aperto, il buco più grande |
