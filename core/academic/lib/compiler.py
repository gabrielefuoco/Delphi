from pathlib import Path
from typing import List, Dict, Set, Tuple
import re
import logging

from .pandoc_wrapper import PandocWrapper
from .models import Project
from .paths import get_templates_dir, get_typst_exe

# Configure module logger
logger = logging.getLogger(__name__)


def generate_ide_cover_html(title, subtitle, author, date, cover_accent):
    import re
    year_match = re.search(r'\b(20\d{2})\b', date)
    year = year_match.group(1) if year_match else "2026"
    safe_title = re.sub(r'[^a-zA-Z0-9_]', '_', title.lower())
    
    if not cover_accent or not cover_accent.startswith('#'):
        cover_accent = "#0ea5e9"
        
    def adjust_color(hex_color, l_factor):
        try:
            hx = hex_color.lstrip('#')
            if len(hx) == 3: hx = "".join(c*2 for c in hx)
            r, g, b = tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
            import colorsys
            h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
            l = max(0, min(1, l * l_factor))
            nr, ng, nb = colorsys.hls_to_rgb(h, l, s)
            return f'#{int(nr*255):02x}{int(ng*255):02x}{int(nb*255):02x}'
        except:
            return hex_color

    def hex_to_rgba(hex_color, alpha):
        try:
            hx = hex_color.lstrip('#')
            if len(hx) == 3: hx = "".join(c*2 for c in hx)
            r, g, b = tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
            return f"rgba({r},{g},{b},{alpha})"
        except:
            return hex_color

    col_dark = adjust_color(cover_accent, 0.7)
    col_deep = adjust_color(cover_accent, 0.4)
    col_light = hex_to_rgba(cover_accent, "0.14")
    
    style_str = f""" style="--col: {cover_accent}; --col-dark: {col_dark}; --col-deep: {col_deep}; --col-light: {col_light}; --grad: linear-gradient(150deg, {col_deep} 0%, {cover_accent} 55%, {col_light} 100%);" """
    
    ln_html = "".join(f"{i}<br>" for i in range(1, 52))
    
    words = title.split()
    if len(words) > 1:
        title_pro = words[0]
        title_rest = " " + " ".join(words[1:])
    else:
        title_pro = title
        title_rest = ""

    return f"""
<div class="page theme-ide"{style_str}>
<div class="grid"></div>
<div class="orb orb-a"></div>
<div class="orb orb-b"></div>
<div class="side-bar"></div>
<div class="bg-vol">1</div>
<div class="ln">{ln_html}</div>
<div class="dots">
<div class="dot d-r"></div><div class="dot d-y"></div><div class="dot d-g"></div>
<span class="dots-path">~/delphi/projects/{safe_title}/main.py</span>
</div>
<div class="content">
<div class="glass-card card-header">
<div class="header-comment"># {title}</div>
<div class="import-line"><span class="kw">from</span> delphi.projects <span class="kw">import</span> <span class="fn">{safe_title}</span></div>
</div>
<div class="section-title">
<div class="title-row">
<span class="title-pro">{title_pro}</span><span class="title-python">{title_rest}</span>
</div>
<div class="vtag">{{ "type": "academic_paper", "status": "COMPILED" }}</div>
</div>
<div class="glass-card card-desc">
<div class="desc-label"><span class="kw">description</span>: <span class="fn">str</span> =</div>
<div class="desc-value"><span class="str">"{subtitle}"</span></div>
</div>
<div class="glass-card card-author">
<div class="author-line"><span class="kw">const</span> author: <span class="fn">Author</span> = {{ name: <span class="str">"{author}"</span>, role: <span class="str">"Researcher"</span> }}</div>
<div class="rule"></div>
<div class="year-line">
<span class="kw">export default</span> {{&nbsp;edition: <span class="str">{year}</span>,&nbsp;license: <span class="str">"MIT"</span>&nbsp;}}
</div>
</div>
</div>
<div class="footer">
<span class="footer-status">[Status: DONE]</span>
<span>Delphi Academic Engine &middot; v0.1.0 &middot; &copy; {year}</span>
</div>
</div>
"""

