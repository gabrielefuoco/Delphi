import docx
from docx.shared import Pt, RGBColor, Cm, Emu
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from pathlib import Path

# =============================================================================
# PDF-matching settings (from default_thesis.typ)
# =============================================================================
# Font: "New Computer Modern" 12pt -> Use "Times New Roman" as Word equivalent
#   (New Computer Modern is a LaTeX font not typically installed in Word)
# Margins: left=3.5cm, right=2.5cm, top=3cm, bottom=3cm
# Leading: 0.65em (~1.3 line spacing)
# Paragraph spacing: 1.2em (~14.4pt at 12pt base)
# Headings: H1=1.8em(~22pt), H2=1.3em(~16pt), H3=1.1em(~13pt)
# =============================================================================

FONT_NAME = "Times New Roman"
FONT_SIZE = 12  # pt

MARGIN_LEFT = 3.5    # cm
MARGIN_RIGHT = 2.5   # cm
MARGIN_TOP = 3.0     # cm
MARGIN_BOTTOM = 3.0  # cm

LINE_SPACING = 1.3    # multiplier (Typst leading 0.65em ≈ 1.3x)
PARAGRAPH_SPACING = Pt(14)  # 1.2em at 12pt ≈ 14.4pt

HEADING_SIZES = {1: 22, 2: 16, 3: 13}  # pt, matching 1.8em, 1.3em, 1.1em
HEADING_DEFAULT_SIZE = 12  # pt


def create_reference_docx(output_path: Path):
    doc = docx.Document()
    
    # 1. Page Setup - Match PDF margins exactly
    for section in doc.sections:
        section.top_margin = Cm(MARGIN_TOP)
        section.bottom_margin = Cm(MARGIN_BOTTOM)
        section.left_margin = Cm(MARGIN_LEFT)
        section.right_margin = Cm(MARGIN_RIGHT)
        
    # 2. Styles
    styles = doc.styles
    
    def set_style_font(style_name, font_name=FONT_NAME, size=FONT_SIZE, 
                       bold=False, color=RGBColor(0, 0, 0), underline=None):
        style = styles[style_name]
        font = style.font
        font.name = font_name
        font.size = Pt(size)
        font.bold = bold
        font.color.rgb = color
        if underline is not None:
            font.underline = underline
        return style

    # --- Normal text ---
    normal = set_style_font("Normal", size=FONT_SIZE)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    normal.paragraph_format.line_spacing = LINE_SPACING  # 1.3x multiplier
    normal.paragraph_format.space_after = PARAGRAPH_SPACING
    normal.paragraph_format.space_before = Pt(0)

    # --- Headings ---
    heading_spacing = {
        1: (Pt(24), Pt(18)),   # H1: above=24pt, below=18pt (chapter)
        2: (Pt(18), Pt(12)),   # H2: above=18pt, below=12pt (section)
        3: (Pt(12), Pt(10)),   # H3: above=12pt, below=10pt (subsection)
    }
    
    for i in range(1, 10):
        style_name = f"Heading {i}"
        if style_name in styles:
            size = HEADING_SIZES.get(i, HEADING_DEFAULT_SIZE)
            s = set_style_font(style_name, font_name=FONT_NAME, size=size, 
                             bold=True, color=RGBColor(0, 0, 0))
            
            before, after = heading_spacing.get(i, (Pt(12), Pt(6)))
            s.paragraph_format.space_before = before
            s.paragraph_format.space_after = after
            s.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    # --- Title ---
    t = set_style_font("Title", size=24, bold=True, color=RGBColor(0, 0, 0))
    t.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # --- Subtitle ---
    if "Subtitle" in styles:
        st = set_style_font("Subtitle", size=18, bold=False, color=RGBColor(0, 0, 0))
        st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
    # --- TOC Heading ---
    if "TOC Heading" in styles:
        set_style_font("TOC Heading", size=22, bold=True, color=RGBColor(0, 0, 0))

    # --- Hyperlinks (black, no underline) ---
    if "Hyperlink" in styles:
        set_style_font("Hyperlink", color=RGBColor(0, 0, 0), underline=False)
        
    if "FollowedHyperlink" in styles:
        set_style_font("FollowedHyperlink", color=RGBColor(0, 0, 0), underline=False)

    # --- Bibliography style ---
    try:
        bib_style = styles['Bibliography']
    except KeyError:
        bib_style = styles.add_style('Bibliography', WD_STYLE_TYPE.PARAGRAPH)
        bib_style.base_style = styles['Normal']
    
    bib_font = bib_style.font
    bib_font.name = FONT_NAME
    bib_font.size = Pt(11)
    bib_font.color.rgb = RGBColor(0, 0, 0)
    
    bib_pf = bib_style.paragraph_format
    bib_pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    bib_pf.left_indent = Cm(1.0)
    bib_pf.first_line_indent = Cm(-1.0)
    bib_pf.space_after = Pt(6)
    bib_pf.space_before = Pt(0)
    bib_pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"Created reference doc at: {output_path}")

if __name__ == "__main__":
    root = Path(__file__).parent.parent
    ref_doc_path = root / "assets" / "templates" / "reference.docx"
    create_reference_docx(ref_doc_path)
