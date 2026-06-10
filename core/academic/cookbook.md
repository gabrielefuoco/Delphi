# Delphi Academic Engine: Cookbook & Ricettario

Questo documento raccoglie le best practice, i workflow operativi e i prompt collaudati per massimizzare la qualità dell'esportazione accademica tramite il motore Delphi. È il riferimento primario sia per l'Agente che per l'Utente.

---

## 1. Workflow Strutturato: Appunti + Diagrammi Mermaid Contestuali

L'obiettivo di questo workflow è trasformare una classica dispensa testuale "monolitica" in un documento dinamico, dove la teoria viene spezzata e supportata visivamente da diagrammi di flusso, macchine a stati o gerarchie. Questo è cruciale nelle materie STEM (Informatica Teorica, Architettura, Matematica).

### Fase 1: Valutazione Cognitiva (L'Agente)
Prima di definire il `chunks.json`, l'agente deve analizzare l'indice e domandarsi: **"Questo paragrafo trarrebbe beneficio da una visualizzazione?"**
Scegli di iniettare un diagramma se il paragrafo tratta di:
- **Flussi di dati o Algoritmi** (es. Pipeline di compilazione, MapReduce).
- **Gerarchie o Classificazioni** (es. Gerarchia di Chomsky, Classi di Complessità).
- **Architetture hardware/software** (es. Circuiti booleani, Macchine di Turing, Reti Neurali).
- **Stati e Transizioni** (es. Automi a stati finiti).

### Fase 2: Iniezione della Direttiva in `chunks.json`
Non delegare la scelta del diagramma all'LLM in modo generico. Usa il campo `context` per dare **note di regia estremamente specifiche** su come strutturare il diagramma.

**Esempio di iniezione di regia ottimale:**
```json
{
  "id": "04_01",
  "title": "4.1 La classe P/poly",
  "context": "Spiega l'architettura dei circuiti booleani. [NOTA DI REGIA: Interrompi la spiegazione testuale a metà e inserisci un blocco ```mermaid. Usa un 'graph LR' per modellare un circuito booleano. Definisci esplicitamente i nodi di Input (x1, x2), un livello intermedio di porte logiche (AND, OR) e il nodo di Output. Mantieni le etichette sintetiche.]",
  "points": [
    "Definire P/poly come classe di complessità non uniforme",
    "Spiegare la taglia e la profondità polinomiale",
    "Connessione con le macchine di Turing con advice"
  ],
  "types": ["text"]
}
```

### Fase 3: Selezione del Layout e del Tipo di Diagramma
La scelta della direttiva `graph` o del tipo di Mermaid ha un impatto enorme sul rendering PDF finale. Segui queste regole ferree:

1. **`graph LR` (Left-to-Right) - [SCELTA PREFERITA]**: 
   - *Quando usarlo*: Pipeline, circuiti, riduzioni polinomiali.
   - *Perché*: Si espande in larghezza, occupando meno spazio in altezza e scalando elegantemente nel PDF senza "schiacciare" il font.
2. **`graph TD` (Top-Down)**: 
   - *Quando usarlo*: Solo per gerarchie strette (es. Collasso della Gerarchia Polinomiale) o alberi con massimo 3-4 livelli.
   - *Perché*: Se il grafico è troppo profondo (oltre 6 nodi verticali), Puppeteer stringerà l'immagine per farla entrare nella pagina PDF, rendendo il testo microscopico e illeggibile.
3. **`stateDiagram-v2`**: 
   - *Quando usarlo*: Perfetto per Automi a Stati Finiti o Macchine di Turing.
   - *Perché*: Rendering nativo degli stati più compatto.

### Fase 4: Standard di Sicurezza e Anti-Crash (Entity Escaping)
L'LLM genererà codice Mermaid che dovrà essere processato da Puppeteer. Se la sintassi è malata, l'intero export web-to-pdf fallirà.
- **Entità HTML**: L'Informatica Teorica richiede simboli come $\in$ (`&isin;`), $\Sigma$ (`&Sigma;`), $\le$ (`&le;`). 
- Se usati all'interno dell'etichetta di un nodo, Mermaid **esige** che siano contenuti in doppi apici testuali. 
  - ❌ **CRASH CERTO**: `A --> B[Output &isin; {0,1}]`
  - ✅ **SICURO**: `A --> B["Output &isin; {0,1}"]`
> *Nota: Il compilatore Delphi ora tenta di fare l'auto-escaping automatico delle entità via Regex, ma è best practice specificarlo nell'istruzione all'LLM (es. "racchiudi le entità HTML tra virgolette").*

---

## 2. Architettura di Configurazione (delphi.json vs chunks.json)

Delphi utilizza due file principali per gestire il ciclo di vita di un progetto accademico. La separazione delle responsabilità è essenziale:

### A. `delphi.json` (Impostazioni di Macchina e Output)
Questo file risiede nella root del progetto e governa il comportamento del motore di generazione e dei compilatori di output.

- **`generation_settings`**: Contiene parametri come `parallel_workers` per controllare la concorrenza asincrona durante l'interrogazione dell'LLM.
- **`export_settings`**: Permette di definire target di esportazione multipli (es. un PDF web, un EPUB typst, ecc.) che verranno eseguiti in sequenza con un singolo comando `delphi export`. Supporta inoltre la chiave `typography` per iniettare variabili CSS globali (es. `base_font_size` e `paper_size`) senza dover toccare i file di stile di default.

### B. `chunks.json` (Struttura, Semantica e Prompting Globale)
Questo file definisce l'indice del progetto (capitoli e paragrafi) e l'oggetto `globals`.

L'oggetto `globals` è il cuore del prompting dinamico e previene le "allucinazioni semantiche". Inserendo variabili come `target_lettori` (es. "Studenti Universitari Magistrali") e definendo i prompt base nell'oggetto `prompts`, ci si assicura che l'Agente e l'LLM utilizzino la terminologia accademica corretta.

```json
"globals": {
    "materia": "Fisica Quantistica",
    "ruolo": "Professore Universitario",
    "target_lettori": "Dottorandi in Fisica",
    "prompts": {
        "PROMPT_GENERAZIONE": "Agisci come un {ruolo}... per {target_lettori}...",
        "CUSTOM_PROMPT_DIMOSTRAZIONE": "Sei un matematico. Fornisci la dimostrazione formale per {target_lettori}."
    }
}
```
L'agente AI (come te) ha il permesso di **inventare nuovi prompt in `globals`** a seconda delle esigenze (es. `PROMPT_ESERCIZIO`, `PROMPT_RIASSUNTO`), che possono poi essere richiamati dai singoli paragrafi usando `"prompt_ref": "NOME_PROMPT"`.

---

## 3. Prompt Repository: Esempi Collaudati

Oltre alla configurazione, la qualità dell'output dipende interamente dai template inseriti in `globals["prompts"]`. Di seguito un esempio perfetto e collaudato per la generazione di dispense e appunti in ambito **Informatico/Ingegneristico**.

### PROMPT_INFORMATICA (Appunti e Codice)
Questo prompt forza l'LLM a non riassumere, ma a fare una trasposizione didattica completa mantenendo il gergo tecnico in inglese e includendo codice e "tips" da colloquio.

```text
Agisci come un {ruolo} esperto di {materia}.
Il tuo compito è generare una dispensa di appunti perfetta, completa ed estremamente dettagliata basandoti rigorosamente ed ESCLUSIVAMENTE sui documenti e file che ti ho fornito.