class Compiler:
    """
    Compiles Delphi projects to PDF (via Typst) or DOCX (via Pandoc).
    
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
        'planck.reduce': 'planck',
    }
    
    # Image path patterns to normalize (relative to chapters/<chap_name>/file.md -> ../../assets/)
    IMAGE_PATH_PATTERNS: List[Tuple[str, str]] = [
        (r'\]\(@/', r'](../../assets/'),           # @/ convention
        (r'\]\(assets/', r'](../../assets/'),       # assets/ prefix
        (r'\]\(\./assets/', r'](../../assets/'),    # ./assets/ prefix
    ]
    
    def __init__(self):
        self.pandoc = PandocWrapper()
        
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

    def _sanitize_paragraph_headers(self, project: Project, chapter_title: str, paragraph_title: str, content: str) -> str:
        """
        Pulisce gli header duplicati o errati in cima al paragrafo, inietta 
        il titolo H2 corretto estrapolandolo da chunks.json, e corregge
        imperfezioni tipiche del Markdown generato dall'LLM.
        """
        import re
        import json
        
        # 1. Rimuovi tutti i vecchi header (H1/H2) all'inizio del file
        while re.match(r'^\s*#+', content):
            content = re.sub(r'^\s*#+.*?\n', '', content, count=1).lstrip()
            
        # 2. Rimuovi auto-numerazione interna generata dall'LLM (es. ### 1.1.1 Sotto-argomento -> ### Sotto-argomento)
        content = re.sub(r'^(#{2,})\s+\d+(?:\.\d+)*\.?\s+', r'\1 ', content, flags=re.MULTILINE)

        # 3. Sanitizza gli elenchi puntati: assicura interlinea vuota e converte '* ' in '- '
        lines = content.split('\n')
        new_lines = []
        for j, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('* '):
                # Se la linea precedente non è vuota e non è un elemento di lista, aggiungi un a-capo per isolare la lista
                if len(new_lines) > 0 and new_lines[-1].strip() != '' and not new_lines[-1].strip().startswith('- '):
                    new_lines.append('')
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.append(indent + '- ' + stripped[2:])
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines)
            
        # 4. Cerca il titolo esatto nel chunks.json
        real_title = "Paragrafo"
        chunks_file = project.path / "chunks.json"
        if chunks_file.exists():
            try:
                cdata = json.loads(chunks_file.read_text(encoding="utf-8"))
                for c in cdata:
                    safe_id = re.sub(r'[\\/*?:"<>|]', "", c.get("id", ""))
                    if safe_id == chapter_title:
                        for p in c.get("paragraphs", []):
                            p_safe_id = re.sub(r'[\\/*?:"<>|]', "", p.get("id", ""))
                            if p_safe_id == paragraph_title:
                                real_title = p.get("title", "Paragrafo")
                                break
                        break
            except Exception:
                pass
                
        # 5. Restituisci il testo sanitizzato
        return f"## {real_title}\n\n{content}"

    def _get_chapter_title(self, project: Project, folder_name: str) -> str:
        """
        Tenta di recuperare il titolo originale del capitolo dal chunks.json.
        Utile perché adesso usiamo ID compatti (es. '01_cap1') per le cartelle.
        """
        import json
        import re
        chunks_file = project.path / "chunks.json"
        if chunks_file.exists():
            try:
                cdata = json.loads(chunks_file.read_text(encoding="utf-8"))
                for c in cdata:
                    safe_id = re.sub(r'[\\/*?:"<>|]', "", c.get("id", ""))
                    if safe_id == folder_name:
                        return c.get("title", folder_name)
            except Exception:
                pass
        return re.sub(r'^\d+[_ ]+', '', folder_name)

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
             cfg = json.loads((project.path / "delphi.json").read_text(encoding="utf-8"))
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
  show_frontespizio: false
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
             cfg = json.loads((project.path / "delphi.json").read_text(encoding="utf-8"))
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
                                 "Set 'strict_asset_validation': false in delphi.json to proceed.")

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
            # Remove prefix like '01_' from folder name or use chunks.json
            display_title = self._get_chapter_title(project, chapter.title)
            if chapter.title.startswith('00_') or not re.match(r'^\d+', chapter.title):
                chap_includes.append(f'#heading(numbering: none, outlined: true)[{display_title}]\n')
            else:
                chap_includes.append(f'= {display_title}\n')

            
            for p in chapter.paragraphs:
                rel_path = p.path.relative_to(project.path)
                target_typ = build_dir / rel_path.with_suffix(".typ")
                target_typ.parent.mkdir(parents=True, exist_ok=True)
                
                # Sanitizzazione on-the-fly dell'header e iniezione H2
                p_text = self._sanitize_paragraph_headers(project, chapter.title, p.title, p.content)
                
                # Pre-process content: Normalize image paths using class patterns
                processed_content = self._normalize_image_paths(p_text)
                
                # Normalize headings: ensure the highest heading level in the paragraph is ## (level 2)
                # because the chapter title itself is level 1 (=)
                import re
                lines = processed_content.split('\n')
                headings = []
                for line in lines:
                    m = re.match(r'^(#{1,6})\s+', line)
                    if m:
                        headings.append(len(m.group(1)))
                if headings:
                    min_heading = min(headings)
                    if min_heading != 2:
                        shift = 2 - min_heading
                        new_lines = []
                        for line in lines:
                            m = re.match(r'^(#{1,6})(\s+.*)', line)
                            if m:
                                current_level = len(m.group(1))
                                new_level = max(2, current_level + shift)
                                new_lines.append('#' * new_level + m.group(2))
                            else:
                                new_lines.append(line)
                        processed_content = '\n'.join(new_lines)
                
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
        
        # Compile Typst Body
        if not output_path:
            output_dir = project.path / "output"
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f"{project.name}.pdf"
            
        logger.info(f"Compiling {master_path.name} -> body.pdf")
        
        import subprocess
        typst_bin = get_typst_exe()
        body_pdf_path = build_dir / "typst_body.pdf"
        
        if typst_bin.exists():
            try:
                subprocess.run([str(typst_bin), "compile", str(master_path), str(body_pdf_path)], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Errore durante la compilazione Typst: {e}")
                raise
        else:
            logger.warning(f"Typst binary non trovato in {typst_bin}. Provo comando di sistema.")
            try:
                subprocess.run(["typst", "compile", str(master_path), str(body_pdf_path)], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Errore Typst: {e}")
                raise
                
        # -- Generazione Copertina HTML --
        import json
        config_path = project.path / "delphi.json"
        config = {}
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        meta = config.get('metadata', {})
        
        logger.info("Avvio motore HTML per la copertina...")
        cover_md_path = build_dir / "web_cover.md"
        cover_pdf_path = build_dir / "web_cover.pdf"
        
        title_raw = meta.get('title', project.name)
        subtitle_raw = meta.get('subtitle', '')
        author_raw = meta.get('author', '')
        date_raw = meta.get('date', '')
        
        cover_theme = meta.get('cover_theme', 'theme-academic')
        cover_accent = meta.get('cover_accent_color', '')
        cover_font = meta.get('cover_font', '')
        
        style_attrs = []
        if cover_accent: style_attrs.append(f"--accent-color: {cover_accent}")
        if cover_font: style_attrs.append(f"--main-font: {cover_font}")
        style_str = f' style="{"; ".join(style_attrs)}"' if style_attrs else ''
        
        if not subtitle_raw: subtitle_raw = "Documentazione generata automaticamente tramite Delphi Engine."
        subtitle_div = f'    <div class="cover-subtitle">{subtitle_raw}</div>\n'
        if cover_theme == 'theme-ide':
            cover_html = generate_ide_cover_html(title_raw, subtitle_raw, author_raw, date_raw, cover_accent)
        else:
            cover_html = f"""<div class="cover-page {cover_theme}"{style_str}>
    <div class="cover-title">{title_raw}</div>
{subtitle_div}    <div class="cover-author">{author_raw}</div>
    <div class="cover-date">{date_raw}</div>
