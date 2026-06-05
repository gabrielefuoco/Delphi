import base64
import os
from playwright.sync_api import sync_playwright

def get_base64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

b64_python = get_base64("python.png")
b64_octopus = get_base64("octopus.png")
b64_owl = get_base64("owl.png")

html_content = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>PRO Python - Print Colored Mode</title>
    <style>
        @page {{
            size: A4;
            margin: 0;
            background-color: transparent;
        }}
        
        * {{ box-sizing: border-box; }}

        body {{
            margin: 0;
            padding: 0;
            font-family: 'Consolas', 'Courier New', monospace;
            color: #0f172a;
            background-color: transparent;
        }}

        .page {{
            position: relative;
            width: 210mm;
            height: 297mm;
            padding: 30mm 20mm 30mm 35mm;
            page-break-after: always;
            overflow: hidden;
            z-index: 1;
        }}
        .page:last-child {{ page-break-after: avoid; }}

        /* Primary Colors per Page */
        .page-v1 {{ --primary: #0284c7; --primary-light: rgba(2, 132, 199, 0.1); --primary-grad: linear-gradient(135deg, #0284c7, #38bdf8); }}
        .page-v2 {{ --primary: #9333ea; --primary-light: rgba(147, 51, 234, 0.1); --primary-grad: linear-gradient(135deg, #9333ea, #c084fc); }}
        .page-v3 {{ --primary: #059669; --primary-light: rgba(5, 150, 105, 0.1); --primary-grad: linear-gradient(135deg, #059669, #34d399); }}

        /* Griglia tech elegante */
        .cyber-grid {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient(var(--primary-light) 1px, transparent 1px),
                linear-gradient(90deg, var(--primary-light) 1px, transparent 1px);
            background-size: 10mm 10mm;
            z-index: -2;
        }}

        /* Sfere di luce colorate ma delicate */
        .glow-orb {{
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            z-index: -1;
            opacity: 0.35;
            background: var(--primary-grad);
        }}
        
        .orb-1 {{ top: -20mm; right: -20mm; width: 160mm; height: 160mm; }}
        .orb-2 {{ bottom: 40mm; left: -40mm; width: 180mm; height: 180mm; }}

        /* Numeri di riga stile IDE a sinistra */
        .line-numbers {{
            position: absolute;
            top: 0; left: 0; width: 15mm; height: 100%;
            background-color: rgba(0, 0, 0, 0.02);
            border-right: 2px solid var(--primary);
            color: #64748b;
            text-align: right;
            padding-top: 30mm;
            padding-right: 3mm;
            font-size: 7pt;
            line-height: 5.5mm;
            user-select: none;
            opacity: 0.8;
        }}

        /* IDE Window Buttons */
        .window-controls {{
            position: absolute;
            top: 15mm; left: 25mm;
            display: flex;
            gap: 6px;
        }}
        .dot {{ width: 10px; height: 10px; border-radius: 50%; }}
        .dot-red {{ background-color: #ef4444; }}
        .dot-yellow {{ background-color: #f59e0b; }}
        .dot-green {{ background-color: #10b981; }}

        /* HEADER */
        .terminal-header {{
            font-size: 11pt;
            color: #475569;
            margin-bottom: 25mm;
            margin-top: 10mm;
        }}
        
        /* Sintassi base per print */
        .keyword {{ color: var(--primary); font-weight: bold; }}
        .variable {{ color: #0f172a; font-weight: bold; }}
        .string {{ color: #475569; font-style: italic; }}
        .function {{ color: var(--primary); font-weight: bold; text-decoration: underline; text-decoration-color: var(--primary-light); text-decoration-thickness: 2px; }}
        .operator {{ color: #334155; }}

        /* TITOLO: Stile Monospace Gigante */
        h1 {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 60pt;
            font-weight: 900;
            letter-spacing: -3px;
            margin: 0 0 5mm 0;
            color: #0f172a;
            position: relative;
        }}

        /* Tag Volume Elegante */
        .volume-tag {{
            display: inline-block;
            font-family: 'Consolas', monospace;
            font-size: 18pt;
            font-weight: 700;
            padding: 6px 18px;
            border-radius: 8px;
            margin-bottom: 15mm;
            color: #ffffff;
            background: var(--primary-grad);
            box-shadow: 0 4px 15px var(--primary-light);
            border: 1px solid rgba(255,255,255,0.4);
        }}

        .subtitle {{
            font-size: 14pt;
            line-height: 1.6;
            color: #334155;
            max-width: 150mm;
            border-left: 4px solid var(--primary);
            padding-left: 15px;
            background: rgba(255, 255, 255, 0.5);
            padding: 10px 15px;
            border-radius: 0 8px 8px 0;
        }}

        /* Illustrazione Base64 */
        .illustration-container {{
            position: absolute;
            top: 155mm;
            left: 45mm;
            width: 130mm;
            height: 100mm;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .animal-img {{ 
            width: 100%; 
            height: 100%; 
            object-fit: contain; 
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1)) contrast(1.1);
        }}
        
        /* Un accento per unire il disegno al tema */
        .illustration-accent {{
            position: absolute;
            bottom: -5mm;
            right: 0;
            width: 40mm;
            height: 4mm;
            background: var(--primary-grad);
            border-radius: 4px;
            opacity: 0.8;
        }}

        /* Blocco Autore: JSON Format */
        .author-box {{
            position: absolute;
            bottom: 30mm;
            left: 35mm;
            font-size: 11pt;
            line-height: 1.6;
            background: rgba(255, 255, 255, 0.7);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid var(--primary-light);
        }}

        .footer {{
            position: absolute;
            bottom: 15mm; left: 35mm; right: 20mm;
            border-top: 1px dashed var(--primary);
            padding-top: 4mm;
            font-size: 8pt;
            color: #475569;
            display: flex;
            justify-content: space-between;
        }}
    </style>
</head>
<body>

    <!-- VOL 1 -->
    <div class="page page-v1">
        <div class="cyber-grid"></div>
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="line-numbers">
            1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15<br>16<br>17<br>18<br>19<br>20<br>21<br>22<br>23<br>24<br>25<br>26<br>27<br>28<br>29<br>30<br>31<br>32<br>33<br>34<br>35<br>36<br>37<br>38<br>39<br>40
        </div>
        
        <div class="window-controls">
            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
        </div>

        <div class="terminal-header">
            <span class="keyword">from</span> system.core <span class="keyword">import</span> knowledge
        </div>

        <h1>PRO Python</h1>
        <div class="volume-tag">{{"volume": 1}}</div>

        <div class="subtitle">
            <span class="operator">#</span> Architettura CPython, Clean Code e Algoritmi Avanzati<br>
            <span class="keyword">class</span> <span class="variable">Architecture</span>(Base):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;complexity = <span class="string">"O(N log N)"</span>
        </div>

        <div class="illustration-container">
            <img src="{b64_python}" class="animal-img" />
            <div class="illustration-accent"></div>
        </div>

        <div class="author-box">
            <span class="keyword">const</span> author = {{<br>
            &nbsp;&nbsp;<span class="function">"name"</span>: <span class="string">"Gabriele Fuoco"</span>,<br>
            &nbsp;&nbsp;<span class="function">"role"</span>: <span class="string">"Software Engineer"</span><br>
            }};
        </div>

        <div class="footer">
            <span>[Status: RUNNING]</span>
            <span>Edizione 2026</span>
        </div>
    </div>

    <!-- VOL 2 -->
    <div class="page page-v2">
        <div class="cyber-grid"></div>
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="line-numbers">
            1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15<br>16<br>17<br>18<br>19<br>20<br>21<br>22<br>23<br>24<br>25<br>26<br>27<br>28<br>29<br>30<br>31<br>32<br>33<br>34<br>35<br>36<br>37<br>38<br>39<br>40
        </div>
        
        <div class="window-controls">
            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
        </div>

        <div class="terminal-header">
            <span class="keyword">import</span> {{ cluster }} <span class="keyword">from</span> '@distributed/nodes';
        </div>

        <h1>PRO Python</h1>
        <div class="volume-tag">{{"volume": 2}}</div>

        <div class="subtitle">
            <span class="operator">#</span> Architetture Distribuite, System Design e Infrastruttura Scale-Out<br>
            <span class="keyword">async def</span> <span class="function">deploy_cluster</span>():<br>
            &nbsp;&nbsp;&nbsp;&nbsp;<span class="keyword">await</span> network.sync_raft()
        </div>

        <div class="illustration-container">
            <img src="{b64_octopus}" class="animal-img" />
            <div class="illustration-accent"></div>
        </div>

        <div class="author-box">
            <span class="keyword">const</span> author = {{<br>
            &nbsp;&nbsp;<span class="function">"name"</span>: <span class="string">"Gabriele Fuoco"</span>,<br>
            &nbsp;&nbsp;<span class="function">"role"</span>: <span class="string">"Cloud Architect"</span><br>
            }};
        </div>

        <div class="footer">
            <span>[Status: ALL_NODES_SYNCED]</span>
            <span style="float:right">Edizione 2026</span>
        </div>
    </div>

    <!-- VOL 3 -->
    <div class="page page-v3">
        <div class="cyber-grid"></div>
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="line-numbers">
            1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15<br>16<br>17<br>18<br>19<br>20<br>21<br>22<br>23<br>24<br>25<br>26<br>27<br>28<br>29<br>30<br>31<br>32<br>33<br>34<br>35<br>36<br>37<br>38<br>39<br>40
        </div>
        
        <div class="window-controls">
            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
        </div>

        <div class="terminal-header">
            <span class="keyword">use</span> std::ai::tensor_processing;
        </div>

        <h1>PRO Python</h1>
        <div class="volume-tag">{{"volume": 3}}</div>

        <div class="subtitle">
            <span class="operator">#</span> AI Engineering, Big Data, Generative AI e Modelli MLOps<br>
            <span class="keyword">def</span> <span class="function">forward_pass</span>(tokens):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;<span class="keyword">return</span> Transformer.attention(tokens)
        </div>

        <div class="illustration-container">
            <img src="{b64_owl}" class="animal-img" />
            <div class="illustration-accent"></div>
        </div>

        <div class="author-box">
            <span class="keyword">const</span> author = {{<br>
            &nbsp;&nbsp;<span class="function">"name"</span>: <span class="string">"Gabriele Fuoco"</span>,<br>
            &nbsp;&nbsp;<span class="function">"role"</span>: <span class="string">"AI Engineer"</span><br>
            }};
        </div>

        <div class="footer">
            <span>[Status: MODEL_CONVERGED]</span>
            <span style="float:right">Edizione 2026</span>
        </div>
    </div>

</body>
</html>
"""

with open("make_colored_print.html", "w", encoding="utf-8") as f:
    f.write(html_content)

output_pdf = "Copertine_Python_ColoredPrint.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_content(html_content)
    # wait a moment for base64 images to fully decode and paint
    page.wait_for_timeout(500) 
    page.pdf(path=output_pdf, format="A4", print_background=True)
    browser.close()

print("File PDF Colorato generato con successo!")
