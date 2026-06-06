"""
Generation Manager: Orchestrates the generation workflow.
Handles chunk parsing, directory mapping, and disk I/O callbacks.
Extracted from delphi_cli.py to keep the CLI layer thin.
"""
import os
import re
import shutil
import logging
from pathlib import Path
from typing import List, Optional, Callable

logger = logging.getLogger("delphi.generation")


def load_chunks(chunks_file: str, chunks_ids: str = None) -> List:
    """Load and optionally filter chunks from a file (JSON or TXT)."""
    if not chunks_file or not os.path.exists(chunks_file):
        return ["Spiega tutti gli argomenti principali trovati nei documenti."]

    if chunks_file.endswith(".json"):
        import json
        with open(chunks_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        if isinstance(raw_data, dict):
            raw_data = raw_data.get("chapters", [])

        if chunks_ids:
            allowed_ids = [x.strip() for x in chunks_ids.split(",")]
            filtered_data = []
            for chapter in raw_data:
                new_chapter = dict(chapter)
                new_paragraphs = [p for p in chapter.get("paragraphs", []) if p.get("id") in allowed_ids]
                if new_paragraphs:
                    new_chapter["paragraphs"] = new_paragraphs
                    filtered_data.append(new_chapter)
            return filtered_data
        return raw_data
    else:
        with open(chunks_file, "r", encoding="utf-8") as f:
            content = f.read()
        return [c.strip() for c in content.split("\n\n") if c.strip()]


def load_chunks_metadata(chunks_file: str) -> dict:
    """Load metadata (materia, ruolo) from chunks.json if it's an object."""
    if not chunks_file or not os.path.exists(chunks_file) or not chunks_file.endswith(".json"):
        return {}
    import json
    with open(chunks_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    if isinstance(raw_data, dict):
        return {
            "materia": raw_data.get("materia"),
            "ruolo": raw_data.get("ruolo")
        }
    return {}


def prepare_chapter_directories(
    project_dir: Path,
    chunks_data: List,
    chunks_ids: str = None,
    pm=None
) -> tuple:
    """
    Pre-creates chapter directories based on chunk data.
    Returns (chap_map, chap_title_map, chap_info_map).
    """
    if not chunks_ids:
        # Clean old auto-generated chapters if doing a full regeneration
        chapters_dir = project_dir / "chapters"
        if chapters_dir.exists():
            for d in chapters_dir.iterdir():
                if d.is_dir() and re.match(r'^\d+_', d.name):
                    shutil.rmtree(d, ignore_errors=True)

    chap_map = {}
    chap_title_map = {}
    chap_info_map = {}

    for i, chunk_item in enumerate(chunks_data, 1):
        if isinstance(chunk_item, dict):
            real_title = chunk_item.get("title", f"Capitolo {i}")
            folder_name = chunk_item.get("id")
            if not folder_name:
                folder_name = f"{i:02d}_{real_title}"
            safe_folder_name = re.sub(r'[\\/*?:"<>|]', "", folder_name)

            chap_path = project_dir / "chapters" / safe_folder_name
            chap_path.mkdir(parents=True, exist_ok=True)
            chap_map[i] = chap_path
            chap_title_map[i] = real_title
            chap_info_map[i] = chunk_item
        else:
            match = re.search(r'^#\s*(?:Capitolo:?\s*)?(.*)' , chunk_item, re.MULTILINE)
            if match:
                real_title = match.group(1).strip()
            else:
                fallback_match = re.search(r'^\s*#{1,2}\s*(.*)', chunk_item, re.MULTILINE)
                if fallback_match:
                    real_title = fallback_match.group(1).strip()
                else:
                    real_title = f"Capitolo {i}"
            safe_title = re.sub(r'[\\/*?:"<>|]', "", real_title)
            if pm:
                chap_path = pm.add_chapter(project_dir, safe_title)
            else:
                chap_path = project_dir / "chapters" / safe_title
                chap_path.mkdir(parents=True, exist_ok=True)
            chap_map[i] = chap_path
            chap_title_map[i] = real_title
            chap_info_map[i] = None

    return chap_map, chap_title_map, chap_info_map


def make_disk_callback(chap_map: dict, on_save: Callable = None):
    """
    Creates a callback function for generation_task that writes
    results to disk as raw markdown files.
    """
    def chunk_completed_callback(chap_idx, results_list):
        chap_path = chap_map.get(chap_idx)
        if not chap_path:
            return

        for _, _, para_id, fcontent in results_list:
            safe_filename = re.sub(r'[\\/*?:"<>|]', "", str(para_id))
            file_path = chap_path / f"{safe_filename}.md"
            file_path.write_text(fcontent, encoding="utf-8")

            if on_save:
                on_save(chap_path.name, file_path.name)
            else:
                logger.info(f"Salvato Paragrafo in {chap_path.name}/{file_path.name}")

    return chunk_completed_callback
