import os
import shutil
import re
import zipfile
from pathlib import Path
from typing import List, Optional
from .models import Project, Chapter, Paragraph
from .compiler import Compiler
from .citation_service import BibliographyService

import json
from datetime import datetime

import json
from datetime import datetime

def resolve_project_root(anchor_file: Path = None) -> Path:
    """
    Determines the project root.
    If run from within an .agent/skills structure, returns the parent of .agent.
    Otherwise returns CWD.
    """
    if anchor_file is None:
        anchor_file = Path(__file__)
        
    try:
        current = anchor_file.resolve()
        for parent in current.parents:
            if parent.name == '.agent':
                return parent.parent
    except Exception:
        pass
        
    return Path.cwd()

class ProjectManager:
    def __init__(self, root_path: Path):
        self.root_path = Path(root_path).resolve()
        self.compiler = Compiler()
        self.bib_service = BibliographyService()
        self._rag_service = None

    @property
    def rag_service(self):
        if self._rag_service is None:
            from .rag_service import RAGService
            self._rag_service = RAGService()
        return self._rag_service

    @property
    def zotero_service(self):
        if not hasattr(self, '_zotero_service') or self._zotero_service is None:
            from .zotero_service import ZoteroService
            # scripts/lib/project.py -> scripts/lib -> scripts -> delphi-manager
            skill_root = Path(__file__).parent.parent.parent
            self._zotero_service = ZoteroService(skill_root)
        return self._zotero_service

    @property
    def research_service(self):
        if not hasattr(self, '_research_service') or self._research_service is None:
            from .research_service import ResearchService
            self._research_service = ResearchService(self.root_path)
        return self._research_service

    def sync_zotero(self, project_dir: Path) -> dict:
        config = self._load_config(project_dir)
        collection_id = config.get("ZOTERO_COLLECTION_ID")
        
        if not collection_id:
            return {"success": False, "message": "No ZOTERO_COLLECTION_ID found in delphi.json"}
            
        # 1. Sync Bibliography
        bib_path = project_dir / "references.bib"
        if not self.zotero_service.sync_bibliography(collection_id, bib_path):
             return {"success": False, "message": "Failed to sync bibliography from Zotero."}
             
        # Reload bib service
        self.bib_service.load_bibliography(bib_path)

        # 2. Sync Attachments
        zotero_files_dir = project_dir / "assets" / "research" / "zotero"
        downloaded = self.zotero_service.download_attachments(collection_id, zotero_files_dir)
        
        # 3. Update RAG (Incremental)
        # We scan the whole dir to catching anything new/modified
        # rag_service.sync_research handles logic.
        if zotero_files_dir.exists():
            files = list(zotero_files_dir.glob("*.pdf")) # Support other types?
            # Also text files? self.zotero_service only downloads PDFs currently.
            pass
            
        # We need to get ALL files in that dir to sync properly (in case we deleted some? RAG usually additive only with my implementation)
        # Actually my incremental implementation handles new/modified, but doesn't handle deletions.
        # MVP: additive is fine.
        
        files = []
        if zotero_files_dir.exists():
             files.extend(list(zotero_files_dir.glob("*.pdf")))
        
        if files:
            self.rag_service.sync_research(project_dir, files)
            
        return {
            "success": True, 
            "message": f"Synced Zotero collection {collection_id}. Updated references.bib and processed {len(files)} research files."
        }

    def _load_config(self, project_dir: Path) -> dict:
        config_path = project_dir / "delphi.json"
        
        # Default compilation settings (match current hardcoded behavior)
        default_compilation = {
            "pandoc_extensions": "+tex_math_dollars",
            "shift_heading_level": 1,
            "page_break_before_chapter": True,
            "typst_template": "default_thesis",
            "heading_numbering": "none"
        }
        
        if not config_path.exists():
            return {
                "metadata": {
                    "title": project_dir.name,
                    "author": "Anonymous", 
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "version": "1.0.0"
                },
                "order": [],
                "compilation": default_compilation
            }
        
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            # Ensure compilation section exists with defaults
            if "compilation" not in config:
                config["compilation"] = default_compilation
            else:
                # Merge with defaults for any missing keys
                for key, value in default_compilation.items():
                    if key not in config["compilation"]:
                        config["compilation"][key] = value
            return config
        except:
             return {"metadata": {}, "order": [], "compilation": default_compilation}

    def _save_config(self, project_dir: Path, config: dict):
        config_path = project_dir / "delphi.json"
        config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

    def init_project(self, name: str) -> Path:
        """Creates a new project structure."""
        if name == ".":
            project_dir = self.root_path
            # Use current folder name as project title if none provided
            name = self.root_path.name
        else:
            project_dir = self.root_path / name
        
        # Check if config already exists to avoid overwriting existing projects
        if (project_dir / "delphi.json").exists():
            raise FileExistsError(f"A Delphi project already exists at {project_dir}")
            
        project_dir.mkdir(parents=True, exist_ok=True)
        (project_dir / "assets").mkdir(exist_ok=True)
        (project_dir / "chapters").mkdir(exist_ok=True)
        (project_dir / "output").mkdir(exist_ok=True)
        
        bib_file = project_dir / "references.bib"
        if not bib_file.exists():
            bib_file.touch()
            
        readme_file = project_dir / "README.md"
        if not readme_file.exists():
            readme_file.write_text(f"# {name}\n\nProject initialized.", encoding="utf-8")
        
        # Init Config
        config = {
            "metadata": {
                "title": name,
                "author": "Author Name",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "version": "0.1.0"
            },
            "order": []
        }
        self._save_config(project_dir, config)
        return project_dir



    def load_project(self, project_dir: Path) -> Project:
        """Scans the folder structure to build the Project object."""
        project_dir = Path(project_dir).resolve()
        if not project_dir.exists():
            raise FileNotFoundError(f"Project not found: {project_dir}")

        name = project_dir.name
        chapters = []
        ignored = {'.', 'assets', '.build', '__pycache__'}
        
        chapters_dir = project_dir / "chapters"
        if chapters_dir.exists():
            for item in sorted(chapters_dir.iterdir()):
                if item.is_dir() and not item.name.startswith('.') and item.name not in ignored:
                    paragraphs = []
                    for f in sorted(item.glob("*.md")):
                        content = f.read_text(encoding="utf-8")
                        paragraphs.append(Paragraph(path=f, title=f.stem, content=content))
                    
                    chapters.append(Chapter(path=item, title=item.name, paragraphs=paragraphs))

        project = Project(path=project_dir, name=name, chapters=chapters)
        bib_path = project_dir / "references.bib"
        self.bib_service.load_bibliography(bib_path)
        return project

    def add_chapter(self, project_dir: Path, title: str) -> Path:
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).strip()
        chapters_dir = project_dir / "chapters"
        chapters_dir.mkdir(exist_ok=True)
        existing_chapters = [x for x in chapters_dir.iterdir() if x.is_dir() and not x.name.startswith('.')]
        next_idx = len(existing_chapters) + 1
        prefix = f"{next_idx:02d}_"
        folder_name = f"{prefix}{safe_title}"
        chapter_path = chapters_dir / folder_name
        
        if chapter_path.exists():
             raise FileExistsError(f"Chapter '{folder_name}' already exists.")
        chapter_path.mkdir()
        
        # Update config
        config = self._load_config(project_dir)
        config["order"].append(folder_name)
        self._save_config(project_dir, config)
        
        return chapter_path

    def add_paragraph(self, chapter_path: Path, title: str, content: str = "", include_header: bool = True) -> Path:
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).strip()
        existing_paras = list(chapter_path.glob("*.md"))
        next_idx = len(existing_paras) + 1
        prefix = f"{next_idx:02d}_"
        filename = f"{prefix}{safe_title}.md"
        file_path = chapter_path / filename
        
        if include_header:
            full_content = f"## {title}\n\n{content}"
        else:
            full_content = content
            
        file_path.write_text(full_content, encoding="utf-8")
        return file_path

    def insert_paragraph(self, project_dir: Path, chapter_id: str, title: str, 
                         content: str = "", after_para_id: str = None, 
                         include_header: bool = True) -> Path:
        """
        Inserts a paragraph at a specific position in a chapter.
        
        Args:
            project_dir: Project directory
            chapter_id: Chapter identifier (index, partial name, or exact)
            title: Title for the new paragraph
            content: Markdown content
            after_para_id: Insert after this paragraph (if None, inserts at beginning)
            include_header: Whether to add ## header
            
        Returns:
            Path to the created file
        """
        chapter = self.resolve_chapter(project_dir, chapter_id)
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).strip()
        
        # Determine insertion index
        if after_para_id is None:
            # Insert at the beginning (index 1)
            insert_idx = 1
        else:
            # Find the paragraph to insert after
            after_para = self.resolve_paragraph(chapter, after_para_id)
            # Extract current index from filename
            import re
            match = re.match(r'^(\d+)', after_para.path.stem)
            if match:
                insert_idx = int(match.group(1)) + 1
            else:
                # Fallback: insert at end
                insert_idx = len(chapter.paragraphs) + 1
        
        # Get all existing paragraphs sorted
        existing_paras = sorted(chapter.path.glob("*.md"), key=lambda x: x.name)
        
        # Renumber paragraphs that come after the insertion point
        # We need to rename them in reverse order to avoid conflicts
        paras_to_shift = []
        for para_path in existing_paras:
            match = re.match(r'^(\d+)', para_path.stem)
            if match:
                current_idx = int(match.group(1))
                if current_idx >= insert_idx:
                    paras_to_shift.append((para_path, current_idx))
        
        # Sort by index descending to rename from highest to lowest
        paras_to_shift.sort(key=lambda x: x[1], reverse=True)
        
        for para_path, current_idx in paras_to_shift:
            new_idx = current_idx + 1
            # Extract base name without prefix
            name_match = re.match(r'^\d+[_ ]+(.+)$', para_path.stem)
            if name_match:
                base_name = name_match.group(1)
            else:
                base_name = para_path.stem
            
            new_name = f"{new_idx:02d}_{base_name}.md"
            new_path = para_path.parent / new_name
            para_path.rename(new_path)
        
        # Create the new paragraph at the insertion position
        filename = f"{insert_idx:02d}_{safe_title}.md"
        file_path = chapter.path / filename
        
        if include_header:
            full_content = f"## {title}\n\n{content}"
        else:
            full_content = content
        
        file_path.write_text(full_content, encoding="utf-8")
        return file_path

    def get_structure_tree(self, project_dir: Path) -> str:
        project = self.load_project(project_dir)
        tree = f"Project: {project.name}\n"
        for chapter in project.chapters:
            tree += f"  ├── 📁 {chapter.title}\n"
            for p in chapter.paragraphs:
                tree += f"  │   ├── 📄 {p.path.name}\n"
        return tree

    def compile_project(self, project_dir: Path) -> Path:
        project = self.load_project(project_dir)
        return self.compiler.compile(project)

    def add_citation(self, project_dir: Path, bibtex: str):
        self.load_project(project_dir)
        self.bib_service.add_reference(bibtex)
            
    def search_bibliography(self, project_dir: Path, query: str) -> List[dict]:
        self.load_project(project_dir)
        return self.bib_service.search(query)

    def add_asset(self, project_dir: Path, source_path: Path) -> str:
        assets_dir = project_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Asset source {source} not found.")
        dest = assets_dir / source.name
        if dest.exists():
            base = dest.stem
            ext = dest.suffix
            c = 1
            while dest.exists():
                dest = assets_dir / f"{base}_{c}{ext}"
                c += 1
        shutil.copy2(source, dest)
        return f"assets/{dest.name}"

    def export_project(self, project_dir: Path, output_zip: Path):
        """Zips the project directory."""
        if not project_dir.exists():
            raise FileNotFoundError("Project directory not found")
        
        if output_zip.suffix != '.zip':
            output_zip = output_zip.with_suffix('.zip')
            
        # shutil.make_archive expects base_name without extension
        base = str(output_zip).replace(".zip", "")
        shutil.make_archive(base, 'zip', root_dir=project_dir.parent, base_dir=project_dir.name)
        return output_zip

    def import_project(self, zip_path: Path) -> Path:
        """Unzips a project into the root path."""
        if not zip_path.exists():
            raise FileNotFoundError("Zip file not found")
            
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Check content
            first = zf.infolist()[0].filename
            is_folder_packed = '/' in first 
            
            if is_folder_packed:
                # Extract as is
                zf.extractall(self.root_path)
                extracted_name = first.split('/')[0]
                return self.root_path / extracted_name
            else:
                # Contents packed at root. Create folder.
                name = zip_path.stem
                target = self.root_path / name
                target.mkdir(exist_ok=True)
                zf.extractall(target)
    def validate_structure(self, project_dir: Path, fix: bool = False) -> List[str]:
        """Checks for structural integrity issues and optionally fixes them."""
        issues = []
        config = self._load_config(project_dir)
        original_order = config.get("order", [])
        
        # 1. Check if all chapters in config exist
        missing_chapters = []
        chapters_dir = project_dir / "chapters"
        for chap_name in original_order:
            if not (chapters_dir / chap_name).exists():
                msg = f"MISSING_CHAPTER: '{chap_name}' listed in config but not found on disk."
                issues.append(msg)
                missing_chapters.append(chap_name)
        
        if fix and missing_chapters:
            # Remove missing chapters from config
            config["order"] = [c for c in config["order"] if c not in missing_chapters]
            issues.append(f"FIXED: Removed {len(missing_chapters)} missing chapters from config.")

        # 2. Check for unlisted chapters
        ignored = {'.', 'assets', '.build', '__pycache__', 'references.bib', 'README.md', 'delphi.json'}
        orphan_chapters = []
        if chapters_dir.exists():
            for item in chapters_dir.iterdir():
                if item.is_dir() and item.name not in ignored and not item.name.startswith('.'):
                     if item.name not in original_order:
                      msg = f"ORPHAN_CHAPTER: '{item.name}' exists but is not in delphi.json order."
                      issues.append(msg)
                      orphan_chapters.append(item.name)
        
        if fix and orphan_chapters:
            # Add orphans to the end of config
            # Try to sort them by name/number if possible
            orphan_chapters.sort()
            config["order"].extend(orphan_chapters)
            issues.append(f"FIXED: Added {len(orphan_chapters)} orphan chapters to config.")

        # 3. Check for missing compilation config (migration)
        config_path = project_dir / "delphi.json"
        if fix and config_path.exists():
            raw_config = json.loads(config_path.read_text(encoding="utf-8"))
            if "compilation" not in raw_config:
                issues.append("FIXED: Added missing 'compilation' section with defaults.")
                # The merged config already has compilation from _load_config
            
        if fix and (missing_chapters or orphan_chapters or "compilation" not in json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else False):
            self._save_config(project_dir, config)
        
        return issues

    def validate_citations(self, project_dir: Path) -> List[str]:
        """Checks if citations used in the text exist in the bibliography."""
        project = self.load_project(project_dir)
        # Ensure bibliography is loaded
        # bib_service was loaded in load_project called above.
        
        valid_keys = set(self.bib_service.get_citation_keys()) # "@key" format
        
        issues = []
        citation_pattern = re.compile(r"\[@([a-zA-Z0-9_\-:]+)\]")
        
        for chapter in project.chapters:
            for para in chapter.paragraphs:
                # Find all citations
                # Text usually matches [@key] or [@key; @key2]
                # Regex needs to handle multiple or single basic ones first.
                # Pandoc citation syntax is complex, but let's target specific simple cases [@key].
                
                # A more robust regex might be needed for complexity, but for MVP:
                # We search for string starting with @ inside []
                
                # Let's verify our regex
                # r"\[@([a-zA-Z0-9_\-:]+)\]" captures simple keys.
                # Does not capture multiple citations like [@a; @b].
                # User's example `check_citations` usage suggests checking "hallucinated" ones.
                
                # Let's scan for anything looking like a citation key.
                matches = citation_pattern.findall(para.content)
                for key in matches:
                    full_key = f"@{key}"
                    if full_key not in valid_keys:
                        issues.append(f"MISSING_SOURCE: Citation '{full_key}' in '{para.title}' (Chapter: {chapter.title}) not found in bibliography.")
                        
        return issues

    # ========== FUZZY RESOLUTION ==========
    
    def resolve_chapter(self, project_dir: Path, id_or_name: str) -> 'Chapter':
        """
        Resolves a chapter by index (1-based), partial name, or exact folder name.
        Returns the Chapter object or raises ValueError if not found or ambiguous.
        """
        project = self.load_project(project_dir)
        
        # Try index first (e.g., "2" or 2)
        try:
            idx = int(id_or_name)
            if 1 <= idx <= len(project.chapters):
                return project.chapters[idx - 1]
            raise ValueError(f"Chapter index {idx} out of range (1-{len(project.chapters)})")
        except ValueError as e:
            if "out of range" in str(e):
                raise
            # Not an integer, continue to name matching
            pass
        
        # Normalize search term
        search_term = id_or_name.lower().strip()
        
        # Try exact match first
        for chapter in project.chapters:
            if chapter.title.lower() == search_term or chapter.path.name.lower() == search_term:
                return chapter
        
        # Try partial match
        matches = []
        for chapter in project.chapters:
            if search_term in chapter.title.lower() or search_term in chapter.path.name.lower():
                matches.append(chapter)
        
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            match_names = [c.path.name for c in matches]
            raise ValueError(f"Ambiguous chapter match for '{id_or_name}'. Matches: {match_names}")
        
        raise ValueError(f"Chapter '{id_or_name}' not found.")

    def resolve_paragraph(self, chapter: 'Chapter', id_or_name: str) -> 'Paragraph':
        """
        Resolves a paragraph within a chapter by index (1-based), partial name, or exact filename.
        Returns the Paragraph object or raises ValueError if not found or ambiguous.
        """
        # Try index first
        try:
            idx = int(id_or_name)
            if 1 <= idx <= len(chapter.paragraphs):
                return chapter.paragraphs[idx - 1]
            raise ValueError(f"Paragraph index {idx} out of range (1-{len(chapter.paragraphs)})")
        except ValueError as e:
            if "out of range" in str(e):
                raise
            pass
        
        search_term = id_or_name.lower().strip()
        
        # Try exact match
        for para in chapter.paragraphs:
            if para.title.lower() == search_term or para.path.name.lower() == search_term:
                return para
        
        # Try partial match
        matches = []
        for para in chapter.paragraphs:
            if search_term in para.title.lower() or search_term in para.path.name.lower():
                matches.append(para)
        
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            match_names = [p.path.name for p in matches]
            raise ValueError(f"Ambiguous paragraph match for '{id_or_name}'. Matches: {match_names}")
        
        raise ValueError(f"Paragraph '{id_or_name}' not found in chapter '{chapter.title}'.")

    # ========== READ OPERATIONS ==========
    
    def read_chapter(self, project_dir: Path, chapter_id: str) -> dict:
        """
        Returns the combined Markdown content of a chapter.
        """
        chapter = self.resolve_chapter(project_dir, chapter_id)
        
        content_parts = []
        for para in chapter.paragraphs:
            content_parts.append(para.content)
        
        combined = "\n\n".join(content_parts)
        
        return {
            "chapter_title": chapter.title,
            "chapter_path": str(chapter.path),
            "paragraph_count": len(chapter.paragraphs),
            "content": combined
        }

    def read_paragraph(self, project_dir: Path, chapter_id: str, para_id: str) -> dict:
        """
        Returns the content of a specific paragraph.
        """
        chapter = self.resolve_chapter(project_dir, chapter_id)
        para = self.resolve_paragraph(chapter, para_id)
        
        return {
            "paragraph_title": para.title,
            "paragraph_path": str(para.path),
            "chapter_title": chapter.title,
            "content": para.content
        }

    # ========== HELPER: RENUMBER PARAGRAPHS ==========
    
    def _renumber_paragraphs(self, chapter_path: Path):
        """
        Renumbers all paragraph files in a chapter to maintain sequential ordering.
        """
        paragraphs = sorted(chapter_path.glob("*.md"), key=lambda x: x.name)
        
        for idx, para_path in enumerate(paragraphs, start=1):
            # Extract current name without prefix
            import re
            name_match = re.match(r'^\d+[_ ]+(.+)$', para_path.stem)
            if name_match:
                base_name = name_match.group(1)
            else:
                base_name = para_path.stem
            
            new_name = f"{idx:02d}_{base_name}.md"
            new_path = chapter_path / new_name
            
            if para_path != new_path:
                para_path.rename(new_path)

    # ========== MERGE OPERATION ==========
    
    def merge_paragraphs(self, project_dir: Path, chapter_id: str, 
                         para_a_id: str, para_b_id: str, 
                         new_title: str, keep_originals: bool = False) -> Path:
        """
        Merges two paragraphs into a new file with combined content.
        By default, deletes the original files and renumbers remaining paragraphs.
        """
        chapter = self.resolve_chapter(project_dir, chapter_id)
        para_a = self.resolve_paragraph(chapter, para_a_id)
        para_b = self.resolve_paragraph(chapter, para_b_id)
        
        # Combine content (A then B)
        combined_content = f"## {new_title}\n\n{para_a.content}\n\n{para_b.content}"
        
        # Create new file with next available index
        safe_title = "".join([c for c in new_title if c.isalnum() or c in (' ', '_', '-')]).strip()
        
        if keep_originals:
            # Add at end
            existing_paras = list(chapter.path.glob("*.md"))
            next_idx = len(existing_paras) + 1
        else:
            # Will take the place of first deleted paragraph
            next_idx = 1
        
        new_filename = f"{next_idx:02d}_{safe_title}.md"
        new_path = chapter.path / new_filename
        new_path.write_text(combined_content, encoding="utf-8")
        
        if not keep_originals:
            # Delete originals
            para_a.path.unlink()
            para_b.path.unlink()
            # Renumber remaining
            self._renumber_paragraphs(chapter.path)
        
        return new_path

    # ========== MOVE OPERATION ==========
    
    def move_paragraph(self, project_dir: Path, para_id: str, 
                       from_chapter_id: str, to_chapter_id: str) -> Path:
        """
        Moves a paragraph from one chapter to another.
        Renumbers both source and target chapters.
        """
        from_chapter = self.resolve_chapter(project_dir, from_chapter_id)
        to_chapter = self.resolve_chapter(project_dir, to_chapter_id)
        para = self.resolve_paragraph(from_chapter, para_id)
        
        # Determine new index in target chapter
        existing_in_target = list(to_chapter.path.glob("*.md"))
        next_idx = len(existing_in_target) + 1
        
        # Extract base name without prefix
        import re
        name_match = re.match(r'^\d+[_ ]+(.+)$', para.path.stem)
        if name_match:
            base_name = name_match.group(1)
        else:
            base_name = para.path.stem
        
        new_filename = f"{next_idx:02d}_{base_name}.md"
        new_path = to_chapter.path / new_filename
        
        # Move file
        shutil.move(str(para.path), str(new_path))
        
        # Renumber source chapter
        self._renumber_paragraphs(from_chapter.path)
        
        return new_path

    # ========== RENAME OPERATIONS ==========
    
    def rename_chapter(self, project_dir: Path, old_id: str, new_name: str) -> Path:
        """
        Renames a chapter folder and updates delphi.json.
        Preserves the numeric prefix.
        """
        chapter = self.resolve_chapter(project_dir, old_id)
        old_folder_name = chapter.path.name
        
        # Extract prefix
        import re
        prefix_match = re.match(r'^(\d+[_ ]+)', old_folder_name)
        if prefix_match:
            prefix = prefix_match.group(1)
        else:
            prefix = ""
        
        # Create new folder name
        safe_name = "".join([c for c in new_name if c.isalnum() or c in (' ', '_', '-')]).strip()
        new_folder_name = f"{prefix}{safe_name}"
        new_path = chapter.path.parent / new_folder_name
        
        # Rename on disk
        chapter.path.rename(new_path)
        
        # Update config
        config = self._load_config(project_dir)
        if old_folder_name in config.get("order", []):
            config["order"] = [new_folder_name if x == old_folder_name else x for x in config["order"]]
            self._save_config(project_dir, config)
        
        return new_path

    def rename_paragraph(self, project_dir: Path, chapter_id: str, 
                         old_para_id: str, new_name: str) -> Path:
        """
        Renames a paragraph file, preserving the numeric prefix.
        """
        chapter = self.resolve_chapter(project_dir, chapter_id)
        para = self.resolve_paragraph(chapter, old_para_id)
        
        # Extract prefix
        import re
        prefix_match = re.match(r'^(\d+[_ ]+)', para.path.stem)
        if prefix_match:
            prefix = prefix_match.group(1)
        else:
            prefix = ""
        
        safe_name = "".join([c for c in new_name if c.isalnum() or c in (' ', '_', '-')]).strip()
        new_filename = f"{prefix}{safe_name}.md"
        new_path = para.path.parent / new_filename
        
        # Rename
        para.path.rename(new_path)
        
        return new_path

    # ========== DELETE OPERATIONS ==========
    
    def delete_chapter(self, project_dir: Path, chapter_id: str, force: bool = False) -> str:
        """
        Deletes a chapter folder and updates delphi.json.
        Requires force=True due to destructive nature.
        """
        if not force:
            raise ValueError("Deleting a chapter requires --force flag (destructive operation)")
        
        chapter = self.resolve_chapter(project_dir, chapter_id)
        folder_name = chapter.path.name
        
        # Delete folder and contents
        shutil.rmtree(chapter.path)
        
        # Update config
        config = self._load_config(project_dir)
        if folder_name in config.get("order", []):
            config["order"] = [x for x in config["order"] if x != folder_name]
            self._save_config(project_dir, config)
        
        return folder_name

    def delete_paragraph(self, project_dir: Path, chapter_id: str, para_id: str) -> str:
        """
        Deletes a paragraph file and renumbers remaining paragraphs.
        """
        chapter = self.resolve_chapter(project_dir, chapter_id)
        para = self.resolve_paragraph(chapter, para_id)
        
        para_name = para.path.name
        para.path.unlink()
        
        # Renumber remaining
        self._renumber_paragraphs(chapter.path)
        
        return para_name

