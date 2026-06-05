import typer
import os
import sys
import json
from pathlib import Path

# Fix per gli emoji su console Windows
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

app = typer.Typer(
    help="Delphi: L'Oracolo documentale per l'Agente Antigravity",
    add_completion=False,
    no_args_is_help=True
)

STATE_FILE = "delphi_state.json"
RESPONSES_DIR = "./delphi_responses"

def _load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"notebooks": []}

def _save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

@app.command()
def leggero(
    query: str = typer.Argument(..., help="Cosa cercare nella documentazione"),
    libs: str = typer.Option(..., help="Librerie target separate da virgola (es. fastapi,tortoise-orm)"),
):
    """
    FLUSSO LEGGERO: Usa Context7 per estrarre direttamente frammenti di codice o documentazione.
    """
    typer.echo(f"🔍 Avvio Flusso Leggero per librerie: {libs}...")
    typer.echo(f"❓ Query: {query}")
    # TODO: Integrazione Context7
    pass

def _get_notebook(project_name: str) -> dict:
    state = _load_state()
    target_title = f"[DELPHI-TMP] {project_name}"
    for nb in state.get("notebooks", []):
        if nb.get("title") == target_title:
            return nb
    return None

def _get_notebook_id(project_name: str) -> str:
    nb = _get_notebook(project_name)
    return nb.get("id") if nb else None

@app.command()
def setup(
    project_name: str = typer.Argument(..., help="Nome del progetto (per raggruppare i file)"),
    files: str = typer.Option(None, help="File locali da caricare (separati da virgola, es. doc.pdf,appunti.md)"),
    urls: str = typer.Option(None, help="URL o video YouTube da caricare (separati da virgola)"),
    research: str = typer.Option(None, help="Query per l'agente di ricerca web integrato"),
    libs: str = typer.Option("", help="Librerie da scaricare via context7 e caricare (opzionale)")
):
    """
    MODULO SETUP: Crea un nuovo NotebookLM, carica le fonti e fa ricerca web. Si ferma qui.
    """
    typer.echo(f"🏗️ Avvio Setup per il progetto: {project_name}...")
    import asyncio
    from core.notebooklm_engine import _log
    from notebooklm import NotebookLMClient
    import notebooklm.paths
    import subprocess
    import sys

    async def run_setup():
        official_path = str(notebooklm.paths.get_storage_path())
        client = await NotebookLMClient.from_storage(official_path, timeout=600)
        async with client:
            nb_title = f"[DELPHI-TMP] {project_name}"
            # Controllo se esiste già
            existing_id = _get_notebook_id(project_name)
            if existing_id:
                typer.echo(f"⚠️ Il progetto '{project_name}' esiste già (ID: {existing_id}). Verranno aggiunte le nuove fonti a questo notebook.")
                notebook_id = existing_id
            else:
                _log(f"Creazione notebook: {nb_title} ...")
                notebook = await client.notebooks.create(title=nb_title)
                notebook_id = notebook.id
                _log(f"✅ Notebook creato con ID: {notebook_id}")
                
                state = _load_state()
                state["notebooks"].append({
                    "id": notebook_id,
                    "title": nb_title,
                    "ownership": "created_by_delphi",
                    "libs": libs.split(",") if libs else []
                })
                _save_state(state)
                
            if files:
                for fpath in files.split(","):
                    fpath = fpath.strip()
                    if fpath:
                        _log(f"Caricamento file: {fpath}...")
                        subprocess.run([sys.executable, "-m", "notebooklm", "source", "add", fpath, "--notebook", notebook_id])
            
            if urls:
                for url in urls.split(","):
                    url = url.strip()
                    if url:
                        _log(f"Caricamento URL: {url}...")
                        subprocess.run([sys.executable, "-m", "notebooklm", "source", "add", url, "--notebook", notebook_id])
                        
            if research:
                _log(f"Avvio Agente di Ricerca su: '{research}'...")
                subprocess.run([sys.executable, "-m", "notebooklm", "source", "add-research", research, "--mode", "deep", "--notebook", notebook_id])
                _log("Attesa completamento ricerca (importazione fonti in corso)...")
                subprocess.run([sys.executable, "-m", "notebooklm", "research", "wait", "--import-all", "--notebook", notebook_id])
                
        typer.echo(f"🎉 Setup completato. Usa 'delphi sources {project_name}' per vedere le fonti caricate.")

    asyncio.run(run_setup())

