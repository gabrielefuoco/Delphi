from playwright.sync_api import sync_playwright

volumes = [
    {
        "v": 1,
        "cls": "v1",
        "header_comment": "# vol_01 :: core_python — internals, algorithms, clean architecture",
        "import_line": '<span class="kw">from</span> cpython.internals <span class="kw">import</span> <span class="fn">Architecture</span>, <span class="fn">Optimizer</span>',
        "description": 'Architettura CPython, algoritmi avanzati, clean code e design pattern — dalla teoria alla produzione.',
        "desc_type": "str",
        "tag": '{"volume": 1, "status": "RUNNING"}',
        "status": "RUNNING",
        "author_decl": '<span class="kw">const</span> author: <span class="fn">Author</span> = { name: <span class="str">"Gabriele Fuoco"</span>, role: <span class="str">"Software Engineer"</span> }',
        "year_expr": "2026",
    },
    {
        "v": 2,
        "cls": "v2",
        "header_comment": "# vol_02 :: distributed_systems — consensus, scale-out, infrastructure",
        "import_line": '<span class="kw">from</span> distributed <span class="kw">import</span> <span class="fn">RaftConsensus</span>, <span class="fn">Kafka</span>, <span class="fn">gRPC</span>',
        "description": 'Sistemi distribuiti, Kafka, gRPC e system design — architetture scalabili da zero a milioni di richieste.',
        "desc_type": "str",
        "tag": '{"volume": 2, "status": "ALL_NODES_SYNCED"}',
        "status": "ALL_NODES_SYNCED",
        "author_decl": '<span class="kw">const</span> author: <span class="fn">Author</span> = { name: <span class="str">"Gabriele Fuoco"</span>, role: <span class="str">"Cloud Architect"</span> }',
        "year_expr": "2026",
    },
    {
        "v": 3,
        "cls": "v3",
        "header_comment": "# vol_03 :: ai_engineering — transformers, mlops, generative models",
        "import_line": '<span class="kw">from</span> torch.nn <span class="kw">import</span> <span class="fn">Transformer</span>, <span class="fn">MultiheadAttention</span>',
        "description": 'AI engineering, LLM fine-tuning, RAG e MLOps — da un modello grezzo a un sistema in produzione.',
        "desc_type": "str",
        "tag": '{"volume": 3, "status": "MODEL_CONVERGED"}',
        "status": "MODEL_CONVERGED",
        "author_decl": '<span class="kw">const</span> author: <span class="fn">Author</span> = { name: <span class="str">"Gabriele Fuoco"</span>, role: <span class="str">"AI Engineer"</span> }',
        "year_expr": "2026",
    },
]


def make_page(vol):
    ln_html = "".join(f"{i}<br>" for i in range(1, 52))
    return f"""
<div class="page {vol['cls']}">
    <div class="grid"></div>
    <div class="orb orb-a"></div>
    <div class="orb orb-b"></div>
    <div class="side-bar"></div>
    <div class="bg-vol">{vol['v']}</div>
    <div class="ln">{ln_html}</div>

    <div class="dots">
        <div class="dot d-r"></div><div class="dot d-y"></div><div class="dot d-g"></div>
        <span class="dots-path">~/pro-python/vol{vol['v']}/main.py</span>
    </div>

    <div class="content">

        <!-- CARD 1: header -->
        <div class="glass-card card-header">
            <div class="header-comment">{vol['header_comment']}</div>
            <div class="import-line">{vol['import_line']}</div>
        </div>

        <!-- TITOLO: hero, fuori dai card -->
        <div class="section-title">
            <div class="title-row">
                <span class="title-pro">PRO</span><span class="title-python">Python</span>
            </div>
            <div class="vtag">{vol['tag']}</div>
        </div>

        <!-- CARD 2: descrizione -->
        <div class="glass-card card-desc">
            <div class="desc-label"><span class="kw">description</span>: <span class="fn">{vol['desc_type']}</span> =</div>
            <div class="desc-value"><span class="str">"{vol['description']}"</span></div>
        </div>

        <!-- CARD 3: autore + anno -->
        <div class="glass-card card-author">
            <div class="author-line">{vol['author_decl']}</div>
            <div class="rule"></div>
            <div class="year-line">
                <span class="kw">export default</span> {{&nbsp;edition: <span class="str">{vol['year_expr']}</span>,&nbsp;license: <span class="str">"MIT"</span>&nbsp;}}
            </div>
        </div>

    </div>

    <div class="footer">
        <span class="footer-status">[Status: {vol['status']}]</span>
        <span>PRO Python &middot; v{vol['v']}.0.0 &middot; &copy; {vol['year_expr']}</span>
    </div>
</div>
"""


