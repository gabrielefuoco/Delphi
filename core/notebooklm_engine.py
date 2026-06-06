import os
import sys
import asyncio
import traceback
import re
import time
import logging
import httpx

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
from typing import List, Optional, Dict
from notebooklm import NotebookLMClient
import notebooklm.paths

logger = logging.getLogger("delphi.engine")

# Configure stream handler with timestamp if no handlers exist
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)

# Prompt di default per la generazione
PROMPT_GENERAZIONE = r"""Agisci come un {ruolo} esperto di {materia}.
Il tuo compito è generare una dispensa di appunti accademici perfetta, completa ed estremamente dettagliata basandoti rigorosamente ed ESCLUSIVAMENTE sui documenti e file che ti ho fornito.

Target: Livello Universitario Magistrale. Usa un tono accademico, coerente e rigoroso. Nessun riduzionismo o metafore infantili.
Stile Cognitivo: Usa ragionamenti per analogie strutturali e pattern sistemici/informatici. Spiega tramite relazioni causa-effetto e flussi logici.
Formalismo: Se l'argomento prevede dimostrazioni matematiche o formalismi puri, mostrali SOLO alla fine della spiegazione concettuale.

Di seguito ti fornirò un blocco specifico dell'indice. Voglio che tu analizzi tutti i documenti caricati, estragga e strutturi ogni singola informazione chiave, definizioni, riflessioni teoriche ed esempi. Non devi fare un riassunto, ma una trasposizione estesa ed esaustiva.

Regole:
1. Usa linguaggio accademico e rigoroso (ITALIANO).
2. Sii esaustivo: includi prospettive, definizioni ed eccezioni. Non sintetizzare troppo.
3. Se necessario, usa elenchi puntati o modelli logici per spiegare.

Ecco il blocco dell'indice che devi sviluppare in appunti in questo prompt:
{indice_corrente}"""
def split_chapter_by_h2(text: str) -> List[str]:
    lines = text.split('\n')
    h1_title = ""
    for line in lines:
        if line.strip().startswith('# '):
            h1_title = line.strip()
            break
            
    sections = []
    current_section = []
    for line in lines:
        if line.strip().startswith('# '):
            continue
        if line.strip().startswith('## '):
            if current_section:
                sections.append('\n'.join(current_section))
            current_section = [line]
        else:
            if current_section or line.strip():
                current_section.append(line)
                
    if current_section:
        sections.append('\n'.join(current_section))
        
    final_chunks = []
    for sec in sections:
        if h1_title:
            final_chunks.append(f"{h1_title}\n\n{sec}")
        else:
            final_chunks.append(sec)
            
    return final_chunks

def split_markdown_character_fallback(text: str, max_chars: int) -> List[str]:
    if len(text) <= max_chars:
        return [text]
        
    lines = text.split('\n')
    chunks = []
    current_lines = []
    current_len = 0
    
    for line in lines:
        line_len = len(line) + (1 if current_lines else 0)
        if len(line) > max_chars:
            if current_lines:
                chunks.append('\n'.join(current_lines))
                current_lines = []
                current_len = 0
            remaining = line
            while len(remaining) > max_chars:
                split_idx = remaining.rfind(' ', 0, max_chars)
                if split_idx == -1:
                    split_idx = max_chars
                chunks.append(remaining[:split_idx])
                remaining = remaining[split_idx:].lstrip()
            if remaining:
                current_lines.append(remaining)
                current_len = len(remaining)
            continue
            
        if current_len + line_len > max_chars:
            if current_lines:
                chunks.append('\n'.join(current_lines))
                current_lines = [line]
                current_len = len(line)
            else:
                current_lines = [line]
                current_len = len(line)
        else:
            current_lines.append(line)
            current_len += line_len
            
    if current_lines:
        chunks.append('\n'.join(current_lines))
        
    return chunks

def clean_sub_chunk_output(content: str, is_first: bool) -> str:
    content = content.strip()
    
    # 1. Trova il primo e l'ultimo '```' per estrarre il blocco globale (ignorando chatty text)
    first_idx = content.find('```')
    last_idx = content.rfind('```')
    
    if first_idx != -1 and last_idx != -1 and last_idx > first_idx:
        # Estraiamo tutto ciò che c'è tra il primo e l'ultimo backtick
        block = content[first_idx:last_idx]
        lines = block.split('\n')
        if len(lines) >= 2:
            # lines[0] è '```markdown' o '```', la rimuoviamo. L'ultimo '```' è stato escluso da content[first_idx:last_idx]
            content = '\n'.join(lines[1:]).strip()
            
    if is_first:
        return content
        
    lines = content.split('\n')
    cleaned_lines = []
    removed_h1 = False
    
    for line in lines:
        stripped = line.strip()
        if not removed_h1 and stripped.startswith('#') and not stripped.startswith('##'):
            removed_h1 = True
            continue
        cleaned_lines.append(line)
        
    return '\n'.join(cleaned_lines).strip()

