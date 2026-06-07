# Delphi - Academic Engine

Delphi è un motore accademico (Academic Engine) sviluppato in Python. Permette di gestire progetti, effettuare ricerche, strutturare, generare e compilare progetti accademici.

## Struttura del Progetto

- `delphi_cli.py`: L'interfaccia a riga di comando principale per interagire con Delphi.
- `core/`: Contiene i moduli core dell'applicazione.
- `Projects/`: Directory dove vengono salvati i progetti generati/gestiti da Delphi.
- `agent.md`: Documentazione/istruzioni per l'agente AI su come interagire con Delphi.
- `requirements.txt`: Dipendenze Python necessarie per il progetto.

## Installazione

Per installare le dipendenze:
```bash
pip install -r requirements.txt
```

## Utilizzo

Esegui lo script principale per interagire con l'applicazione:
```bash
python delphi_cli.py --help
```

## Funzionalità

Delphi offre una suite di strumenti integrati tramite CLI per gestire l'intero ciclo di vita di un progetto accademico:

- **Inizializzazione Progetto (`init`)**: Crea una nuova struttura per tesi o paper, generando il template base (`chunks.json`).
- **Ricerca e Acquisizione (`fetch`, `setup`)**: Cerca e scarica automaticamente risorse (es. da Z-Library) e inizializza un notebook su NotebookLM con le fonti desiderate (file locali, URL, ricerca web).
- **Gestione Fonti (`sources`, `curate`)**: Permette di visualizzare le fonti attive e gestirle tramite azioni di disattivazione, riattivazione o eliminazione automatica/manuale.
- **Generazione Massiva (`generate`, `create-launcher`)**: Sfrutta NotebookLM per la generazione parallela dei contenuti del progetto in base a ruoli, materie e prompt personalizzati, salvando progressivamente i risultati.
- **Revisione e Validazione (`lint`)**: Verifica l'integrità dei file di progetto e controlla la presenza di citazioni mancanti.
- **Esportazione (`export`)**: Compila il progetto strutturato nel formato finale desiderato, supportando PDF (tramite `typst` o `web`), DOCX ed EPUB, conservando le citazioni accademiche.
- **Gestione Stato (`status`, `clear_all`)**: Mostra lo stato dei notebook associati ai progetti ed esegue garbage collection per pulire e rimuovere risorse non più necessarie.