</div>
"""
        cover_md_path.write_text(cover_html, encoding="utf-8")
        
        base_export = Path(__file__).resolve().parent.parent.parent / "export_module"
        build_cover_script = base_export / "build_cover.js"
        merge_script = base_export / "merge_pdfs.js"
        
        try:
            subprocess.run(["node", str(build_cover_script), str(cover_md_path), str(cover_pdf_path)], check=True, cwd=str(project.path))
        except subprocess.CalledProcessError as e:
            logger.error(f"Errore generazione copertina HTML: {e}")
            raise RuntimeError("Generazione copertina HTML fallita.")
            
        # -- Fusione dei PDF --
        logger.info("Unione Copertina HTML e Corpo Typst...")
        try:
            subprocess.run(["node", str(merge_script), str(cover_pdf_path), str(body_pdf_path), str(output_path)], check=True, cwd=str(project.path))
        except subprocess.CalledProcessError as e:
            logger.error(f"Errore fusione PDF: {e}")
            raise RuntimeError("Fusione PDF fallita.")
            
        import shutil
        shutil.rmtree(build_dir, ignore_errors=True)
        logger.info(f"Esportazione completata: {output_path}")
        return output_path


    def compile_web(self, project: Project, output_path: Path = None):
        """Compila il progetto in PDF usando il vecchio engine web HTML/Puppeteer."""
        if not output_path:
            output_dir = project.path / "output"
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f"{project.name}.pdf"
            
        build_dir = project.path / ".build"
        build_dir.mkdir(exist_ok=True)
        
        # Separazione file per disabilitare footer sulla copertina
        cover_md_path = build_dir / "web_cover.md"
        body_md_path = build_dir / "web_body.md"
        
        # Generazione Copertina HTML
        import json
        config_path = project.path / "delphi.json"
        config = {}
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                
        meta = config.get('metadata', {})
        title = meta.get('title', project.name)
        subtitle = meta.get('subtitle', '')
        author = meta.get('author', '')
        date = meta.get('date', '')
        
        cover_theme = meta.get('cover_theme', 'theme-academic')
        cover_accent = meta.get('cover_accent_color', '')
        cover_font = meta.get('cover_font', '')
        
        style_attrs = []
        if cover_accent: style_attrs.append(f"--accent-color: {cover_accent}")
        if cover_font: style_attrs.append(f"--main-font: {cover_font}")
        style_str = f' style="{"; ".join(style_attrs)}"' if style_attrs else ''
        
        if not subtitle: subtitle = "Documentazione generata automaticamente tramite Delphi Engine."
        subtitle_div = f'        <div class="cover-subtitle">{subtitle}</div>\n'
        if cover_theme == 'theme-ide':
            cover_html = generate_ide_cover_html(title, subtitle, author, date, cover_accent)
        else:
            cover_html = f"""<div class="cover-page {cover_theme}"{style_str}>
    <div class="cover-content">
        <div class="cover-title">{title}</div>
{subtitle_div}        <div class="cover-author">{author}</div>
        <div class="cover-date">{date}</div>
    </div>
