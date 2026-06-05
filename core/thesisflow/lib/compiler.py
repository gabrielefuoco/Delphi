from pathlib import Path
from typing import List, Dict, Set, Tuple
import re
import logging

from .pandoc_wrapper import PandocWrapper
from .typst_wrapper import TypstWrapper
from .models import Project
from .paths import get_templates_dir

# Configure module logger
logger = logging.getLogger(__name__)


class Compiler:
    """
    Compiles ThesisFlow projects to PDF (via Typst) or DOCX (via Pandoc).
    
    Handles:
    - Markdown to Typst conversion
    - Asset path normalization
    - Deprecated symbol replacement
    - Configurable heading numbering
    """
    
    # Extensible mapping of deprecated Typst symbols to their replacements
    # Add new entries here when Typst deprecates more symbols
    DEPRECATED_SYMBOLS: Dict[str, str] = {
        # Typst 0.14+ deprecations
        'sect': 'inter',           # Intersection symbol
        'sect.sq': 'inter.sq',     # Square intersection
        'angle.l': 'chevron.l',    # Left angle bracket
        'angle.r': 'chevron.r',    # Right angle bracket
        'angle.l.double': 'guillemet.l',
        'angle.r.double': 'guillemet.r',
    }
    
    # Image path patterns to normalize
    IMAGE_PATH_PATTERNS: List[Tuple[str, str]] = [
        (r'\]\(@/', r'](../assets/'),           # @/ convention
        (r'\]\(assets/', r'](../assets/'),       # assets/ prefix
        (r'\]\(\./assets/', r'](../assets/'),    # ./assets/ prefix
    ]
    
    def __init__(self):
        self.pandoc = PandocWrapper()
        self.typst = TypstWrapper()
        
    def _read_template(self, template_name: str = "default_thesis") -> str:
        # Sanity check: prevent path traversal
        safe_name = Path(template_name).stem
        tpl_path = get_templates_dir() / f"{safe_name}.typ"
        if not tpl_path.exists():
            # Fallback
            tpl_path = get_templates_dir() / "default_thesis.typ"
            
        if tpl_path.exists():
            return tpl_path.read_text(encoding="utf-8")
        return "" # Fallback or error

    @staticmethod
    def typst_escape(text: str) -> str:
        """Escapes characters that break Typst string syntax."""
        if not text: return ""
        # Typst strings are double quoted. 
        # Escape backslashes first, then quotes.
        return str(text).replace("\\", "\\\\").replace('"', '\\"')

    def _get_template_header(self, project: Project) -> str:
        # Load logic
        import json
        meta = {
             "title": project.name,
             "author": "Author",
             "date": "2024",
             "version": "1.0",
             "template": "default_thesis" 
        }
        try:
             cfg = json.loads((project.path / "thesisflow.json").read_text(encoding="utf-8"))
             meta.update(cfg.get("metadata", {}))
             meta.update(cfg.get("compilation", {}))
        except: pass
        
        tpl_name = meta.get("template", "default_thesis")
        # Load external template
        content = self._read_template(tpl_name)
        
        # Escape metadata values
        e_title = self.typst_escape(meta['title'])
        e_author = self.typst_escape(meta['author'])
        e_date = self.typst_escape(meta['date'])
        e_version = self.typst_escape(meta['version'])
        
        e_university = self.typst_escape(meta.get('university', ''))
        e_department = self.typst_escape(meta.get('department', ''))
        e_degree = self.typst_escape(meta.get('degree', ''))
        e_supervisor = self.typst_escape(meta.get('supervisor', ''))
        e_academic_year = self.typst_escape(meta.get('academic_year', ''))
        e_logo = self.typst_escape(meta.get('logo', ''))
        
        e_degree_label = self.typst_escape(meta.get('degree_label', 'Corso di laurea magistrale in'))
        e_academic_year_label = self.typst_escape(meta.get('academic_year_label', 'Anno Accademico'))
        
        # Determine if logo is a Typst literal (none) or a string
        logo_val = f'"{e_logo}"' if e_logo else "none"

        # Boolean parameters should be passed as lowercase string for Typst bool
        numbered_chapters = str(meta.get('numbered_chapters', True)).lower()
        heading_numbering = meta.get('heading_numbering', 'none')
        if heading_numbering is None or heading_numbering == 'none':
            heading_numbering_val = "none"
        else:
            heading_numbering_val = f'"{self.typst_escape(heading_numbering)}"'

        header = f"""
#import "master_template.typ": project

#show: project.with(
  title: "{e_title}",
  author: "{e_author}",
  university: "{e_university}",
  department: "{e_department}",
  degree: "{e_degree}",
  supervisor: "{e_supervisor}",
  academic_year: "{e_academic_year}",
  degree_label: "{e_degree_label}",
  academic_year_label: "{e_academic_year_label}",
  logo_path: {logo_val},
  numbered_chapters: {numbered_chapters},
  heading_numbering: {heading_numbering_val},
  date: "{e_date}",
  version: "{e_version}",
)
"""
        return header

    def _fix_deprecated_symbols(self, build_dir: Path) -> int:
        """
        Post-processes all .typ files in build_dir to replace deprecated symbols.
        Uses the class-level DEPRECATED_SYMBOLS mapping for extensibility.
        
        Returns:
            Number of files modified.
        """
        modified_count = 0
        
        for typ_file in build_dir.rglob('*.typ'):
            try:
                content = typ_file.read_text(encoding='utf-8')
                original_content = content
                
                for old_symbol, new_symbol in self.DEPRECATED_SYMBOLS.items():
                    if old_symbol in content:
                        content = content.replace(old_symbol, new_symbol)
                
                if content != original_content:
                    typ_file.write_text(content, encoding='utf-8')
                    modified_count += 1
                    logger.debug(f"Fixed deprecated symbols in: {typ_file.name}")
                    
            except Exception as e:
                logger.warning(f"Could not fix symbols in {typ_file}: {e}")
        
        if modified_count > 0:
            logger.info(f"Fixed deprecated symbols in {modified_count} file(s)")
        
        return modified_count


    def _parse_bib_authors(self, bib_path: Path) -> dict:
        """
        Parses a .bib file and extracts the first author's surname for each entry.
        Returns a dict: {citekey: "Surname"}.
        """
        authors = {}
        if not bib_path.exists():
            return authors
        
        content = bib_path.read_text(encoding="utf-8", errors="replace")
        
        # Split by entries
        entries = re.split(r'(?=@\w+\{)', content)
        entry_pattern = re.compile(r'@\w+\{([^,]+),', re.MULTILINE)
        author_pattern = re.compile(r'author\s*=\s*\{([^}]+)\}', re.IGNORECASE)
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            key_match = entry_pattern.search(entry)
            if not key_match:
                continue
            citekey = key_match.group(1).strip()
            
            auth_match = author_pattern.search(entry)
            if not auth_match:
                continue
            
            raw_authors = auth_match.group(1).strip()
            author_list = raw_authors.split(" and ")
            first_author = author_list[0].strip()
            
            if "," in first_author:
                surname = first_author.split(",")[0].strip()
            else:
                parts = first_author.split()
                surname = parts[-1].strip() if parts else first_author
            
            # Clean LaTeX escapes
            surname = re.sub(r"[{}\\'`\"~^]", "", surname)
            
            # Add "et al." if multiple authors
            if len(author_list) > 1:
                surname = f"{surname} et al."
            
            authors[citekey] = surname
        
        return authors

    def _preprocess_narrative_citations(self, content: str, bib_path: Path) -> str:
        """
        Replaces bare narrative citations (@citekey) with 'Surname [-@citekey]'
        so that numeric CSL styles (IEEE) render 'Surname [N]' instead of just '[N]'.
        
        Uses a robust shielding technique to prevent corrupting markdown links,
        images, and parenthetical citation blocks.
        """
        authors = self._parse_bib_authors(bib_path)
        
        if not authors:
            return content
        
        # Step 1: Protect all content inside brackets [...] and parentheses (...)
        placeholders = {}
        counter = [0]
        
        def protect(match):
            key = f"__PROTECTED_CITE_{counter[0]}__"
            placeholders[key] = match.group(0)
            counter[0] += 1
            return key
        
        protected = re.sub(r'\[[^\]]*\]', protect, content)
        protected = re.sub(r'\([^\)]*\)', protect, protected)
        
        # Step 2: Replace bare @citekey with Surname [-@citekey]
        def replace_narrative(match):
            citekey = match.group(1)
            if citekey in authors:
                surname = authors[citekey]
                return f"{surname} [-@{citekey}]"
            else:
                return match.group(0)
        
        bare_pattern = re.compile(r'(?<!-)(?<!\w)@([a-zA-Z][\w:-]*)')
        result = bare_pattern.sub(replace_narrative, protected)
        
        # Step 3: Restore protected content
        for key, original in reversed(list(placeholders.items())):
            result = result.replace(key, original)
        
        return result

    def _normalize_image_paths(self, content: str) -> str:
        """
        Normalizes image paths in markdown content to be relative to the build directory.
        Handles multiple path formats: @/, assets/, ./assets/
        
        Args:
            content: Markdown content with image references.
            
        Returns:
            Content with normalized image paths.
        """
        for pattern, replacement in self.IMAGE_PATH_PATTERNS:
            content = re.sub(pattern, replacement, content)
        return content

    def _validate_assets(self, project: Project) -> List[Dict[str, str]]:
        """
        Validates that all referenced images exist in the project assets.
        
        Args:
            project: The project to validate.
            
        Returns:
            List of dictionaries with 'file', 'line', and 'path' for missing assets.
        """
        missing = []
        assets_dir = project.path / "assets"
        
        # Pattern to match markdown images: ![alt](path)
        image_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
        
        for chapter in project.chapters:
            for paragraph in chapter.paragraphs:
                for line_num, line in enumerate(paragraph.content.split('\n'), 1):
                    for match in image_pattern.finditer(line):
                        img_path = match.group(2)
                        
                        # Skip external URLs
                        if img_path.startswith(('http://', 'https://', '//')):
                            continue
                        
                        # Normalize path
                        clean_path = img_path.replace('@/', '').replace('../assets/', '').replace('assets/', '')
                        
                        # Check if file exists
                        full_path = assets_dir / clean_path
                        if not full_path.exists():
                            # Try in images subdirectory
                            alt_path = assets_dir / "images" / Path(clean_path).name
                            if not alt_path.exists():
                                missing.append({
                                    'file': str(paragraph.path.relative_to(project.path)),
                                    'line': line_num,
                                    'path': img_path
                                })
        
        if missing:
            logger.warning(f"Found {len(missing)} missing asset(s)")
            for m in missing:
                logger.debug(f"  Missing: {m['path']} (in {m['file']}:{m['line']})")
        
        return missing

    def compile(self, project: Project, output_path: Path = None):
        """
        Compiles the project to PDF.
        """
        logger.info(f"Starting compilation for: {project.name}")
        
        build_dir = project.path / ".build"
        build_dir.mkdir(exist_ok=True)
        
        # Load full config
        import json
        cfg = {}
        tpl_name = "default_thesis"
        compilation_config = {
            "pandoc_extensions": "+tex_math_dollars",
            "page_break_before_chapter": True,
            "validate_assets": True,  # Enable asset validation by default
            "strict_asset_validation": False  # If True, fail on missing assets
        }
        try:
             cfg = json.loads((project.path / "thesisflow.json").read_text(encoding="utf-8"))
             tpl_name = cfg.get("metadata", {}).get("template", "default_thesis")
             # Override defaults with config values
             if "compilation" in cfg:
                 compilation_config.update(cfg["compilation"])
        except: pass

        pandoc_extensions = compilation_config.get("pandoc_extensions", "+tex_math_dollars")
        page_break = compilation_config.get("page_break_before_chapter", True)
        
        # Optional asset validation
        if compilation_config.get("validate_assets", True):
            missing_assets = self._validate_assets(project)
            if missing_assets and compilation_config.get("strict_asset_validation", False):
                raise ValueError(f"Compilation aborted: {len(missing_assets)} missing asset(s) found. "
                                 "Set 'strict_asset_validation': false in thesisflow.json to proceed.")

        # 1. Copy template to build dir
        safe_name = Path(tpl_name).stem
        tpl_src = get_templates_dir() / f"{safe_name}.typ"
        if not tpl_src.exists(): tpl_src = get_templates_dir() / "default_thesis.typ"
        
        if tpl_src.exists():
             import shutil
             shutil.copy2(tpl_src, build_dir / "master_template.typ")
             
        # 1.1 Copy title_page.typ if it exists (for default_thesis modularity)
        title_page_src = get_templates_dir() / "title_page.typ"
        if title_page_src.exists():
            import shutil
            shutil.copy2(title_page_src, build_dir / "title_page.typ")
        
        includes = []
        
        # Use header that imports the template
        master_content = self._get_template_header(project)
        
        import re
        for chapter in project.chapters:
            chap_includes = []
            # Start new page for each chapter (if enabled)
            if page_break:
                chap_includes.append("#pagebreak(weak: true)")
            
            # Add a chapter heading (Level 1)
            # Remove prefix like '01_' from folder name
            display_title = re.sub(r'^\d+[_ ]+', '', chapter.title)
            if chapter.title.startswith('00_') or not re.match(r'^\d+', chapter.title):
                chap_includes.append(f'#heading(numbering: none, outlined: true)[{display_title}]\n')
            else:
                chap_includes.append(f'= {display_title}\n')

            
            for p in chapter.paragraphs:
                rel_path = p.path.relative_to(project.path)
                target_typ = build_dir / rel_path.with_suffix(".typ")
                target_typ.parent.mkdir(parents=True, exist_ok=True)
                
                # Pre-process content: Normalize image paths using class patterns
                processed_content = self._normalize_image_paths(p.content)
                
                # Use configurable pandoc extensions
                self.pandoc.convert_markdown_to_typst(processed_content, target_typ, 
                                                       extensions=pandoc_extensions)
                
                # Make path relative to build_dir
                inc_rel = target_typ.relative_to(build_dir)
                chap_includes.append(f'#include "{inc_rel.as_posix()}"')
                
            includes.append("\n\n".join(chap_includes))
            
        master_content += "\n\n" + "\n\n".join(includes)
        
        # Copy assets
        if (project.path / "assets").exists():
            import shutil
            assets_target = build_dir / "assets"
            if assets_target.exists(): shutil.rmtree(assets_target)
            shutil.copytree(project.path / "assets", assets_target)
            
        if (project.path / "references.bib").exists():
             # Copy bib file
             # Copy bib file
             import shutil
             bib_source = project.path / "references.bib"
             shutil.copy2(bib_source, build_dir / "references.bib")
             
             # Only add bibliography if file is not empty
             if bib_source.stat().st_size > 0:
                 master_content += '\n\n#pagebreak(weak: true)\n#set heading(numbering: none)\n#bibliography("references.bib")'

        # Write master
        master_path = build_dir / "master.typ"
        master_path.write_text(master_content, encoding="utf-8")
        
        # Post-process: Fix deprecated symbols
        self._fix_deprecated_symbols(build_dir)
        
        # Compile
        if not output_path:
            output_path = project.path / f"{project.name}.pdf"
            
        logger.info(f"Compiling {master_path.name} -> {output_path.name}")
        self.typst.compile(master_path, output_path)
        
        logger.info(f"PDF compilation complete: {output_path}")
        return output_path
        
    def compile_docx(self, project: Project, output_path: Path = None):
        """
        Exports the project to DOCX by concatenating all markdown and converting at once.
        """
        logger.info(f"Starting DOCX export for: {project.name}")
        
        build_dir = project.path / ".build"
        build_dir.mkdir(exist_ok=True)
        
        full_md_path = build_dir / "full_project.md"
        
        # Concatenate content
        full_content = []
        full_content.append(f"% {project.name}")
        full_content.append(f"% Author")
        full_content.append("")
        
        for chapter in project.chapters:
            # Remove prefix like '01_' from folder name for clean headings
            display_title = re.sub(r'^\d+[_ ]+', '', chapter.title)
            if chapter.title.startswith('00_') or not re.match(r'^\d+', chapter.title):
                full_content.append(f"# {display_title} {{-}}\n")
            else:
                full_content.append(f"# {display_title}\n")
            for p in chapter.paragraphs:
                # Pre-process content: Normalize image paths
                # We need them relative to the build dir (where full_project.md is)
                # Or absolute. Pandoc handles absolute best if we are running from root.
                # Let's keep them as is and assume we run pandoc? 
                # Actually, Convert normalized paths (../assets) to absolute for safety in DOCX
                content = self._normalize_image_paths(p.content)
                # Hack: replace "../assets" with absolute path to assets
                assets_abs = (project.path / "assets").as_posix()
                content = content.replace("../assets", assets_abs)
                
                full_content.append(content)
                full_content.append("\n\n")
        
        # Append Bibliography Header if bib exists
        bib_path = project.path / "references.bib"
        has_bib = bib_path.exists() and bib_path.stat().st_size > 0
        
        if has_bib:
             full_content.append("\n\n# Bibliografia\n")
        
        
        # Pre-process narrative citations for numeric CSL compatibility
        # Transforms bare @citekey into "Surname [-@citekey]"
        joined = "\n".join(full_content)
        if has_bib:
            joined = self._preprocess_narrative_citations(joined, bib_path)

        
        full_md_path.write_text(joined, encoding="utf-8")
        
        if not output_path:
            output_path = project.path / f"{project.name}.docx"
            
        # Check for custom reference doc
        ref_doc = get_templates_dir() / "reference.docx"
        if not ref_doc.exists(): ref_doc = None
        
        # Check for CSL
        # Default to IEEE if not specified
        csl_path = project.path / "assets" / "csl" / "ieee.csl"
        if not csl_path.exists():
             csl_path = get_templates_dir().parent / "csl" / "ieee.csl"
        
        # Build metadata for Pandoc
        # We need to pass metadata via a sidecar yaml or arguments?
        # PandocWrapper doesn't support arbitrary args easily in the current signature.
        # Let's update PandocWrapper signature first? 
        # Actually, let's just pass it via the 'metadata' argument to convert_markdown_to_docx if we add it.
        # For now, let's hardcode lang=it-IT in the wrapper or add it as an argument.
        
        logger.info(f"Exporting DOCX: {full_md_path.name} -> {output_path.name}")
        
        self.pandoc.convert_markdown_to_docx(
            full_md_path, 
            output_path,
            reference_doc=ref_doc,
            bibliography=bib_path if has_bib else None,
            csl=csl_path if csl_path.exists() else None,
            metadata={
                "lang": "it-IT",
                "link-citations": "true"
            },
            toc=True,
            numbered=True
        )
        
        logger.info(f"DOCX export complete: {output_path}")
        return output_path