@app.command()
def sources(project_name: str = typer.Argument(..., help="Nome del progetto")):
    """
    MODULO ISPEZIONE: Mostra tutte le fonti attualmente attive nel progetto.
    """
    nb_id = _get_notebook_id(project_name)
    if not nb_id:
        typer.echo(f"❌ Progetto '{project_name}' non trovato. Lancia prima il setup.")
        raise typer.Exit(1)
        
    import asyncio
    from notebooklm import NotebookLMClient
    import notebooklm.paths
    
    async def run_sources():
        official_path = str(notebooklm.paths.get_storage_path())
        client = await NotebookLMClient.from_storage(official_path, timeout=600)
        async with client:
            typer.echo(f"📋 Recupero fonti per il notebook {nb_id[:8]}...")
            sources_list = await client.sources.list(nb_id)
            if not sources_list:
                typer.echo("📭 Nessuna fonte caricata.")
                return
            typer.echo(f"📎 {len(sources_list)} fonti trovate:\n")
            for i, s in enumerate(sources_list, 1):
                title = getattr(s, 'title', 'Senza Titolo')
                nb_data = _get_notebook(project_name)
                disabled = nb_data.get("disabled_sources", [])
                status = "🔴 DISATTIVATA" if s.id in disabled else "🟢 ATTIVA"
                typer.echo(f"[{i}] {status} | ID: {s.id} | Titolo: {title[:80]}")
    asyncio.run(run_sources())

@app.command()
def curate(
    project_name: str = typer.Argument(..., help="Nome del progetto"),
    delete: str = typer.Option(None, help="ID della fonte specifica da eliminare (permanente)"),
    auto: str = typer.Option(None, help="Argomento: elimina tutte le fonti che NON contengono queste parole nel titolo"),
    disable: str = typer.Option(None, help="ID della fonte da disattivare logicamente"),
    enable: str = typer.Option(None, help="ID della fonte da riattivare logicamente")
):
    """
    MODULO CURATION: Gestisci lo stato delle fonti (Elimina, Disattiva, Attiva).
    """
    nb = _get_notebook(project_name)
    if not nb:
        typer.echo(f"❌ Progetto '{project_name}' non trovato.")
        raise typer.Exit(1)
        
    nb_id = nb.get("id")
    
    if disable or enable:
        state = _load_state()
        for notebook in state.get("notebooks", []):
            if notebook.get("id") == nb_id:
                disabled = notebook.get("disabled_sources", [])
                if disable and disable not in disabled:
                    disabled.append(disable)
                    typer.echo(f"🔴 Fonte {disable} DISATTIVATA.")
                if enable and enable in disabled:
                    disabled.remove(enable)
                    typer.echo(f"🟢 Fonte {enable} RIATTIVATA.")
                notebook["disabled_sources"] = disabled
                break
        _save_state(state)
        return

    import asyncio
    from notebooklm import NotebookLMClient
    import notebooklm.paths

    async def run_curate():
        official_path = str(notebooklm.paths.get_storage_path())
        client = await NotebookLMClient.from_storage(official_path, timeout=600)
        async with client:
            if delete:
                typer.echo(f"🗑️ Eliminazione fonte {delete}...")
                await client.sources.delete(nb_id, delete)
                typer.echo("✅ Fonte eliminata.")
            elif auto:
                typer.echo(f"🤖 Curation Automatica. Filtro argomento: '{auto}'")
                sources_list = await client.sources.list(nb_id)
                deleted = 0
                keywords = [k.lower() for k in auto.split()]
                for s in sources_list:
                    title = getattr(s, 'title', '').lower()
                    # Elimina se il titolo NON contiene ALMENO una delle keyword dell'argomento
                    if not any(k in title for k in keywords):
                        typer.echo(f"  ❌ Irrilevante: {title[:60]}... (Eliminazione)")
                        await client.sources.delete(nb_id, s.id)
                        deleted += 1
                    else:
                        typer.echo(f"  ✅ Mantenuto: {title[:60]}...")
                typer.echo(f"\n🎉 Pulizia terminata: {deleted} fonti rimosse, {len(sources_list)-deleted} mantenute.")
            else:
                typer.echo("⚠️ Devi specificare --delete <ID> oppure --auto <Argomento>.")
    asyncio.run(run_curate())

