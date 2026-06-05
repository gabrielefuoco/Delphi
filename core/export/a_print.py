from playwright.sync_api import sync_playwright

html_content = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>PRO Python - Light/Print Mode</title>
    <style>
        @page {
            size: A4;
            margin: 0;
            background-color: transparent; /* Sfondo scuro profondo (Dark Mode) */
        }
        
        * { box-sizing: border-box; }

        body {
            margin: 0;
            padding: 0;
            font-family: 'Consolas', 'Courier New', monospace; /* Total coding font */
            color: #000000;
            background-color: transparent;
        }

        .page {
            position: relative;
            width: 210mm;
            height: 297mm;
            padding: 30mm 20mm 30mm 35mm;
            page-break-after: always;
            overflow: hidden;
            z-index: 1;
        }
        .page:last-child { page-break-after: avoid; }

        /* Griglia tech scura al neon */
        .cyber-grid {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient(rgba(0, 0, 0, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 0, 0, 0.05) 1px, transparent 1px);
            background-size: 10mm 10mm;
            z-index: -2;
        }

        /* Sfere di luce (Gradients) per dare profondità e modernità */
        .glow-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            z-index: -1;
            opacity: 0.4;
        }
        
        /* Orb colori per ogni volume */
        .orb-v1 { top: -20mm; right: -20mm; width: 150mm; height: 150mm; background: linear-gradient(135deg, #e2e8f0, #f8fafc); }
        .orb-v2 { top: 40mm; left: -40mm; width: 180mm; height: 180mm; background: linear-gradient(135deg, #cbd5e1, #f1f5f9); }
        .orb-v3 { bottom: -20mm; right: -20mm; width: 160mm; height: 160mm; background: linear-gradient(135deg, #94a3b8, #e2e8f0); opacity: 0.3; }

        /* Numeri di riga stile IDE a sinistra */
        .line-numbers {
            position: absolute;
            top: 0; left: 0; width: 15mm; height: 100%;
            background-color: rgba(0, 0, 0, 0.02);
            border-right: 1px solid rgba(0, 0, 0, 0.1);
            color: #94a3b8;
            text-align: right;
            padding-top: 30mm;
            padding-right: 3mm;
            font-size: 7pt;
            line-height: 5.5mm;
            user-select: none;
        }

        /* IDE Window Buttons */
        .window-controls {
            position: absolute;
            top: 15mm; left: 25mm;
            display: flex;
            gap: 6px;
        }
        .dot { width: 10px; height: 10px; border-radius: 50%; }
        .dot-red { background-color: #334155; }
        .dot-yellow { background-color: #94a3b8; }
        .dot-green { background-color: #475569; }

        /* HEADER */
        .terminal-header {
            font-size: 11pt;
            color: #475569;
            margin-bottom: 25mm;
            margin-top: 10mm;
        }
        .keyword { color: #000000; font-weight: bold; } /* Pink/Purple */
        .variable { color: #333333; } /* Yellow */
        .string { color: #475569; font-style: italic; }   /* Green */
        .function { color: #0f172a; font-weight: bold; } /* Blue/Green */
        .operator { color: #000000; } /* Cyan */

        /* TITOLO: Stile Monospace Gigante */
        h1 {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 60pt;
            font-weight: 900;
            letter-spacing: -3px;
            margin: 0 0 5mm 0;
            color: #000000;
            position: relative;
        }

        /* Tag Volume Neon */
        .volume-tag {
            display: inline-block;
            font-family: 'Consolas', monospace;
            font-size: 18pt;
            font-weight: 700;
            padding: 4px 15px;
            border-radius: 4px;
            margin-bottom: 15mm;
            color: #ffffff;
        }
        .vol-v1 { background: linear-gradient(90deg, #64748b, #94a3b8); box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        .vol-v2 { background: linear-gradient(90deg, #475569, #64748b); box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        .vol-v3 { background: linear-gradient(90deg, #334155, #475569); box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }

        .subtitle {
            font-size: 14pt;
            line-height: 1.6;
            color: #334155;
            max-width: 150mm;
            border-left: 3px solid rgba(0, 0, 0, 0.2);
            padding-left: 15px;
        }

        /* Animale SVG Centrato, colori Neon */
        .illustration-container {
            position: absolute;
            top: 155mm;
            left: 45mm;
            width: 120mm;
            height: 90mm;
        }
        .animal-svg { width: 100%; height: 100%; }

        /* Blocco Autore: JSON Format */
        .author-box {
            position: absolute;
            bottom: 30mm;
            left: 35mm;
            font-size: 11pt;
            line-height: 1.6;
        }

        .footer {
            position: absolute;
            bottom: 15mm; left: 35mm; right: 20mm;
            border-top: 1px dashed rgba(0, 0, 0, 0.2);
            padding-top: 4mm;
            font-size: 8pt;
            color: #475569;
            display: flex;
            justify-content: space-between;
        }
    </style>
</head>
<body>

    <!-- VOL 1 -->
    <div class="page">
        <div class="cyber-grid"></div>
        <div class="glow-orb orb-v1"></div>
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
        <div class="volume-tag vol-v1">{"volume": 1}</div>

        <div class="subtitle">
            <span class="operator">#</span> Architettura CPython, Clean Code e Algoritmi Avanzati<br>
            <span class="keyword">class</span> <span class="variable">Architecture</span>(Base):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;complexity = <span class="string">"O(N log N)"</span>
        </div>

        <div class="illustration-container">
            <img src="file:///c:/Users/gabri/APP/copertina/python.png" style="width: 100%; height: 100%; object-fit: contain;" />
        </div>

        <div class="author-box">
            <span class="keyword">const</span> author = {<br>
            &nbsp;&nbsp;<span class="function">"name"</span>: <span class="string">"Gabriele Fuoco"</span>,<br>
            &nbsp;&nbsp;<span class="function">"role"</span>: <span class="string">"Software Engineer"</span><br>
            };
        </div>

        <div class="footer">
            <span>[Status: RUNNING]</span>
            <span>Edizione 2026</span>
        </div>
    </div>

    <!-- VOL 2 -->
    <div class="page">
        <div class="cyber-grid"></div>
        <div class="glow-orb orb-v2"></div>
        <div class="line-numbers">
            1<br>2<br>3<br>4<br>5<br>6<br>7<br>8<br>9<br>10<br>11<br>12<br>13<br>14<br>15<br>16<br>17<br>18<br>19<br>20<br>21<br>22<br>23<br>24<br>25<br>26<br>27<br>28<br>29<br>30<br>31<br>32<br>33<br>34<br>35<br>36<br>37<br>38<br>39<br>40
        </div>
        
        <div class="window-controls">
            <div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div>
        </div>

        <div class="terminal-header">
            <span class="keyword">import</span> { cluster } <span class="keyword">from</span> '@distributed/nodes';
        </div>

        <h1>PRO Python</h1>
        <div class="volume-tag vol-v2">{"volume": 2}</div>

        <div class="subtitle">
            <span class="operator">#</span> Architetture Distribuite, System Design e Infrastruttura Scale-Out<br>
            <span class="keyword">async def</span> <span class="function">deploy_cluster</span>():<br>
            &nbsp;&nbsp;&nbsp;&nbsp;<span class="keyword">await</span> network.sync_raft()
        </div>

        <div class="illustration-container">
            <img src="file:///c:/Users/gabri/APP/copertina/octopus.png" style="width: 100%; height: 100%; object-fit: contain;" />
        </div>

        <div class="author-box">
            <span class="keyword">const</span> author = {<br>
            &nbsp;&nbsp;<span class="function">"name"</span>: <span class="string">"Gabriele Fuoco"</span>,<br>
            &nbsp;&nbsp;<span class="function">"role"</span>: <span class="string">"Cloud Architect"</span><br>
            };
        </div>

        <div class="footer">
            <span>[Status: ALL_NODES_SYNCED]</span>
            <span style="float:right">Edizione 2026</span>
        </div>
    </div>

    <!-- VOL 3 -->
    <div class="page">
        <div class="cyber-grid"></div>
        <div class="glow-orb orb-v3"></div>
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
        <div class="volume-tag vol-v3">{"volume": 3}</div>

        <div class="subtitle">
            <span class="operator">#</span> AI Engineering, Big Data, Generative AI e Modelli MLOps<br>
            <span class="keyword">def</span> <span class="function">forward_pass</span>(tokens):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;<span class="keyword">return</span> Transformer.attention(tokens)
        </div>

        <div class="illustration-container">
            <img src="file:///c:/Users/gabri/APP/copertina/owl.png" style="width: 100%; height: 100%; object-fit: contain;" />
        </div>

        <div class="author-box">
            <span class="keyword">const</span> author = {<br>
            &nbsp;&nbsp;<span class="function">"name"</span>: <span class="string">"Gabriele Fuoco"</span>,<br>
            &nbsp;&nbsp;<span class="function">"role"</span>: <span class="string">"AI Engineer"</span><br>
            };
        </div>

        <div class="footer">
            <span>[Status: MODEL_CONVERGED]</span>
            <span style="float:right">Edizione 2026</span>
        </div>
    </div>

</body>
</html>
"""

with open("Copertine_Python_Print.html", "w", encoding="utf-8") as f:
    f.write(html_content)

output_pdf = "Copertine_Python_Print.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_content(html_content)
    page.pdf(path=output_pdf, format="A4", print_background=True)
    browser.close()

print("File generati")