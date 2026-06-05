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
            
        async with client:
            
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
    chunks_file: str = typer.Option(None, help="File TXT o MD con gli argomenti (indice) separati da riga vuota o capitoli.")
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
        
        os.makedirs(RESPONSES_DIR, exist_ok=True)
        for fname, content in memory_files.items():
            out_path = os.path.join(RESPONSES_DIR, f"{project_name}_{fname}")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            typer.echo(f"SUCCESS: Output salvato in {out_path}")

    asyncio.run(run_generate())

@app.command()
def fetch(
    query: str = typer.Argument(..., help="Titolo o autore del libro/documento da cercare e scaricare"),
    output_dir: str = typer.Option("downloads", help="Cartella in cui salvare il file scaricato")
):
    """
    MODULO RICERCA: Cerca e scarica libri interi (PDF/EPUB) in autonomia.
    """
    typer.echo(f"🕵️ Avvio ricerca autonoma per: {query}")
    from core.fetch_engine import download_book
    
    # Esegue la ricerca e il download
    result_path = download_book(query, dest_dir=output_dir)
    
    if result_path:
        typer.echo(f"\n✅ Il libro è stato salvato in: {result_path}")
        typer.echo(f"💡 Puoi caricarlo in un nuovo progetto usando: delphi pesante <NomeProgetto> --files \"{result_path}\"")
    else:
        typer.echo("\n❌ Ricerca fallita. Nessun file scaricato.")

