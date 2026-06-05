from pathlib import Path
import shutil
from .paths import get_pandoc_exe, get_typst_exe, get_templates_dir

class EnvironmentChecker:
    @staticmethod
    def check_tools():
        """Checks availability of external tools and templates."""
        results = []
        
        # 1. Pandoc
        pandoc = get_pandoc_exe()
        if shutil.which(pandoc.name) or pandoc.exists():
             results.append(("Pandoc", "OK", str(pandoc)))
        else:
             results.append(("Pandoc", "MISSING", "Required for Markdown -> Typst/Docx conversion"))

        # 2. Typst
        typst = get_typst_exe()
        if shutil.which(typst.name) or typst.exists():
             results.append(("Typst", "OK", str(typst)))
        else:
             results.append(("Typst", "MISSING", "Required for PDF compilation"))

        # 3. PyPDF (Optional but recommended)
        try:
            import pypdf
            results.append(("PyPDF", "OK", f"Installed (v{pypdf.__version__})"))
        except ImportError:
            results.append(("PyPDF", "WARNING", "Not installed. Metadata inspection will be disabled."))

        # 4. Templates
        tpl = get_templates_dir() / "default_thesis.typ"
        if tpl.exists():
             results.append(("Templates", "OK", "Default template found"))
        else:
             results.append(("Templates", "MISSING", f"Not found at {tpl}"))

        return results

    @staticmethod
    def print_report():
        results = EnvironmentChecker.check_tools()
        print("\nDependency Check Report:")
        print(f"{'Component':<15} | {'Status':<10} | {'Details'}")
        print("-" * 60)
        
        all_ok = True
        for name, status, details in results:
            print(f"{name:<15} | {status:<10} | {details}")
            if status == "MISSING":
                all_ok = False
        
        return all_ok