def _log(msg: str):
    """Backward-compatible logging wrapper."""
    logger.info(msg)

async def generation_task(notebook_id: str, chunks: List[str], materia: str, ruolo: str, custom_prompt: str, disabled_sources: List[str] = None, academic_mode: bool = False, on_chunk_completed=None) -> Dict[str, str]:
    INITIAL_PARALLEL = 6
    HALVE_THRESHOLD = 3
    memory_files = {}
    if disabled_sources is None:
        disabled_sources = []
    
    if not custom_prompt or not custom_prompt.strip():
        base_prompt = PROMPT_GENERAZIONE
    else:
        base_prompt = custom_prompt.strip()
        
    gen_start = time.monotonic()
    try:
        official_path = str(notebooklm.paths.get_storage_path())
        _log("🔐 Connessione a NotebookLM...")
        
        try:
            client = await NotebookLMClient.from_storage(official_path, timeout=600)
        except Exception as e:
            if "Authentication expired" in str(e) or "invalid" in str(e).lower():
                _log("💥 Sessione scaduta. Avvio procedura di login automatica...")
                import subprocess
                import sys
                res = subprocess.run([sys.executable, "-m", "notebooklm", "login"])
                if res.returncode == 0:
                    _log("✅ Login completato. Ritento connessione...")
                    client = await NotebookLMClient.from_storage(official_path, timeout=600)
                else:
                    raise ValueError(f"Login automatico fallito con codice {res.returncode}")
            else:
                raise e
                
        _log("✅ Connessione stabilita.")

        template_overhead = len(base_prompt) + len(ruolo) + len(materia)
        max_chunk_chars = 4900 - template_overhead
        if max_chunk_chars < 1000:
            max_chunk_chars = 1000
            
        chapters = {}
        original_total = len(chunks)
        for idx, chunk in enumerate(chunks, start=1):
            if isinstance(chunk, dict):
                sections = []
                for p_idx, p in enumerate(chunk.get("paragraphs", [])):
                    if isinstance(p, dict):
                        md = f"## {p.get('title', 'Paragrafo')}\n"
                        if p.get("context"):
                            md += f"[Contesto di Posizionamento: {p['context']}]\n"
                        for pt in p.get("points", []):
                            md += f"- {pt}\n"
                        sections.append((p.get("id", f"p{p_idx}"), md))
                    else:
                        sections.append((f"p{p_idx}", str(p)))
            else:
                raw_sections = split_chapter_by_h2(chunk)
                sections = [(f"p{i}", sec) for i, sec in enumerate(raw_sections)]
                
            chapter_tasks = []
            sub_idx = 0
            for para_id, sec in sections:
                if len(sec) > max_chunk_chars:
                    sub_splits = split_markdown_character_fallback(sec, max_chunk_chars)
                    for ss in sub_splits:
                        chapter_tasks.append((sub_idx, para_id, ss))
                        sub_idx += 1
                else:
                    chapter_tasks.append((sub_idx, para_id, sec))
                    sub_idx += 1
            chapters[idx] = chapter_tasks
        
        total_calls = sum(len(tasks) for tasks in chapters.values())
        _log(f"📚 {original_total} capitoli, {total_calls} sotto-parti totali. Parallelismo iniziale: {INITIAL_PARALLEL}.")

        async with client:
            _log(f"📋 Recupero fonti per il notebook {notebook_id[:8]}...")
            sources = await client.sources.list(notebook_id)
            source_ids = [s.id for s in sources if s.id not in disabled_sources]
            if not source_ids:
                raise ValueError("Nessuna fonte attiva trovata. Assicurati di aver caricato e attivato le fonti.")
            _log(f"📎 {len(source_ids)} fonti attive trovate ({len(sources)-len(source_ids)} disattivate). Avvio generazione...")
            print("=" * 60, flush=True)
            
            completed_count = 0
            errors_total = 0
            active_calls = 0
            cv = asyncio.Condition()
            
            for orig_idx, chapter_tasks in chapters.items():
                halvings = errors_total // HALVE_THRESHOLD
                current_parallel = max(1, INITIAL_PARALLEL >> halvings)
                _log(f"📖 Preparazione Capitolo {orig_idx}/{original_total} — {len(chapter_tasks)} paragrafi...")
                
            async def process_paragraph(sub_idx, para_id, chunk_text, chap_idx, para_total):
                nonlocal completed_count, errors_total, active_calls
                
                async with cv:
                    while True:
                        halvings = errors_total // HALVE_THRESHOLD
                        current_allowed = max(1, INITIAL_PARALLEL >> halvings)
                        if active_calls < current_allowed:
                            active_calls += 1
                            break
                        await cv.wait()
                
                call_label = f"Cap.{chap_idx} §{sub_idx+1}/{para_total}"
                try:
                    for attempt in range(1, 4):
                        try:
                            _log(f"  ⚡ {call_label} — tentativo {attempt}/3 (attivi: {active_calls})")
                            t0 = time.monotonic()
                            final_prompt = (base_prompt
                                .replace("{ruolo}", ruolo)
                                .replace("{materia}", materia)
                                .replace("{indice_corrente}", chunk_text))
                            result = await client.chat.ask(notebook_id, final_prompt, source_ids=source_ids)
                            elapsed = time.monotonic() - t0
                            content = getattr(result, 'answer', getattr(result, 'text', str(result)))
                            if not content or not content.strip():
                                raise ValueError("Risposta vuota")
                            
                            if academic_mode:
                                def replace_citation(match):
                                    text = match.group(0)
                                    nums = re.findall(r'\d+', text)
                                    if not nums: return text
                                    cites = "; ".join(f"@source_{n}" for n in nums)
                                    return f" [{cites}]"
                                content = re.sub(r'(?:\s*\[\d+(?:[,\-\s]+\d+)*\](?:\s*,\s*)?)+', replace_citation, content)
                            else:
                                content = re.sub(r'(\s*\[\d+(?:[,\-\s]+\d+)*\](?:\s*,\s*)?)+', ' ', content)
                                content = re.sub(r'\s+([,.])', r'\1', content)
                            content = re.sub(r' +', ' ', content).strip()
                            
                            is_first = sub_idx == 0
                            cleaned = clean_sub_chunk_output(content, is_first)
                            
                            completed_count += 1
                            _log(f"  ✅ {call_label} OK in {elapsed:.1f}s [{completed_count}/{total_calls}]")
                            return (chap_idx, sub_idx, para_id, cleaned)
                        
                        except (httpx.RemoteProtocolError, httpx.TransportError, httpx.ConnectError, httpx.NetworkError) as e:
                            wait = 20 * attempt
                            _log(f"  🌐 {call_label} ERRORE RETE (tentativo {attempt}/3): {type(e).__name__}: {e}")
                            if attempt < 3:
                                await asyncio.sleep(wait)
                        
                        except Exception as e:
                            wait = 5 * attempt
                            _log(f"  ⚠️  {call_label} ERRORE (tentativo {attempt}/3): {type(e).__name__}: {e}")
                            if attempt < 3:
                                await asyncio.sleep(wait)
                    
                    completed_count += 1
                    async with cv:
                        errors_total += 1
                        if errors_total % HALVE_THRESHOLD == 0:
                            new_parallel = max(1, INITIAL_PARALLEL >> (errors_total // HALVE_THRESHOLD))
                            _log(f"🔻 Concorrenza ridotta a {new_parallel} (totale errori: {errors_total})")
                    
                    _log(f"  ❌ {call_label} FALLITO dopo 3 tentativi → placeholder inserito")
                    return (chap_idx, sub_idx, para_id, f"\n\n---\n\n> ⚠️ **SEZIONE NON GENERATA** — Riprovare la generazione.\n\n---\n\n")
                finally:
                    async with cv:
                        active_calls -= 1
                        cv.notify_all()
            
            all_chapter_tasks = []
            for orig_idx, chapter_tasks in chapters.items():
                para_total = len(chapter_tasks)
                tasks_for_chap = []
                for sub_idx, para_id, text in chapter_tasks:
                    tasks_for_chap.append(process_paragraph(sub_idx, para_id, text, orig_idx, para_total))
                all_chapter_tasks.append((orig_idx, tasks_for_chap))
            
            _log("🚀 Avvio elaborazione asincrona globale su tutti i capitoli...")
            
            async def gather_chapter(chap_idx, tasks):
                res = await asyncio.gather(*tasks)
                res = sorted(res, key=lambda x: x[1])
                full_content = "\n\n".join(t for _, _, _, t in res)
                
                if on_chunk_completed is not None:
                    if asyncio.iscoroutinefunction(on_chunk_completed):
                        await on_chunk_completed(chap_idx, res)
                    else:
                        on_chunk_completed(chap_idx, res)
                        
                _log(f"📗 Capitolo {chap_idx}/{original_total} completato e processato.")
                return chap_idx, full_content
                
            flat_results = await asyncio.gather(*(gather_chapter(idx, tsks) for idx, tsks in all_chapter_tasks))
            
            # Manteniamo comunque compatibilità con chi si aspetta memory_files ritornati alla fine
            for chap_idx, content in flat_results:
                memory_files[f"appunti_p{chap_idx}.md"] = content
            
            total_elapsed = time.monotonic() - gen_start
            print("=" * 60, flush=True)
            if errors_total > 0:
                _log(f"⚠️  Generazione terminata in {total_elapsed:.0f}s con {errors_total} errori.")
            else:
                _log(f"🎉 Generazione completata con successo in {total_elapsed:.0f}s!")
    except Exception as e:
        tb = traceback.format_exc()
        _log(f"💥 Errore fatale: {type(e).__name__}: {e}")
        print(tb, flush=True)
        
    return memory_files