</div>
"""
        cover_md_path.write_text(cover_html, encoding="utf-8")
        
        # Generazione Indice e Contenuto
        import re
        toc_lines = [
            "<div class='toc-page' style='page-break-after: always; padding-top: 50px; font-family: \"Georgia\", serif;'>",
            "<h1 class='toc-title' style='font-size: 2.5em; font-weight: normal; border-bottom: 1px solid #ddd; padding-bottom: 15px; margin-bottom: 30px; color: #222;'>Indice</h1>",
            "<ul class='toc-list' style='list-style: none; padding-left: 0; margin: 0;'>"
        ]
        
        body_content = []
        
        for i, chapter in enumerate(project.chapters, 1):
            display_title = self._get_chapter_title(project, chapter.title)
            slug = re.sub(r'[^a-zA-Z0-9]+', '-', display_title.lower()).strip('-')
            
            # Voce Indice
            if chapter.title.startswith('00_') or not re.match(r'^\d+', chapter.title):
                toc_lines.append(f"<li style='margin-top: 20px; margin-bottom: 8px;'><a href='#{slug}' style='text-decoration: none; color: #111; font-weight: 600; font-size: 1.2em; letter-spacing: 0.5px;'>{display_title}</a></li>")
                body_content.append(f"<h1 id='{slug}' class='unnumbered'>{display_title}</h1>\n")
            else:
                toc_lines.append(f"<li style='margin-top: 20px; margin-bottom: 8px;'><a href='#{slug}' style='text-decoration: none; color: #111; font-weight: 600; font-size: 1.2em; letter-spacing: 0.5px;'>{display_title}</a></li>")
                body_content.append(f"<h1 id='{slug}'>{display_title}</h1>\n")
                
            toc_lines.append("<ul style='list-style: none; padding-left: 0; margin-top: 0; margin-bottom: 10px;'>")
            for p in chapter.paragraphs:
                # Sanitizzazione on-the-fly
                p_text = self._sanitize_paragraph_headers(project, chapter.title, p.title, p.content)
                
                # Trova la prima intestazione ## nel testo
                import re
                match = re.search(r'^##\s+(.*)', p_text, re.MULTILINE)
                if match:
                    para_title = match.group(1).strip()
                    para_slug = re.sub(r'[^a-zA-Z0-9]+', '-', para_title.lower()).strip('-')
                    
                    # Aggiungi voce all'Indice sotto il capitolo (rientrata)
                    toc_lines.append(f"<li style='margin-bottom: 8px;'><a href='#{para_slug}' style='text-decoration: none; color: #555; font-size: 1.05em; margin-left: 20px; display: inline-block; transition: color 0.2s ease;'>{para_title}</a></li>")
                    
                    # Sostituisci il ## nel testo con l'HTML corrispondente per abilitare l'anchor link
                    p_text = p_text.replace(match.group(0), f"<h2 id='{para_slug}'>{para_title}</h2>", 1)
                
                # Fix image paths
                def fix_img(m):
                    img_path = m.group(2)
                    if img_path.startswith('assets/'):
                        img_path = f"../../{img_path}"
                    return f"![{m.group(1)}]({img_path})"
                p_text = re.sub(r'!\[(.*?)\]\((.*?)\)', fix_img, p_text)
                
                body_content.append(p_text + "\n")
            toc_lines.append("</ul>")
                
        toc_lines.append("</ul></div>")
        toc_html = "\n".join(toc_lines)
        
        body_md_path.write_text(toc_html + "\n" + "\n".join(body_content), encoding="utf-8")
        
        # Invoca build_pdfs.js
        import subprocess
        from pathlib import Path
        script_path = Path(__file__).resolve().parent.parent.parent / "export_module" / "build_pdfs.js"
        logger.info("Avvio motore HTML per il PDF...")
        try:
            subprocess.run(
                ["node", str(script_path), str(cover_md_path), str(body_md_path), str(output_path)],
                check=True, cwd=str(project.path)
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Errore Node.js: {e}")
            raise RuntimeError("Compilazione Web fallita.")
            
        import shutil
        shutil.rmtree(build_dir, ignore_errors=True)
        logger.info(f"Esportazione Web completata: {output_path}")
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
            # Get real title from chunks.json or fallback
            display_title = self._get_chapter_title(project, chapter.title)
            # Add page break in DOCX
            if full_content and full_content[-1] != "":
                 full_content.append("")
            full_content.append("```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n")
            
            if chapter.title.startswith('00_') or not re.match(r'^\d+', chapter.title):
                full_content.append(f"# {display_title} {{-}}\n")
            else:
                full_content.append(f"# {display_title}\n")
            for p in chapter.paragraphs:
                # Sanitizzazione on-the-fly
                p_text = self._sanitize_paragraph_headers(project, chapter.title, p.title, p.content)
                
                # Pre-process content: Normalize image paths
                # We need them relative to the build dir (where full_project.md is)
                # Or absolute. Pandoc handles absolute best if we are running from root.
                # Let's keep them as is and assume we run pandoc? 
                # Actually, Convert normalized paths (../../assets) to absolute for safety in DOCX
                content = self._normalize_image_paths(p_text, pattern='../../assets/')
                # Hack: replace "../../assets" with absolute path to assets
                assets_abs = (project.path / "assets").as_posix()
                content = content.replace("../../assets", assets_abs)
                
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
            output_dir = project.path / "output"
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f"{project.name}.docx"
            
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
            numbered=False
        )
        
        logger.info(f"DOCX export complete: {output_path}")
        
        # Cleanup temp build directory
        import shutil
        shutil.rmtree(build_dir, ignore_errors=True)
        return output_path