@app.command()
def generate(
    project_name: str = typer.Argument(..., help="Nome del progetto"),
    materia: str = typer.Option("Generale", help="La materia o l'argomento (es. Ingegneria del Software)"),
    ruolo: str = typer.Option("Tutor Accademico", help="Il ruolo che l'LLM deve assumere"),
    prompt: str = typer.Option(None, help="Prompt personalizzato di estrazione (se non fornito usa il default). Usa {indice_corrente} per il chunk."),
    chunks_file: str = typer.Option(None, help="File TXT o MD con gli argomenti (indice) separati da riga vuota o capitoli."),
    academic: bool = typer.Option(False, "--academic", help="Preserva e converte le citazioni generate da NotebookLM in formato Pandoc")
):
    """
    MODULO GENERAZIONE: Recupera le fonti attive e lancia la generazione massiva parallela.
    """
    nb = _get_notebook(project_name)
    if not nb:
        typer.echo(f"❌ Progetto '{project_name}' non trovato.")
        raise typer.Exit(1)
        
    nb_id = nb.get("id")
    disabled_sources = nb.get("disabled_sources", [])
    typer.echo(f"🏗️ Avvio Generazione per il progetto: {project_name}...")
    
    chunks_data = []
    if chunks_file and os.path.exists(chunks_file):
        with open(chunks_file, "r", encoding="utf-8") as f:
            content = f.read()
            chunks_data = [c.strip() for c in content.split("\n\n") if c.strip()]
    else:
        typer.echo("⚠️ Nessun file chunks fornito. Verrà generato un singolo chunk base.")
        chunks_data = ["Spiega tutti gli argomenti principali trovati nei documenti."]

    import asyncio
    from core.notebooklm_engine import generation_task
    
    async def run_generate():
        # Avvia la generazione asincrona super-parallela
        memory_files = await generation_task(nb_id, chunks_data, materia, ruolo, prompt, disabled_sources)
        
        from pathlib import Path
        project_dir = Path.cwd() / project_name
        if not project_dir.exists() or not (project_dir / "delphi.json").exists():
            typer.echo(f"❌ Struttura Delphi non trovata per '{project_name}'. Esegui 'delphi init' prima di generare.")
            raise typer.Exit(1)
            
        from core.academic.lib.project import ProjectManager
        import shutil
        import re as re_mod
        pm = ProjectManager(Path.cwd())
        
        typer.echo(f"📥 Progetto strutturato rilevato. Aggiornamento cartella {project_dir}...")
        
        # Rimuovi vecchi capitoli generati automaticamente (che iniziano con cifre e underscore)
        for d in project_dir.iterdir():
            if d.is_dir() and re_mod.match(r'^\d+_', d.name):
                shutil.rmtree(d, ignore_errors=True)
                
        for i, (fname, fcontent) in enumerate(memory_files.items(), 1):
            # Extract real title
            match = re_mod.search(r'^#\s*(?:Capitolo:?\s*)?(.*)', fcontent, re_mod.MULTILINE)
            if match:
                real_title = match.group(1).strip()
                fcontent_clean = fcontent[match.start():]
                # Remove the H1
                fcontent_clean = re_mod.sub(r'^#\s+.*?\n', '', fcontent_clean, count=1).strip()
            else:
                real_title = f"Capitolo {i}"
                fcontent_clean = fcontent
                
            safe_title = re_mod.sub(r'[\\/*?:"<>|]', "", real_title)
            chap = pm.add_chapter(project_dir, safe_title)
                
            if academic:
                def replace_cit(m):
                    nums = m.group(1).split(',')
                    cits = [f"@{n.strip()}" for n in nums]
                    return "[" + "; ".join(cits) + "]"
                fcontent_clean = re_mod.sub(r'\[(\d+(?:\s*,\s*\d+)*)\]', replace_cit, fcontent_clean)
                
            # Clean manual numbering
            fcontent_clean = re_mod.sub(r'^(#{2,})\s+\d+(?:\.\d+)*\.?\s+', r'\1 ', fcontent_clean, flags=re_mod.MULTILINE)
            
            pm.add_paragraph(chap, "Appunti", fcontent_clean, include_header=False)
            typer.echo(f"💾 Salvato Capitolo {i} in {chap.name}")

    asyncio.run(run_generate())

@app.command()
def fetch(
    query: str = typer.Argument(..., help="Termine di ricerca per Z-Library (titolo, autore, ISBN)"),
    project: str = typer.Option(None, "--project", "-p", help="Nome del progetto in cui salvare il file (opzionale)")
):
    """
    MODULO RICERCA: Cerca e scarica automaticamente risorse da Z-Library.
    """
    typer.echo(f"📚 Avvio modulo ricerca per: {query}")
    from core.fetch_engine import download_book
    from pathlib import Path
    
    if project:
        output_dir = Path.cwd() / "Projects" / project / "assets"
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path.cwd() / "downloads"
        output_dir.mkdir(exist_ok=True)
        
    result_path = download_book(query, dest_dir=output_dir)
    
    if result_path:
        typer.echo(f"\n✅ Il libro è stato salvato in: {result_path}")
    else:
        typer.echo("\n❌ Ricerca fallita. Nessun file scaricato.")