Di seguito ti fornirò un blocco specifico dell'indice del corso. Voglio che tu analizzi tutti i documenti caricati, estragga e strutturi ogni singola informazione (definizioni, eccezioni, passaggi logici ed esempi). Non devi fare un riassunto, ma una trasposizione completa ed esaustiva.

Segui queste regole tassative per la generazione dell'output:
**Struttura:** Utilizza un'impaginazione gerarchica e pulita. Ogni risposta generata deve iniziare obbligatoriamente con un ## per il titolo del paragrafo/sezione corrente, e utilizzare ### o #### per i sotto-argomenti.
**Regola della lingua:** Tutto l'output testuale deve essere in ITALIANO tecnico e accademico, ma mantieni TASSATIVAMENTE in INGLESE i termini ingegneristici, i nomi dei design pattern e i concetti architetturali (es. non tradurre 'Garbage Collection' o 'Event Loop').
**Esaustività Massima:** Il tuo scopo non è fare un riassunto o una sintesi, ma una trasposizione completa. Se nel testo originale c'è un'analogia, un'osservazione particolare o un'eccezione a una regola, riportala. Mantieni un linguaggio formale e rigoroso, ma chiaro e didattico. 
**Flessibilità Didattica:** Adatta autonomamente la struttura al contenuto. 
   - Se il tema è pratico, usa i blocchi a contrasto (Anti-pattern vs Refactoring).
   - Se il tema è teorico o architetturale, preferisci spiegazioni discorsive, modelli mentali o note di approfondimento.
   - Se il tema è algoritmico o da colloquio, inserisci le sezioni "LeetCode Tip" o "Interview Insight".
   - Se riguarda codice, estrai e includi snippet di CODICE REALE dai documenti sorgente (con Type Hints e Docstrings).

Ecco il blocco dell'indice che devi sviluppare in appunti in questo prompt:
{indice_corrente}
```

---

## 4. Gestione del Workspace e Operazioni dell'Agente

- **Isolamento dell'Ambiente**: L'Agente non deve sporcare la root directory di Delphi. Qualsiasi script Python o file di servizio generato temporaneamente DEVE risiedere nella directory del progetto corrente (es. `Projects/Domande Teorica/`).
- **Editing Chirurgico**: Per modificare file Markdown esistenti, privilegia l'uso dei tool nativi (come `replace_file_content`). L'uso di script esterni (bash/python via terminale) è sconsigliato a meno che non si tratti di regex massive su decine di file contemporaneamente.
- **Ricompilazione in Tempo Reale (Watch Mode)**:
  Avviando il comando `py delphi_cli.py export "Nome Progetto" --watch`, Delphi rimarrà in ascolto. Modificando un file `.md` (ad esempio rimuovendo manualmente del fluff) o sistemando il file `.css`, il sistema ricompilerà automaticamente in background, velocizzando il loop di feedback visivo.
- **Filtro Anti-Slop Integrato**: In fase di compilazione, Delphi effettuerà una scansione regex su tutti i markdown uniti. Se trova frasi come "in qualità di assistente", bloccherà silenziosamente il processo di compilazione? No, avvertirà l'utente (e l'agente) tramite la CLI con un WARNING in testo giallo, in modo che l'agente possa usare un search (es. `grep_search`) per andarlo a rimuovere chirurgicamente.
