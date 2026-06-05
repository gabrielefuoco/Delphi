import os
import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def bibtex_escape(text: str) -> str:
    """Converts accented characters to BibTeX escape sequences for maximum compatibility."""
    if not text: return ""
    # Common LaTeX/BibTeX escapes
    mapping = {
        'à': r'{\`a}', 'á': r"{\'a}", 'â': r'{\^a}', 'ã': r'{\~a}', 'ä': r'{\\"a}',
        'è': r'{\`e}', 'é': r"{\'e}", 'ê': r'{\^e}', 'ë': r'{\\"e}',
        'ì': r'{\`i}', 'í': r"{\'i}", 'î': r'{\^i}', 'ï': r'{\\"i}',
        'ò': r'{\`o}', 'ó': r"{\'o}", 'ô': r'{\^o}', 'õ': r'{\~o}', 'ö': r'{\\"o}',
        'ù': r'{\`u}', 'ú': r"{\'u}", 'û': r'{\^u}', 'ü': r'{\\"u}',
        'ñ': r'{\~n}', 'ç': r'{\c c}',
        'À': r'{\`A}', 'Á': r"{\'A}", 'Â': r'{\^A}', 'Ã': r'{\~A}', 'Ä': r'{\\"A}',
        'È': r'{\`E}', 'É': r"{\'E}", 'Ê': r'{\^E}', 'Ë': r'{\\"E}',
        'Ì': r'{\`I}', 'Í': r"{\'I}", 'Î': r'{\^I}', 'Ï': r'{\\"I}',
        'Ò': r'{\`O}', 'Ó': r"{\'O}", 'Ô': r'{\^O}', 'Õ': r'{\~O}', 'Ö': r'{\\"O}',
        'Ù': r'{\`U}', 'Ú': r"{\'U}", 'Û': r'{\^U}', 'Ü': r'{\\"U}',
        'Ñ': r'{\~N}', 'Ç': r'{\c C}',
        '—': '---', '–': '--',
        '→': r'$\rightarrow$', 'µ': r'$\mu$', '±': r'$\pm$'
    }
    for char, escape in mapping.items():
        text = text.replace(char, escape)
    return text

def ensure_utf8_bib(path: Path) -> bool:
    """
    Detects and repairs encoding issues in a BibTeX file.
    Reverses common mojibake and ensures the file is valid UTF-8.
    """
    if not path.exists(): return False
    
    try:
        # Try reading as UTF-8
        with open(path, 'rb') as f:
            raw = f.read()
        
        try:
            text = raw.decode('utf-8')
            # Check for mojibake patterns even if it decodes as UTF-8
            if 'Ã' in text or 'â' in text:
                # Potential mojibake detected - try to fix
                pass 
            else:
                return True # All good
        except UnicodeDecodeError:
            # Encoding is definitely not clean UTF-8
            text = raw.decode('latin-1')

        # Mojibake & Corrupted pattern replacement
        replacements = {
            'Ã ': 'à', 'Ã¡': 'á', 'Ã¢': 'â', 'Ã£': 'ã', 'Ã¤': 'ä',
            'Ã¨': 'è', 'Ã©': 'é', 'Ãª': 'ê', 'Ã«': 'ë',
            'Ã¬': 'ì', 'Ã­': 'í', 'Ã®': 'î', 'Ã¯': 'ï',
            'Ã²': 'ò', 'Ã³': 'ó', 'Ã´': 'ô', 'Ãµ': 'õ', 'Ã¶': 'ö',
            'Ã¹': 'ù', 'Ãº': 'ú', 'Ã»': 'û', 'Ã¼': 'ü',
            'Ã±': 'ñ', 'Ã§': 'ç',
            'Ã€': 'À', 'Ã ': 'Á', 'Ã‚': 'Â', 'Ãƒ': 'Ã', 'Ã„': 'Ä',
            'Ãˆ': 'È', 'Ã‰': 'É', 'ÃŠ': 'Ê', 'Ã‹': 'Ë',
            'ÃŒ': 'Ì', 'Ã ': 'Í', 'ÃŽ': 'Î', 'Ã ': 'Ï',
            'Ã’': 'Ò', 'Ã“': 'Ó', 'Ã”': 'Ô', 'Ã•': 'Õ', 'Ã–': 'Ö',
            'Ã™': 'Ù', 'Ãš': 'Ú', 'Ã›': 'Û', 'Ãœ': 'Ü',
            'Ã‘': 'Ñ', 'Ã‡': 'Ç',
            'â†’': '→', 'Âµ': 'µ', 'Â±': '±'
        }
        
        fixed_text = text
        for old, new in replacements.items():
            fixed_text = fixed_text.replace(old, new)
        
        # After fixing characters, convert to LaTeX escapes for permanent safety
        fixed_text = bibtex_escape(fixed_text)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed_text)
            
        logger.info(f"Fixed encoding/characters in {path.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to ensure UTF-8 for {path}: {e}")
        return False
