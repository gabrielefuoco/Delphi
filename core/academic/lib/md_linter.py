"""
Delphi Markdown Content Linter
==============================
Analizza i file .md generati dall'LLM per individuare e correggere 
difetti tipici di formattazione, struttura e rendering.

Modalità:
  - report: restituisce issue senza modificare i file
  - fix:    applica auto-fix sicure e restituisce il resoconto
"""

import re
import os
import glob
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from enum import Enum


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class LintIssue:
    file: str
    line: int
    rule_id: str
    severity: Severity
    message: str
    auto_fixed: bool = False

    def __str__(self):
        status = "✅ FIXED" if self.auto_fixed else f"{'🔴' if self.severity == Severity.ERROR else '🟡' if self.severity == Severity.WARNING else '🔵'}"
        basename = os.path.basename(self.file)
        return f"  {status} [{self.rule_id}] {basename}:{self.line} — {self.message}"


# ─────────────────────────────────────────────
#  Pattern di etichette strutturali LLM
# ─────────────────────────────────────────────
STRUCTURAL_LABELS = [
    "Dimostrazioni", "Dimostrazione", "Diagrammi", "Diagramma",
    "Spiegazione della dimostrazione", "Spiegazione", "Definizione",
    "Diagramma Paragrafo", "Diagramma Logico della Dimostrazione",
]

# Regex per riconoscere una riga che contiene solo un'etichetta bold
_LABEL_PATTERNS = []
for lbl in STRUCTURAL_LABELS:
    # Matches: **Label:** , **Label** , * **Label:** , - **Label:**
    _LABEL_PATTERNS.append(re.compile(
        rf'^\s*[\*\-]?\s*\*\*{re.escape(lbl)}:?\*\*(?:\\)?\s*$'
    ))


def _is_structural_label(line: str) -> bool:
    """Verifica se una riga è un'etichetta strutturale isolata (senza contenuto)."""
    stripped = line.strip()
    if not stripped:
        return False
    for pat in _LABEL_PATTERNS:
        if pat.match(stripped):
            return True
    return False


def _get_label_name(line: str) -> Optional[str]:
    """Estrae il nome dell'etichetta dalla riga, se presente."""
    stripped = line.strip()
    for lbl in STRUCTURAL_LABELS:
        if lbl.lower() in stripped.lower():
            return lbl
    return None


# ─────────────────────────────────────────────
#  Regole di Linting
# ─────────────────────────────────────────────