pages_html = "".join(make_page(v) for v in volumes)

html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>PRO Python</title>
    <style>
        @page {{ size: A4; margin: 0; }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}

        /* ── Colori per volume ── */
        .v1 {{
            --col:       #0ea5e9;
            --col-dark:  #0369a1;
            --col-deep:  #0c4a6e;
            --col-light: rgba(14,165,233,0.14);
            --glass:     rgba(255,255,255,0.35);
            --glass-bdr: rgba(255,255,255,0.85);
            --grad:      linear-gradient(150deg, #0c4a6e 0%, #0ea5e9 55%, #38bdf8 100%);
        }}
        .v2 {{
            --col:       #a855f7;
            --col-dark:  #7e22ce;
            --col-deep:  #3b0764;
            --col-light: rgba(168,85,247,0.14);
            --glass:     rgba(255,255,255,0.35);
            --glass-bdr: rgba(255,255,255,0.85);
            --grad:      linear-gradient(150deg, #3b0764 0%, #a855f7 55%, #e879f9 100%);
        }}
        .v3 {{
            --col:       #10b981;
            --col-dark:  #047857;
            --col-deep:  #064e3b;
            --col-light: rgba(16,185,129,0.14);
            --glass:     rgba(255,255,255,0.35);
            --glass-bdr: rgba(255,255,255,0.85);
            --grad:      linear-gradient(150deg, #064e3b 0%, #10b981 55%, #34d399 100%);
        }}

        /* ── Pagina ── */
        .page {{
            position: relative;
            width: 210mm; height: 297mm;
            overflow: hidden;
            background: #edf4fb;
            page-break-after: always;
        }}
        .page:last-child {{ page-break-after: avoid; }}

        .grid {{
            position: absolute; inset: 0;
            background-image:
                linear-gradient(var(--col-light) 1px, transparent 1px),
                linear-gradient(90deg, var(--col-light) 1px, transparent 1px);
            background-size: 10mm 10mm;
        }}
        .orb {{
            position: absolute; border-radius: 50%;
            filter: blur(90px); opacity: 0.26;
            background: var(--grad); pointer-events: none;
        }}
        .orb-a {{ top: -50mm; right: -50mm; width: 220mm; height: 220mm; }}
        .orb-b {{ bottom: -40mm; left: -60mm; width: 220mm; height: 220mm; }}

        .side-bar {{
            position: absolute; top: 0; left: 0;
            width: 9mm; height: 100%;
            background: var(--grad);
        }}

        .bg-vol {{
            position: absolute;
            right: -10mm; bottom: 10mm;
            font-size: 380pt; font-weight: 900;
            color: var(--col); opacity: 0.05;
            line-height: 1; user-select: none;
        }}

        .ln {{
            position: absolute; top: 0; left: 9mm;
            width: 12mm; height: 100%;
            background: rgba(0,0,0,0.01);
            border-right: 1.5px solid var(--col-light);
            color: #b0bec5; text-align: right;
            padding: 26mm 3mm 0 0;
            font-size: 5.5pt; line-height: 5.35mm;
            font-family: 'Courier New', monospace;
        }}

        .dots {{
            position: absolute; top: 10mm; left: 27mm;
            display: flex; align-items: center; gap: 6px;
        }}
        .dot {{ width: 10px; height: 10px; border-radius: 50%; }}
        .d-r {{ background: #ef4444; }}
        .d-y {{ background: #f59e0b; }}
        .d-g {{ background: #22c55e; }}
        .dots-path {{
            font-family: 'Courier New', monospace;
            font-size: 8pt; color: #64748b; margin-left: 8px;
        }}

        /* ── Layout principale ── */
        .content {{
            position: absolute;
            top: 0; left: 21mm; right: 0; bottom: 18mm;
            padding: 0 16mm;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding-top: 22mm;
            padding-bottom: 8mm;
        }}

        /* ── Glass card base ── */
        .glass-card {{
            background: var(--glass);
            border: 1px solid var(--glass-bdr);
            border-radius: 10px;
            padding: 14px 20px;
            box-shadow:
                0 4px 20px rgba(0,0,0,0.07),
                inset 0 1px 0 rgba(255,255,255,0.9);
        }}

        /* ── Card 1: header ── */
        .card-header {{ flex-shrink: 0; }}
        .header-comment {{
            font-family: 'Courier New', monospace;
            font-size: 9pt; color: #475569;
            margin-bottom: 5px;
        }}
        .import-line {{
            font-family: 'Courier New', monospace;
            font-size: 11pt; color: #1e293b;
        }}
        .kw  {{ color: var(--col-dark); font-weight: bold; }}
        .fn  {{ color: var(--col-dark); font-weight: bold; }}
        .str {{ color: #1e293b; font-style: italic; }}

        /* ── Titolo ── */
        .section-title {{ flex-shrink: 0; }}
        .title-row {{
            display: flex;
            align-items: baseline;
            gap: 12px;
            line-height: 1;
            margin-bottom: 6mm;
        }}
        .title-pro {{
            font-size: 70pt; font-weight: 900;
            letter-spacing: -2px;
            color: var(--col-dark);
        }}
        .title-python {{
            font-size: 70pt; font-weight: 900;
            letter-spacing: -2px;
            color: #0f172a;
        }}
        .vtag {{
            display: inline-block;
            font-family: 'Courier New', monospace;
            font-size: 10pt; font-weight: bold;
            padding: 6px 18px; border-radius: 6px;
            color: #fff; background: var(--grad);
            letter-spacing: 0.3px;
            box-shadow: 0 3px 14px var(--col-light);
        }}

        /* ── Card 2: descrizione ── */
        .card-desc {{ flex-shrink: 0; }}
        .desc-label {{
            font-family: 'Courier New', monospace;
            font-size: 9.5pt; color: #334155;
            margin-bottom: 6px;
        }}
        .desc-value {{
            font-family: 'Courier New', monospace;
            font-size: 11.5pt;
            color: #0f172a;
            line-height: 1.55;
        }}
        .desc-value .str {{
            color: #1e293b; font-style: normal;
        }}

        /* ── Card 3: autore ── */
        .card-author {{ flex-shrink: 0; }}
        .author-line {{
            font-family: 'Courier New', monospace;
            font-size: 10.5pt; color: #0f172a;
            margin-bottom: 8px;
        }}
        .rule {{
            height: 1.5px;
            background: linear-gradient(90deg, var(--col-dark) 0%, var(--col) 40%, transparent 80%);
            opacity: 0.4; border-radius: 2px;
            margin-bottom: 8px;
        }}
        .year-line {{
            font-family: 'Courier New', monospace;
            font-size: 10pt; color: #334155;
        }}
        .year-line .str {{ font-style: normal; color: #1e293b; }}

        /* ── Footer ── */
        .footer {{
            position: absolute;
            bottom: 6mm; left: 24mm; right: 16mm;
            border-top: 1px dashed rgba(100,116,139,0.45);
            padding-top: 2.5mm;
            font-family: 'Courier New', monospace;
            font-size: 7.5pt; color: #475569;
            display: flex; justify-content: space-between;
        }}
        .footer-status {{ color: var(--col-dark); font-weight: bold; }}
    </style>
</head>
<body>
{pages_html}
</body>
</html>
"""

with open("make_colored_vector_print.html", "w", encoding="utf-8") as f:
    f.write(html_content)

output_pdf = "Copertine_Python_Final.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_content(html_content, wait_until="networkidle")
    page.pdf(
        path=output_pdf,
        format="A4",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
    )
    browser.close()

print("PDF generato: " + output_pdf)