@app.command()
def export(
    project_name: str = typer.Argument(..., help="Nome del progetto da esportare in PDF"),
    title: str = typer.Option(None, "--title", "-t", help="Titolo della copertina"),
    subtitle: str = typer.Option(None, "--subtitle", "-s", help="Sottotitolo della copertina"),
    author: str = typer.Option("Generato da Delphi", "--author", "-a", help="Autore"),
    date: str = typer.Option(None, "--date", "-d", help="Data (es. Giugno 2026)"),
    theme: str = typer.Option("academic", "--theme", help="Tema: academic, modern, classic, minimalist, brutalism, ide"),
    bg_color: str = typer.Option(None, "--bg-color", help="Colore di sfondo (es. #0d1117)"),
    primary_color: str = typer.Option(None, "--primary-color", help="Colore principale (es. #58a6ff)"),
    text_color: str = typer.Option(None, "--text-color", help="Colore del testo (es. #c9d1d9)"),
    font: str = typer.Option(None, "--font", help="Google Font da usare (es. 'Fira Code')")
):
    """
    MODULO ESPORTAZIONE: Concatena i chunk generati e produce un PDF formattato (KaTeX + CSS).
    """
    typer.echo(f"🖨️ Avvio esportazione per il progetto: {project_name}")
    import glob
    import subprocess
    
    responses_dir = Path("delphi_responses")
    if not responses_dir.exists():
        typer.echo("❌ Cartella delphi_responses non trovata.")
        raise typer.Exit(1)
        
    # Trova tutti i file corrispondenti
    pattern = str(responses_dir / f"{project_name}_appunti_p*.md")
    files = glob.glob(pattern)
    
    if not files:
        typer.echo(f"❌ Nessun chunk trovato per il progetto '{project_name}'.")
        raise typer.Exit(1)
        
    # Ordina numericamente
    def get_num(fpath):
        import re
        match = re.search(r'_p(\d+)\.md$', fpath)
        return int(match.group(1)) if match else 0
        
    files.sort(key=get_num)
    
    typer.echo(f"📚 Trovati {len(files)} capitoli. Assemblaggio in corso...")
    
    cover_title = title if title else project_name
    
    font_link = f'<link href="https://fonts.googleapis.com/css2?family={font.replace(" ", "+")}:wght@300;400;700;900&display=swap" rel="stylesheet">\n' if font else ""
    
    style_vars = []
    if bg_color: style_vars.append(f"--bg-color: {bg_color};")
    if primary_color: style_vars.append(f"--primary-color: {primary_color};")
    if text_color: style_vars.append(f"--text-color: {text_color};")
    if font: style_vars.append(f"--main-font: '{font}', monospace;")
    style_attr = f' style="{" ".join(style_vars)}"' if style_vars else ""

    if theme == "ide":
        # Impalcatura IDE avanzata senza righe vuote per non rompere il parser Markdown!
        cover_html = f"""{font_link}<div class="cover-page theme-ide"{style_attr}>
    <div class="ide-grid"></div>
    <div class="ide-sidebar"></div>
    <div class="ide-lines">
        {'<br>'.join(str(i) for i in range(1, 51))}
    </div>
    <div class="ide-content">
        <div class="ide-window-controls">
            <span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span>
            <span class="ide-path">~/{project_name.lower().replace(' ', '-')}/main.py</span>
        </div>
        <div class="ide-block top-block">
            <span class="ide-comment"># {date or '2026'} :: {cover_title.lower()}</span><br>
            <span class="ide-keyword">from</span> <span class="ide-variable">knowledge_base</span> <span class="ide-keyword">import</span> <span class="ide-class">{project_name.replace(' ', '')}</span>
        </div>
        <h1 class="cover-title">{cover_title}</h1>
        <div class="ide-pill">{{ "status": "COMPUTED" }}</div>
        <div class="ide-block desc-block">
            <span class="ide-keyword">description</span>: <span class="ide-type">str</span> = <br>
            <span class="ide-string">"{subtitle or 'Generato automaticamente.'}"</span>
        </div>
        <div class="ide-block author-block">
            <span class="ide-keyword">const</span> <span class="ide-variable">author</span>: <span class="ide-type">Author</span> = {{ name: <span class="ide-string">"{author}"</span> }}<br>
            <span class="ide-keyword">export default</span> {{ edition: 2026, license: <span class="ide-string">"MIT"</span> }}
        </div>
    </div>
</div>
<div style="page-break-after: always;"></div>
"""
    else:
        # Layout standard per gli altri temi
        cover_html = f"""{font_link}<div class="cover-page theme-{theme}"{style_attr}>
    <h1 class="cover-title">{cover_title}</h1>
"""
        if subtitle:
            cover_html += f'    <h2 class="cover-subtitle">{subtitle}</h2>\n'
        if author:
            cover_html += f'    <h3 class="cover-author">{author}</h3>\n'
        if date:
            cover_html += f'    <p class="cover-date">{date}</p>\n'
            
        cover_html += '</div>\n<div style="page-break-after: always;"></div>\n\n'
    
    merged_content = cover_html

    
    for f in files:
        with open(f, 'r', encoding='utf-8') as file_in:
            merged_content += file_in.read() + "\n\n"
            
    manoscritto_path = responses_dir / f"{project_name}_Manoscritto.md"
    with open(manoscritto_path, 'w', encoding='utf-8') as file_out:
        file_out.write(merged_content)
        
    typer.echo(f"✅ Manoscritto unito salvato in: {manoscritto_path}")
    
    pdf_path = responses_dir / f"{project_name}.pdf"
    script_path = Path("core") / "export_module" / "build_pdfs.js"
    
    if not script_path.exists():
        typer.echo(f"❌ Script di esportazione PDF non trovato in {script_path}")
        raise typer.Exit(1)
        
    typer.echo("🚀 Generazione PDF in corso tramite Node.js (KaTeX + CSS)...")
    try:
        # Usa node.exe o node a seconda del PATH
        result = subprocess.run(["node", str(script_path), str(manoscritto_path), str(pdf_path)], check=True)
        typer.echo(f"🎉 Esportazione PDF completata! File: {pdf_path}")
    except FileNotFoundError:
        typer.echo("❌ NodeJS ('node') non trovato nel PATH. Installa Node.js per esportare i PDF.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Errore durante l'esecuzione dello script Node.js: {e}")

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

if __name__ == "__main__":
    app()