def _check_setext_headers(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD001: Testo seguito da --- senza riga vuota (crea H2 setext accidentale)."""
    issues = []
    new_lines = list(lines)
    i = 0
    while i < len(new_lines):
        line = new_lines[i].rstrip()
        if re.match(r'^-{3,}\s*$', line) and i > 0:
            prev = new_lines[i - 1].rstrip()
            # Se la riga precedente è testo (non vuota, non header, non lista, non fence)
            if prev and not prev.startswith('#') and not prev.startswith('```') and not prev.startswith('-') and not prev.startswith('*') and prev != '---':
                issue = LintIssue(
                    file=filepath, line=i + 1, rule_id="MD001",
                    severity=Severity.ERROR,
                    message=f"Setext H2 accidentale: il testo '{prev[:50]}...' è seguito da '---' senza riga vuota"
                )
                if fix:
                    # Inserisci riga vuota prima del ---
                    new_lines.insert(i, '\n')
                    issue.auto_fixed = True
                    i += 1  # compenso per l'inserimento
                issues.append(issue)
        i += 1
    return new_lines, issues


def _check_mermaid_fences(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD002: Mermaid fence con trailing/leading spaces o backtick mancanti."""
    issues = []
    new_lines = list(lines)
    for i, line in enumerate(new_lines):
        raw = line.rstrip('\n').rstrip('\r')
        # Controlla fence di apertura con trailing spaces o 1-2 backtick
        if re.match(r'^(\s*)`{1,3}mermaid\s*$', raw) and raw.strip() != '```mermaid':
            issue = LintIssue(
                file=filepath, line=i + 1, rule_id="MD002",
                severity=Severity.ERROR,
                message="Mermaid fence malformato (spazi extra o backtick mancanti)"
            )
            if fix:
                new_lines[i] = '```mermaid\n'
                issue.auto_fixed = True
            issues.append(issue)
        # Controlla fence di chiusura con trailing spaces  
        elif re.match(r'^(\s*)```\s+$', raw) and not raw.strip().startswith('```mermaid'):
            # Verifica che siamo dentro un blocco mermaid
            in_mermaid = False
            for j in range(i - 1, -1, -1):
                if '```mermaid' in lines[j]:
                    in_mermaid = True
                    break
                if lines[j].strip() == '```':
                    break
            if in_mermaid:
                issue = LintIssue(
                    file=filepath, line=i + 1, rule_id="MD002",
                    severity=Severity.ERROR,
                    message="Fence di chiusura ``` con spazi trailing"
                )
                if fix:
                    new_lines[i] = '```\n'
                    issue.auto_fixed = True
                issues.append(issue)
    return new_lines, issues


def _check_glued_lists(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD003: Lista numerata incollata a un'etichetta bold."""
    issues = []
    new_lines = list(lines)
    i = 0
    while i < len(new_lines):
        line = new_lines[i]
        # Pattern: **Label:** 1. **Item** o **Label:** 1) Item
        match = re.match(r'^(\*\*[^*]+\*\*:?\s+)(1[\.\)]\s+.+)$', line.strip())
        if match:
            label_part = match.group(1).rstrip()
            list_part = match.group(2)
            issue = LintIssue(
                file=filepath, line=i + 1, rule_id="MD003",
                severity=Severity.WARNING,
                message=f"Lista numerata incollata all'etichetta: '{label_part[:30]}... 1.'"
            )
            if fix:
                indent = line[:len(line) - len(line.lstrip())]
                new_lines[i] = f"{indent}{label_part}\n"
                new_lines.insert(i + 1, f"{indent}{list_part}\n")
                issue.auto_fixed = True
                i += 1  # compenso
            issues.append(issue)
        i += 1
    return new_lines, issues


def _check_list_indent(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD004: Rientro inconsistente del primo item di una lista numerata."""
    issues = []
    new_lines = list(lines)
    for i, line in enumerate(new_lines):
        # Riga con spazio iniziale extra + numero di lista
        match = re.match(r'^( +)(\d+\.\s+.+)$', line.rstrip('\n'))
        if match:
            spaces = match.group(1)
            content = match.group(2)
            # Controlla se la riga successiva è anche un item di lista senza lo stesso indent
            if i + 1 < len(new_lines):
                next_match = re.match(r'^(\d+\.\s+)', new_lines[i + 1])
                if next_match and len(spaces) > 0:
                    issue = LintIssue(
                        file=filepath, line=i + 1, rule_id="MD004",
                        severity=Severity.WARNING,
                        message=f"Item di lista con rientro extra ({len(spaces)} spazi)"
                    )
                    if fix:
                        new_lines[i] = content + '\n'
                        issue.auto_fixed = True
                    issues.append(issue)
    return new_lines, issues


def _check_ghost_labels(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD005: Etichette strutturali isolate senza contenuto a seguire."""
    issues = []
    new_lines = list(lines)
    indices_to_remove = []
    
    i = 0
    while i < len(new_lines):
        if _is_structural_label(new_lines[i]):
            label_name = _get_label_name(new_lines[i])
            # Cerca la prossima riga non vuota
            j = i + 1
            while j < len(new_lines) and new_lines[j].strip() == '':
                j += 1
            
            is_empty = False
            if j >= len(new_lines):
                # Fine file: l'etichetta è orfana
                is_empty = True
            elif _is_structural_label(new_lines[j]):
                # Seguita da un'altra etichetta: è vuota
                # Eccezione: "Diagrammi" seguita da ```mermaid è valida
                is_empty = True
            elif new_lines[j].strip().startswith('#'):
                # Seguita da un header: è vuota
                is_empty = True
            
            # Eccezione: "Diagrammi" + mermaid
            if label_name and "Diagramm" in label_name:
                if j < len(new_lines) and '```mermaid' in new_lines[j]:
                    is_empty = False
                elif is_empty:
                    # Diagrammi senza diagramma: rimuovi
                    pass
            
            if is_empty:
                issue = LintIssue(
                    file=filepath, line=i + 1, rule_id="MD005",
                    severity=Severity.WARNING,
                    message=f"Etichetta fantasma '{label_name}' senza contenuto"
                )
                if fix:
                    # Segna per rimozione (label + righe vuote dopo)
                    for k in range(i, j):
                        indices_to_remove.append(k)
                    issue.auto_fixed = True
                issues.append(issue)
        i += 1
    
    if fix and indices_to_remove:
        new_lines = [l for idx, l in enumerate(new_lines) if idx not in indices_to_remove]
    
    return new_lines, issues


def _check_excessive_blank_lines(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD006: 3+ righe vuote consecutive."""
    issues = []
    new_lines = []
    blank_count = 0
    reported = False
    
    for i, line in enumerate(lines):
        if line.strip() == '':
            blank_count += 1
            if blank_count >= 3 and not reported:
                issue = LintIssue(
                    file=filepath, line=i + 1, rule_id="MD006",
                    severity=Severity.INFO,
                    message="3+ righe vuote consecutive"
                )
                if fix:
                    issue.auto_fixed = True
                issues.append(issue)
                reported = True
            if fix and blank_count > 2:
                continue  # non aggiungere la riga
        else:
            blank_count = 0
            reported = False
        new_lines.append(line)
    
    if not fix:
        new_lines = lines
    return new_lines, issues


def _check_orphan_symbols(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD007: Simbolo matematico breve orfano a fine riga (potenziale wrap isolato)."""
    issues = []
    new_lines = list(lines)
    # Preposizioni italiane brevi che precedono simboli
    preps = r'(?:a|di|da|in|con|su|per|tra|fra|ad|del|al|dal|nel)'
    
    for i, line in enumerate(new_lines):
        # Pattern: " a $X$." o " di $Y$," a fine riga
        match = re.search(rf'\s({preps})\s(\$[^$]{{1,5}}\$[.,;:]*)\s*$', line, re.IGNORECASE)
        if match:
            prep = match.group(1)
            symbol = match.group(2)
            # Solo se il simbolo è davvero breve (meno di 8 char totali)
            if len(symbol) <= 8:
                issue = LintIssue(
                    file=filepath, line=i + 1, rule_id="MD007",
                    severity=Severity.INFO,
                    message=f"Potenziale simbolo orfano: '{prep} {symbol}' a fine riga"
                )
                if fix:
                    # Sostituisci lo spazio tra preposizione e simbolo con &nbsp;
                    new_line = line[:match.start(1)] + f'{prep}&nbsp;{symbol}' + line[match.end(2):]
                    new_lines[i] = new_line
                    issue.auto_fixed = True
                issues.append(issue)
    return new_lines, issues


def _check_missing_h2(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD008: File che non inizia con ## (H2 mancante)."""
    issues = []
    # Trova la prima riga non vuota
    first_content = None
    first_idx = 0
    for i, line in enumerate(lines):
        if line.strip():
            first_content = line.strip()
            first_idx = i
            break
    
    if first_content and not first_content.startswith('## '):
        issue = LintIssue(
            file=filepath, line=first_idx + 1, rule_id="MD008",
            severity=Severity.ERROR,
            message=f"H2 mancante a inizio file. Prima riga: '{first_content[:50]}...'. L'AGENTE DEVE inserire il titolo corretto da chunks.json."
        )
        # Non auto-fixabile: richiede lookup in chunks.json
        issues.append(issue)
    
    return lines, issues


def _check_empty_math_blocks(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD009: Blocchi $$ vuoti o con solo spazi."""
    issues = []
    new_lines = list(lines)
    content = ''.join(lines)
    
    # Pattern: $$ seguita da $$ con solo spazi/newline in mezzo
    empty_blocks = list(re.finditer(r'\$\$\s*\$\$', content))
    if empty_blocks:
        # Calcola la riga
        for m in empty_blocks:
            line_num = content[:m.start()].count('\n') + 1
            issue = LintIssue(
                file=filepath, line=line_num, rule_id="MD009",
                severity=Severity.ERROR,
                message="Blocco $$ vuoto (senza formula)"
            )
            if fix:
                issue.auto_fixed = True
            issues.append(issue)
        
        if fix:
            fixed_content = re.sub(r'\$\$\s*\$\$', '', content)
            new_lines = fixed_content.splitlines(True)
    
    return new_lines, issues


def _check_mermaid_plaintext_formulas(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD010: Formule scritte in testo puro nei nodi Mermaid (es. sigma^2 CC^t anziché LaTeX)."""
    issues = []
    in_mermaid = False
    
    # Pattern che identificano formule in testo puro
    formula_patterns = [
        re.compile(r'(?:\\|\b)(?:sigma|beta|alpha|theta|gamma|delta|epsilon|lambda|mu|rho|tau|omega|phi|psi|chi|eta|nu|zeta)(?:\b|[_\^0-9]|$)', re.IGNORECASE),
        re.compile(r'[A-Z]_(?:tilde|hat|bar)'),
        re.compile(r'(?:CC|MM|XX|X\'X)\^t'),
        re.compile(r'B_tilde|B_hat|V B_'),
    ]
    
    def extract_mermaid_labels(line: str) -> List[str]:
        # 1. Trova tutte le stringhe tra virgolette (sono i label dei nodi quotati)
        quoted_labels = re.findall(r'"(.*?)"', line)
        
        # 2. Rimuovi le parti quotate per evitare falsi positivi al loro interno
        line_no_quotes = re.sub(r'".*?"', '""', line)
        
        # 3. Trova i nodi non quotati (es. A[testo], B(testo), C{testo})
        unquoted_labels = []
        for m in re.finditer(r'\b\w+\s*([\[\(\{\>]+)([^"\s][^\]\)\}]*?)([\]\)\}\<]+)', line_no_quotes):
            content = m.group(2).strip()
            # Rimuove simboli di apertura/chiusura rimasti ai bordi (es. se era A[(testo)] o A((testo)))
            content = content.strip('[](){}<> ')
            if content and content != '""':
                unquoted_labels.append(content)
                
        return quoted_labels + unquoted_labels

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '```mermaid':
            in_mermaid = True
            continue
        if stripped == '```' and in_mermaid:
            in_mermaid = False
            continue
        
        if in_mermaid and stripped:
            node_contents = extract_mermaid_labels(stripped)
            for content in node_contents:
                for pat in formula_patterns:
                    if pat.search(content):
                        # Verifica che non sia già in $$ o $
                        if '$$' not in content and '$' not in content:
                            issue = LintIssue(
                                file=filepath, line=i + 1, rule_id="MD010",
                                severity=Severity.WARNING,
                                message=f"Formula in testo puro nel nodo Mermaid: '{content[:60]}'. L'AGENTE DEVE convertire in LaTeX ($$ ... $$) o in testo leggibile."
                            )
                            issues.append(issue)
                            break
    
    return lines, issues


def _check_html_entities_in_latex(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD011: Entità HTML dentro formule LaTeX (&#92; &#95; ecc.)."""
    issues = []
    new_lines = list(lines)
    
    for i, line in enumerate(new_lines):
        # Cerca entità HTML dentro delimitatori $ ... $ o $$ ... $$
        # Semplificazione: cerca entità HTML su qualsiasi riga che contiene $
        if '$' in line and re.search(r'&#\d+;', line):
            issue = LintIssue(
                file=filepath, line=i + 1, rule_id="MD011",
                severity=Severity.ERROR,
                message=f"Entità HTML dentro formula LaTeX: {re.findall(r'&#[0-9]+;', line)}"
            )
            if fix:
                # Decodifica le entità HTML più comuni
                replacements = {
                    '&#92;': '\\', '&#95;': '_', '&#123;': '{', '&#125;': '}',
                    '&#36;': '$', '&#38;': '&', '&#60;': '<', '&#62;': '>',
                    '&#40;': '(', '&#41;': ')',
                }
                for entity, char in replacements.items():
                    new_lines[i] = new_lines[i].replace(entity, char)
                issue.auto_fixed = True
            issues.append(issue)
    
    return new_lines, issues


def _check_fluff_ai(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD101: Residui di fluff conversazionale dall'LLM."""
    issues = []
    fluff_patterns = [
        (r"in qualit[àa] di (?:professore|assistente|esperto|docente)", "Fluff: 'In qualità di...'"),
        (r"^(?:ecco|di seguito)\s+(?:il|la|i|le)\s+", "Fluff: 'Ecco il/la...'"),
        (r"^certamente[,.]", "Fluff: 'Certamente,...'"),
        (r"^come richiesto[,.]", "Fluff: 'Come richiesto,...'"),
        (r"spero (?:che )?(?:sia|questo)", "Fluff: 'Spero che...'"),
    ]
    
    for i, line in enumerate(lines):
        stripped = line.strip().lower()
        for pattern, msg in fluff_patterns:
            if re.search(pattern, stripped):
                issues.append(LintIssue(
                    file=filepath, line=i + 1, rule_id="MD101",
                    severity=Severity.WARNING,
                    message=msg
                ))
                break
    
    return lines, issues


def _check_inline_math_blocks(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD012: Uso improprio di $$ per formule matematiche inline."""
    issues = []
    new_lines = list(lines)
    
    for i, line in enumerate(new_lines):
        # Cerca doppie $$ sulla stessa riga circondate da testo
        # Se la riga contiene $$ ... $$ ma ha anche altro testo normale
        if line.count('$$') >= 2 and len(line.strip()) > line.strip().rfind('$$') + 2:
            # Semplice euristica: se la riga non inizia e finisce solo con $$
            if not (line.strip().startswith('$$') and line.strip().endswith('$$')):
                issue = LintIssue(
                    file=filepath, line=i + 1, rule_id="MD012",
                    severity=Severity.WARNING,
                    message="Possibile blocco $$ usato inline (dovrebbe essere $...$ per formule nel testo)"
                )
                if fix:
                    # Sostituisce i $$ con $ se ci sono lettere prima o dopo, ma  un po' rischioso con regex semplici. 
                    # Lo segniamo come auto-fixed per una pulizia di base
                    new_lines[i] = re.sub(r'(?<!\S)\$\$(.+?)\$\$(?!\S)', r'$\1$', line)
                    issue.auto_fixed = True
                issues.append(issue)
                
    return new_lines, issues


def _check_missing_info(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD102: Presenza di placeholder 'INFORMAZIONE NON PRESENTE'."""
    issues = []
    new_lines = []
    
    for i, line in enumerate(lines):
        if re.search(r'(?i)informazione non presente', line):
            issue = LintIssue(
                file=filepath, line=i + 1, rule_id="MD102",
                severity=Severity.WARNING,
                message="Trovato placeholder LLM di informazione mancante"
            )
            if fix:
                issue.auto_fixed = True
            issues.append(issue)
            if fix:
                continue # Rimuove la riga
        new_lines.append(line)
        
    if not fix:
        new_lines = lines
    return new_lines, issues


def _check_hard_breaks(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD013: Rimuove backslash orfani e spazi a fine riga pre-mdformat."""
    issues = []
    new_lines = list(lines)
    for i, line in enumerate(new_lines):
        original = line
        cleaned = re.sub(r'(?<!\\)\\[ \t]*(\r?\n)', r'\1', line)
        cleaned = re.sub(r'[ \t]+(\r?\n)?$', r'\1', cleaned)
        
        if cleaned != original:
            issue = LintIssue(
                file=filepath, line=i + 1, rule_id="MD013",
                severity=Severity.INFO,
                message="Rimossi spazi finali o backslash per prevenire anomalie di a capo"
            )
            if fix:
                new_lines[i] = cleaned
                issue.auto_fixed = True
            issues.append(issue)
            
    return new_lines, issues


def _pre_format_markdown(lines: List[str], filepath: str, fix: bool) -> Tuple[List[str], List[LintIssue]]:
    """MD000: Usa mdformat (se installato) per formattazione base, proteggendo la matematica."""
    issues = []
    if not fix:
        return list(lines), issues

    try:
        import mdformat
    except ImportError:
        return list(lines), issues

    text = "".join(lines)
    
    protected_blocks = {}
    counter = 0
    
    def _protect(match):
        nonlocal counter
        placeholder = f"DELPHI_PROTECTED_BLOCK_{counter:05d}"
        protected_blocks[placeholder] = match.group(0)
        counter += 1
        return placeholder

    # 1. Mascheramento
    text = re.sub(r'```mermaid[\s\S]*?```', _protect, text)
    text = re.sub(r'\$\$[\s\S]*?\$\$', _protect, text)
    text = re.sub(r'(?<!\$)\$[^\$\n]+?\$(?!\$)', _protect, text)

    # 2. Formattazione
    try:
        formatted_text = mdformat.text(text, options={"wrap": "keep", "number": True})
    except Exception:
        return list(lines), issues

    for placeholder, original_content in protected_blocks.items():
        formatted_text = formatted_text.replace(placeholder, original_content)
        
    new_lines = formatted_text.splitlines(keepends=True)
    
    if "".join(lines) != "".join(new_lines):
        issue = LintIssue(
            file=filepath, line=1, rule_id="MD000",
            severity=Severity.INFO,
            message="Auto-formattazione mdformat applicata (spazi, liste, paragrafi)",
            auto_fixed=True
        )
        issues.append(issue)
        
    return new_lines, issues


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────

ALL_RULES = [
    _check_missing_h2,           # MD008 (prima, non modifica)
    _check_setext_headers,       # MD001
    _check_mermaid_fences,       # MD002
    _check_hard_breaks,          # MD013 (prima di mdformat)
    _pre_format_markdown,        # MD000
    _check_glued_lists,          # MD003
    _check_list_indent,          # MD004
    _check_ghost_labels,         # MD005
    _check_excessive_blank_lines, # MD006
    _check_orphan_symbols,       # MD007
    _check_empty_math_blocks,    # MD009
    _check_mermaid_plaintext_formulas,  # MD010
    _check_html_entities_in_latex, # MD011
    _check_inline_math_blocks,   # MD012
    _check_fluff_ai,             # MD101
    _check_missing_info,         # MD102
]


def lint_file(filepath: str, fix: bool = False) -> List[LintIssue]:
    """Esegue il linting su un singolo file .md."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    all_issues = []
    current_lines = lines
    
    for rule_fn in ALL_RULES:
        current_lines, issues = rule_fn(current_lines, filepath, fix)
        all_issues.extend(issues)
    
    # Se in modalità fix, scrivi il file aggiornato
    if fix:
        fixed_count = sum(1 for i in all_issues if i.auto_fixed)
        if fixed_count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(current_lines)
    
    return all_issues


def lint_project(chapters_dir: str, fix: bool = False, verbose: bool = False) -> List[LintIssue]:
    """Esegue il linting su tutti i .md di un progetto Delphi."""
    all_issues = []
    
    chapters_path = Path(chapters_dir)
    if not chapters_path.exists():
        return all_issues
    
    md_files = sorted(chapters_path.rglob("*.md"))
    
    for md_file in md_files:
        file_issues = lint_file(str(md_file), fix=fix)
        all_issues.extend(file_issues)
    
    return all_issues


def format_report(issues: List[LintIssue], verbose: bool = False) -> str:
    """Formatta il report di linting per output CLI."""
    if not issues:
        return "✅ Nessun problema trovato nei file Markdown."
    
    errors = [i for i in issues if i.severity == Severity.ERROR]
    warnings = [i for i in issues if i.severity == Severity.WARNING]
    infos = [i for i in issues if i.severity == Severity.INFO]
    fixed = [i for i in issues if i.auto_fixed]
    
    lines = []
    lines.append(f"\n📋 Report Linting Markdown")
    lines.append(f"{'=' * 50}")
    lines.append(f"  🔴 Errori:     {len(errors)}")
    lines.append(f"  🟡 Warning:    {len(warnings)}")
    lines.append(f"  🔵 Info:       {len(infos)}")
    if fixed:
        lines.append(f"  ✅ Auto-fixed: {len(fixed)}")
    lines.append(f"{'=' * 50}")
    
    # Raggruppa per file
    by_file = {}
    for issue in issues:
        if not verbose and issue.severity == Severity.INFO and issue.auto_fixed:
            continue
        basename = os.path.basename(issue.file)
        by_file.setdefault(basename, []).append(issue)
    
    for fname, file_issues in sorted(by_file.items()):
        lines.append(f"\n📄 {fname}:")
        for issue in sorted(file_issues, key=lambda x: x.line):
            lines.append(str(issue))
    
    # Se ci sono issue non auto-fixed, aggiungi istruzioni per l'agente
    manual_issues = [i for i in issues if not i.auto_fixed and i.severity in (Severity.ERROR, Severity.WARNING)]
    if manual_issues:
        lines.append(f"\n{'=' * 50}")
        lines.append(f"⚠️  {len(manual_issues)} problemi richiedono intervento MANUALE dell'agente.")
        lines.append(f"L'agente DEVE aprire ogni file segnalato con view_file e correggere con replace_file_content.")
    
    return '\n'.join(lines)
