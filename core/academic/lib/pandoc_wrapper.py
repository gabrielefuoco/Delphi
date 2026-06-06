import subprocess
from pathlib import Path
from .paths import get_pandoc_exe

class PandocWrapper:
    def __init__(self):
        self.exe = get_pandoc_exe()
        
    def _check_exists(self):
        import shutil
        if not shutil.which(self.exe.name) and not self.exe.exists():
             raise FileNotFoundError(f"Pandoc executable not found. Please install Pandoc or place 'pandoc.exe' in {self.exe.parent}")

    def convert_markdown_to_typst(self, input_text: str, output_path: Path, 
                                   extensions: str = "+tex_math_dollars"):
        """
        Converts Markdown string to a Typst file using Pandoc.
        
        Args:
            input_text: Markdown content to convert
            output_path: Path for the output .typ file
            extensions: Pandoc markdown extensions (default: +tex_math_dollars for $...$ math)
        """
        self._check_exists()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build format string with extensions
        from_format = f"markdown{extensions}"
        
        cmd = [
            str(self.exe),
            "--from", from_format,
            "--to", "typst",
            "--output", str(output_path)
        ]
        # Use input_text via stdin
        process = subprocess.run(
            cmd,
            input=input_text,
            text=True,
            capture_output=True,
            encoding='utf-8'
        )

        if process.returncode != 0:
            raise RuntimeError(f"Pandoc failed: {process.stderr}")
        
        # Post-process: Fix Pandoc Typst output issues
        if output_path.exists():
            content = output_path.read_text(encoding="utf-8")
            # Fix #horizontalrule -> valid Typst line
            content = content.replace("#horizontalrule", '#line(length: 100%)')
            output_path.write_text(content, encoding="utf-8")

    def convert_markdown_to_docx(self, input_path: Path, output_path: Path, 
                                 reference_doc: Path = None,
                                 bibliography: Path = None,
                                 csl: Path = None,
                                 metadata: dict = None,
                                 toc: bool = False,
                                 numbered: bool = False):
        """
        Converts a Markdown file to DOCX with academic features.
        """
        cmd = [
            str(self.exe),
            str(input_path),
            "--from", "markdown+tex_math_dollars+citations",
            "--to", "docx",
            "--output", str(output_path)
        ]
        
        if reference_doc and reference_doc.exists():
            cmd.extend(["--reference-doc", str(reference_doc)])
            
        if bibliography and bibliography.exists():
            cmd.extend(["--bibliography", str(bibliography)])
            cmd.append("--citeproc") # Process citations
        
        if csl and csl.exists():
            cmd.extend(["--csl", str(csl)])
            
        if metadata:
            for k, v in metadata.items():
                cmd.extend(["--metadata", f"{k}={v}"])
            
        if toc:
            cmd.append("--toc")
            
        if numbered:
            cmd.append("--number-sections")

        self._check_exists()
        process = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if process.returncode != 0:
             raise RuntimeError(f"Pandoc DOCX export failed: {process.stderr}")

    def convert_markdown_to_epub(self, input_path: Path, output_path: Path, 
                                 cover_image: Path = None,
                                 metadata: dict = None,
                                 css: Path = None,
                                 toc: bool = True):
        """
        Converts a Markdown file to EPUB.
        """
        cmd = [
            str(self.exe),
            str(input_path),
            "--from", "markdown+tex_math_dollars+citations",
            "--to", "epub",
            "--output", str(output_path)
        ]
        
        if cover_image and cover_image.exists():
            cmd.extend(["--epub-cover-image", str(cover_image)])
            
        if metadata:
            for k, v in metadata.items():
                cmd.extend(["--metadata", f"{k}={v}"])
                
        if css and css.exists():
            cmd.extend(["--css", str(css)])
            
        if toc:
            cmd.append("--toc")

        self._check_exists()
        process = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if process.returncode != 0:
             raise RuntimeError(f"Pandoc EPUB export failed: {process.stderr}")