@app.command()
def export(
    project_name: str = typer.Argument(..., help="Nome del progetto da esportare in PDF/DOCX"),
    format: str = typer.Option("pdf", "--format", "-f", help="Formato: 'pdf' o 'docx'"),
    engine: str = typer.Option("typst", "--engine", "-e", help="Motore di rendering per PDF: 'typst' o 'web'")
):
    """
    MODULO ESPORTAZIONE: Compila il progetto strutturato nel formato finale.
    """
    typer.echo(f"🖨️ Avvio esportazione per il progetto: {project_name}")
    from pathlib import Path
    
    project_dir = Path.cwd() / "Projects" / project_name
    if not project_dir.exists() or not (project_dir / "delphi.json").exists():
        typer.echo(f"❌ Struttura Delphi non trovata per '{project_name}'.")
        raise typer.Exit(1)
        
    from core.academic.lib.project import ProjectManager
    pm = ProjectManager(Path.cwd() / "Projects")
    project = pm.load_project(project_dir)
    
    output_dir = project_dir / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{project_name}.{format}"
    
    typer.echo("🎓 Esportazione in corso...")
    try:
        if format == "docx":
            pm.compiler.compile_docx(project, output_file)
        else:
            if engine == "web":
                pm.compiler.compile_web(project, output_file)
            else:
                pm.compiler.compile(project, output_file)
        typer.echo(f"🎉 Esportazione completata: {output_file}")
    except Exception as e:
        typer.echo(f"❌ Errore: {str(e)}")
        raise typer.Exit(1)

@app.command()
def clear_all():
    """
    GARBAGE COLLECTION: Rimuove i NotebookLM creati da Delphi e pulisce lo stato locale.
    """
    state = _load_state()
    notebooks_da_eliminare = [nb for nb in state.get("notebooks", []) if nb.get("ownership") == "created_by_delphi" and nb.get("title", "").startswith("[DELPHI-TMP]")]
    
    if not notebooks_da_eliminare:
        typer.echo("🧹 Nessun notebook temporaneo da eliminare.")
        return

    for nb in notebooks_da_eliminare:
        typer.echo(f"🗑️ Eliminazione da NotebookLM: {nb['title']} (ID: {nb['id']})")
        # TODO: Aggiungere logica di delete notebooklm-py
    
    _save_state({"notebooks": []})
    typer.echo("✅ Pulizia completata.")

@app.command()
def status():
    """Mostra lo stato attuale del database locale (Notebook attivi)."""
    state = _load_state()
    typer.echo(json.dumps(state, indent=2))

@app.command()
def init(
    project_name: str = typer.Argument(..., help="Nome del nuovo progetto accademico")
):
    """
    MODULO PROGETTO: Inizializza una nuova struttura progetto per tesi/paper.
    """
    from core.academic.lib.project import ProjectManager
    from pathlib import Path
    
    try:
        pm = ProjectManager(Path.cwd() / "Projects")
        project_dir = pm.init_project(project_name)
        typer.echo(f"✅ Progetto accademico '{project_name}' inizializzato in: {project_dir}")
    except Exception as e:
        typer.echo(f"❌ Errore durante l'inizializzazione: {e}")
        raise typer.Exit(1)

@app.command()
def lint(
    project_name: str = typer.Argument(..., help="Nome del progetto da validare")
):
    """
    MODULO REVISIONE: Verifica l'integrità dei file e le citazioni mancanti.
    """
    from core.academic.lib.project import ProjectManager
    from pathlib import Path
    
    pm = ProjectManager(Path.cwd() / "Projects")
    
    if project_name == ".":
        project_dir = Path.cwd()
    else:
        project_dir = Path.cwd() / "Projects" / project_name
    
    if not project_dir.exists():
        typer.echo(f"❌ Progetto non trovato: {project_dir}")
        raise typer.Exit(1)
        
    typer.echo(f"🔍 Avvio linting per '{project_name}'...")
    
    try:
        issues = pm.validate_structure(project_dir, fix=False)
        cit_issues = pm.validate_citations(project_dir)
        
        all_issues = issues + cit_issues
        if not all_issues:
            typer.echo("✅ Nessun problema trovato. Il progetto è perfetto!")
        else:
            typer.echo(f"⚠️  Trovati {len(all_issues)} problemi:")
            for issue in all_issues:
                typer.echo(f"  - {issue}")
    except Exception as e:
        typer.echo(f"❌ Errore durante il linting: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
