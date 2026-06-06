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

STATE_FILE = "delphi_state.json"  # Legacy, kept for migration
RESPONSES_DIR = "./delphi_responses"
PROJECTS_DIR = Path.cwd() / "Projects"

def _get_project_dir(project_name: str) -> Path:
    return PROJECTS_DIR / project_name

def _load_project_config(project_name: str) -> dict:
    """Carica la configurazione dal delphi.json del progetto specifico."""
    config_path = _get_project_dir(project_name) / "delphi.json"
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))
    return {}

def _save_project_config(project_name: str, config: dict):
    """Salva la configurazione nel delphi.json del progetto specifico."""
    config_path = _get_project_dir(project_name) / "delphi.json"
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

def _get_notebook_id(project_name: str) -> str:
    config = _load_project_config(project_name)
    return config.get("notebook", {}).get("id")

def _get_notebook(project_name: str) -> dict:
    config = _load_project_config(project_name)
    return config.get("notebook")

def _set_notebook(project_name: str, notebook_id: str, title: str):
    """Registra un notebook nel delphi.json del progetto."""
    config = _load_project_config(project_name)
    config["notebook"] = {
        "id": notebook_id,
        "title": title,
        "disabled_sources": config.get("notebook", {}).get("disabled_sources", [])
    }
    _save_project_config(project_name, config)

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
                
                _set_notebook(project_name, notebook_id, nb_title)
                
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
                disabled = nb_data.get("disabled_sources", []) if nb_data else []
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
        config = _load_project_config(project_name)
        nb_data = config.get("notebook", {})
        disabled = nb_data.get("disabled_sources", [])
        if disable and disable not in disabled:
            disabled.append(disable)
            typer.echo(f"🔴 Fonte {disable} DISATTIVATA.")
        if enable and enable in disabled:
            disabled.remove(enable)
            typer.echo(f"🟢 Fonte {enable} RIATTIVATA.")
        nb_data["disabled_sources"] = disabled
        config["notebook"] = nb_data
        _save_project_config(project_name, config)
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
    chunks_file: str = typer.Option(None, help="File TXT o JSON con gli argomenti (indice)."),
    chunks_ids: str = typer.Option(None, help="ID dei chunk da generare separati da virgola (se json)"),
    academic: bool = typer.Option(False, "--academic", help="Preserva e converte le citazioni generate da NotebookLM in formato Pandoc")
):
    """
    MODULO GENERAZIONE: Recupera le fonti attive e lancia la generazione massiva parallela.
    """
    nb = _get_notebook(project_name)
    if not nb:
        typer.echo(f"❌ Nessun notebook associato al progetto '{project_name}'. Lancia prima il setup.")
        raise typer.Exit(1)
        
    nb_id = nb.get("id")
    disabled_sources = nb.get("disabled_sources", [])
    typer.echo(f"🏗️ Avvio Generazione per il progetto: {project_name}...")
    
    from core.generation_manager import load_chunks, prepare_chapter_directories, make_disk_callback
    
    chunks_data = load_chunks(chunks_file, chunks_ids)
    if not chunks_file or not os.path.exists(chunks_file or ""):
        typer.echo("⚠️ Nessun file chunks fornito. Verrà generato un singolo chunk base.")

    import asyncio
    from core.notebooklm_engine import generation_task
    
    async def run_generate():
        project_dir = Path.cwd() / "Projects" / project_name
        if not project_dir.exists() or not (project_dir / "delphi.json").exists():
            typer.echo(f"❌ Struttura Delphi non trovata per '{project_name}'. Esegui 'delphi init' prima di generare.")
            raise typer.Exit(1)
            
        from core.academic.lib.project import ProjectManager
        pm = ProjectManager(Path.cwd() / "Projects")
        
        typer.echo(f"📥 Progetto strutturato rilevato. Inizializzazione salvataggio progressivo...")
        
        chap_map, _, _ = prepare_chapter_directories(project_dir, chunks_data, chunks_ids, pm)
        
        callback = make_disk_callback(
            chap_map,
            on_save=lambda chap, fname: typer.echo(f"💾 Salvato Paragrafo in {chap}/{fname}")
        )

        await generation_task(nb_id, chunks_data, materia, ruolo, prompt, disabled_sources, academic, on_chunk_completed=callback)

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
def clear_all(
    project_name: str = typer.Argument(None, help="Nome del progetto da pulire (opzionale, se omesso pulisce tutti)")
):
    """
    GARBAGE COLLECTION: Rimuove i notebook NotebookLM associati ai progetti e pulisce lo stato.
    """
    import asyncio
    from notebooklm import NotebookLMClient
    import notebooklm.paths
    
    if project_name:
        # Pulisci un singolo progetto
        nb = _get_notebook(project_name)
        if not nb:
            typer.echo(f"⚠️ Nessun notebook associato al progetto '{project_name}'.")
            return
        
        async def delete_single():
            official_path = str(notebooklm.paths.get_storage_path())
            client = await NotebookLMClient.from_storage(official_path, timeout=600)
            async with client:
                try:
                    typer.echo(f"🗑️ Eliminazione notebook: {nb['title']} (ID: {nb['id']})")
                    await client.notebooks.delete(nb['id'])
                    typer.echo("✅ Notebook eliminato da NotebookLM.")
                except Exception as e:
                    typer.echo(f"⚠️ Errore eliminazione remota: {e}")
            # Rimuovi dal config locale
            config = _load_project_config(project_name)
            config.pop("notebook", None)
            _save_project_config(project_name, config)
            typer.echo("✅ Stato locale ripulito.")
        
        asyncio.run(delete_single())
    else:
        # Pulisci tutti i progetti
        projects_dir = Path.cwd() / "Projects"
        if not projects_dir.exists():
            typer.echo("📭 Nessun progetto trovato.")
            return
        
        async def delete_all():
            official_path = str(notebooklm.paths.get_storage_path())
            client = await NotebookLMClient.from_storage(official_path, timeout=600)
            async with client:
                for pdir in projects_dir.iterdir():
                    if pdir.is_dir() and (pdir / "delphi.json").exists():
                        config = json.loads((pdir / "delphi.json").read_text(encoding="utf-8"))
                        nb = config.get("notebook")
                        if nb and nb.get("id"):
                            try:
                                typer.echo(f"🗑️ Eliminazione: {nb.get('title', pdir.name)} (ID: {nb['id']})")
                                await client.notebooks.delete(nb['id'])
                            except Exception as e:
                                typer.echo(f"  ⚠️ Errore: {e}")
                            config.pop("notebook", None)
                            (pdir / "delphi.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
            typer.echo("✅ Pulizia completata.")
        
        asyncio.run(delete_all())

@app.command()
def status(
    project_name: str = typer.Argument(None, help="Nome del progetto (opzionale)")
):
    """Mostra lo stato del notebook associato a un progetto (o di tutti)."""
    if project_name:
        config = _load_project_config(project_name)
        nb = config.get("notebook")
        if nb:
            typer.echo(f"📓 Progetto: {project_name}")
            typer.echo(f"   Notebook ID: {nb.get('id', 'N/A')}")
            typer.echo(f"   Titolo: {nb.get('title', 'N/A')}")
            disabled = nb.get('disabled_sources', [])
            typer.echo(f"   Fonti disattivate: {len(disabled)}")
        else:
            typer.echo(f"📭 Nessun notebook associato a '{project_name}'.")
    else:
        projects_dir = Path.cwd() / "Projects"
        if not projects_dir.exists():
            typer.echo("📭 Nessun progetto trovato.")
            return
        found = False
        for pdir in sorted(projects_dir.iterdir()):
            if pdir.is_dir() and (pdir / "delphi.json").exists():
                config = json.loads((pdir / "delphi.json").read_text(encoding="utf-8"))
                nb = config.get("notebook")
                if nb:
                    found = True
                    typer.echo(f"📓 {pdir.name} → {nb.get('id', 'N/A')[:12]}... ({nb.get('title', '')})")
        if not found:
            typer.echo("📭 Nessun progetto ha un notebook associato.")

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
        
        chunks_file = project_dir / "chunks.json"
        if not chunks_file.exists():
            default_chunks = [
                {
                    "id": "01_Introduzione",
                    "title": "Introduzione",
                    "paragraphs": [
                        {
                            "id": "1",
                            "title": "Panoramica Generale",
                            "content": "Inserisci qui il prompt che l'agente dovrà usare per estrarre questo paragrafo dai documenti."
                        }
                    ]
                }
            ]
            chunks_file.write_text(json.dumps(default_chunks, indent=2, ensure_ascii=False), encoding="utf-8")
            
        typer.echo(f"✅ Progetto accademico '{project_name}' inizializzato in: {project_dir}")
        typer.echo(f"📄 Creato template chunks.json in: {chunks_file}")
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

@app.command("create-launcher")
def create_launcher(
    project_name: str = typer.Argument(..., help="Nome del progetto"),
    materia: str = typer.Option("Generale", help="La materia o l'argomento (es. Ingegneria del Software)"),
    ruolo: str = typer.Option("Tutor Accademico", help="Il ruolo che l'LLM deve assumere"),
    prompt: str = typer.Option(None, help="Prompt personalizzato di estrazione (se non fornito usa il default). Usa {indice_corrente} per il chunk."),
    chunks_file: str = typer.Option(None, help="File TXT o JSON con gli argomenti (indice)."),
    chunks_ids: str = typer.Option(None, help="ID dei chunk da generare separati da virgola (se json)"),
    academic: bool = typer.Option(False, "--academic", help="Preserva e converte le citazioni generate da NotebookLM in formato Pandoc")
):
    """
    MODULO GENERAZIONE OFF-GRID: Crea uno script .ps1 o .bat per avviare la generazione asincrona in locale, senza bloccare l'agente.
    """
    from pathlib import Path
    import sys

    cmd = [f'py delphi_cli.py generate "{project_name}"']
    cmd.append(f'--materia "{materia}"')
    cmd.append(f'--ruolo "{ruolo}"')
    
    if prompt:
        cmd.append(f'--prompt "{prompt}"')
    if chunks_file:
        cmd.append(f'--chunks-file "{chunks_file}"')
    if chunks_ids:
        cmd.append(f'--chunks-ids "{chunks_ids}"')
    if academic:
        cmd.append('--academic')

    final_command = " ".join(cmd)
    
    # Crea lo script PowerShell
    ps1_content = f"""# Script generato automaticamente da Delphi
echo "Avvio generazione per: {project_name}..."
{final_command}
echo "Generazione terminata. Puoi tornare all'agente per il controllo."
pause
"""
    script_name = f"build_{project_name.replace(' ', '_')}.ps1"
    script_path = Path.cwd() / script_name
    script_path.write_text(ps1_content, encoding="utf-8")
    
    typer.echo(f"✅ Script di avvio creato in: {script_path}")
    typer.echo("Esegui questo script dal tuo terminale per lanciare la generazione senza bloccare l'agente.")

if __name__ == "__main__":
    app()
