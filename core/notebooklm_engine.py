import os
import sys
import asyncio
import traceback
import re
import time
import httpx

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
from typing import List, Optional, Dict
from notebooklm import NotebookLMClient
import notebooklm.paths

# Prompt di default per la generazione
PROMPT_GENERAZIONE = r"""Agisci come un {ruolo} esperto di {materia}.
Il tuo compito è generare una dispensa di appunti perfetta, completa ed estremamente dettagliata basandoti rigorosamente ed ESCLUSIVAMENTE sui documenti e file che ti ho fornito.

Di seguito ti fornirò un blocco specifico dell'indice del corso. Voglio che tu analizzi tutti i documenti caricati, estragga e strutturi ogni singola informazione (definizioni, eccezioni, passaggi logici ed esempi). Non devi fare un riassunto, ma una trasposizione completa ed esaustiva.

Segui queste regole tassative per la generazione dell'output:
**Struttura:** Utilizza un'impaginazione gerarchica e pulita. Ogni risposta generata deve iniziare obbligatoriamente con un `##` per il titolo del paragrafo/sezione corrente, e utilizzare `###` o `####` per i sotto-argomenti.
**Regola della lingua:** Tutto l'output testuale deve essere in ITALIANO tecnico e accademico, ma mantieni TASSATIVAMENTE in INGLESE i termini ingegneristici, i nomi dei design pattern e i concetti architetturali (es. non tradurre 'Garbage Collection' o 'Event Loop').
**Esaustività Massima:** Il tuo scopo non è fare un riassunto o una sintesi, ma una trasposizione completa. Se nel testo originale c'è un'analogia, un'osservazione particolare o un'eccezione a una regola, riportala. Mantieni un linguaggio formale e rigoroso, ma chiaro e didattico. 
**Flessibilità Didattica:** Adatta autonomamente la struttura al contenuto. 
   - Se il tema è pratico, usa i blocchi a contrasto (Anti-pattern vs Refactoring).
   - Se il tema è teorico o architetturale, preferisci spiegazioni discorsive, modelli mentali o note di approfondimento.
   - Se il tema è algoritmico o da colloquio, inserisci le sezioni "LeetCode Tip" o "Interview Insight".
   - Se riguarda codice, estrai e includi snippet di CODICE REALE dai documenti sorgente (con Type Hints e Docstrings).

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
    timestamp = time.strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)

async def generation_task(notebook_id: str, chunks: List[str], materia: str, ruolo: str, custom_prompt: str, disabled_sources: List[str] = None) -> Dict[str, str]:
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
        client = await NotebookLMClient.from_storage(official_path, timeout=600)
        _log("✅ Connessione stabilita.")

        template_overhead = len(base_prompt) + len(ruolo) + len(materia)
        max_chunk_chars = 4900 - template_overhead
        if max_chunk_chars < 1000:
            max_chunk_chars = 1000
            
        chapters = {}
        original_total = len(chunks)
        for idx, chunk in enumerate(chunks, start=1):
            sections = split_chapter_by_h2(chunk)
            chapter_tasks = []
            sub_idx = 0
            for sec in sections:
                if len(sec) > max_chunk_chars:
                    sub_splits = split_markdown_character_fallback(sec, max_chunk_chars)
                    for ss in sub_splits:
                        chapter_tasks.append((sub_idx, ss))
                        sub_idx += 1
                else:
                    chapter_tasks.append((sub_idx, sec))
                    sub_idx += 1
            chapters[idx] = chapter_tasks
        
        total_calls = sum(len(tasks) for tasks in chapters.values())
        _log(f"📚 {original_total} capitoli, {total_calls} sotto-parti totali. Parallelismo iniziale: {INITIAL_PARALLEL}.")

        async with client:
            _log(f"📋 Recupero fonti per il notebook {notebook_id[:8]}...")
            sources = await client.sources.list(notebook_id)
            source_ids = [s.id for s in sources if s.id not in disabled_sources]
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
                
            async def process_paragraph(sub_idx, chunk_text, chap_idx, para_total):
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
                            
                            content = re.sub(r'(\s*\[\d+(?:[,\-\s]+\d+)*\](?:\s*,\s*)?)+', ' ', content)
                            content = re.sub(r'\s+([,.])', r'\1', content)
                            content = re.sub(r' +', ' ', content).strip()
                            
                            is_first = sub_idx == 0
                            cleaned = clean_sub_chunk_output(content, is_first)
                            
                            completed_count += 1
                            _log(f"  ✅ {call_label} OK in {elapsed:.1f}s [{completed_count}/{total_calls}]")
                            return (chap_idx, sub_idx, cleaned)
                        
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
                    return (chap_idx, sub_idx, f"\n\n---\n\n> ⚠️ **SEZIONE NON GENERATA** — Riprovare la generazione.\n\n---\n\n")
                finally:
                    async with cv:
                        active_calls -= 1
                        cv.notify_all()
            
            all_tasks = []
            for orig_idx, chapter_tasks in chapters.items():
                para_total = len(chapter_tasks)
                for sub_idx, text in chapter_tasks:
                    all_tasks.append(process_paragraph(sub_idx, text, orig_idx, para_total))
            
            _log("🚀 Avvio elaborazione asincrona globale su tutti i capitoli...")
            flat_results = await asyncio.gather(*all_tasks)
            
            # Ricostruiamo i capitoli raggruppandoli
            grouped = {}
            for chap_idx, sub_idx, test_content in flat_results:
                if chap_idx not in grouped:
                    grouped[chap_idx] = []
                grouped[chap_idx].append((sub_idx, test_content))
                
            for chap_idx, items in grouped.items():
                items.sort(key=lambda x: x[0])
                memory_files[f"appunti_p{chap_idx}.md"] = "\n\n".join(t for _, t in items)
                _log(f"📗 Capitolo {chap_idx}/{original_total} salvato.")
            
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
