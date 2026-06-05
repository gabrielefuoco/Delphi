from playwright.sync_api import sync_playwright

html_content = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>PRO Python - Cyber/Dark Mode</title>
    <style>
        @page {
            size: A4;
            margin: 0;
            background-color: #09090b; /* Sfondo scuro profondo (Dark Mode) */
        }
        
        * { box-sizing: border-box; }

        body {
            margin: 0;
            padding: 0;
            font-family: 'Consolas', 'Courier New', monospace; /* Total coding font */
            color: #f8fafc;
            background-color: #09090b;
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
                linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
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
        .orb-v1 { top: -20mm; right: -20mm; width: 150mm; height: 150mm; background: linear-gradient(135deg, #2563eb, #06b6d4); }
        .orb-v2 { top: 40mm; left: -40mm; width: 180mm; height: 180mm; background: linear-gradient(135deg, #7c3aed, #db2777); }
        .orb-v3 { bottom: -20mm; right: -20mm; width: 160mm; height: 160mm; background: linear-gradient(135deg, #059669, #84cc16); opacity: 0.3; }

        /* Numeri di riga stile IDE a sinistra */
        .line-numbers {
            position: absolute;
            top: 0; left: 0; width: 15mm; height: 100%;
            background-color: rgba(255, 255, 255, 0.02);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            color: #334155;
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
        .dot-red { background-color: #ef4444; }
        .dot-yellow { background-color: #f59e0b; }
        .dot-green { background-color: #10b981; }

        /* HEADER */
        .terminal-header {
            font-size: 11pt;
            color: #64748b;
            margin-bottom: 25mm;
            margin-top: 10mm;
        }
        .keyword { color: #c678dd; } /* Pink/Purple */
        .variable { color: #e5c07b; } /* Yellow */
        .string { color: #98c379; }   /* Green */
        .function { color: #61afef; } /* Blue/Green */
        .operator { color: #56b6c2; } /* Cyan */

        /* TITOLO: Stile Monospace Gigante */
        h1 {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 60pt;
            font-weight: 900;
            letter-spacing: -3px;
            margin: 0 0 5mm 0;
            color: #ffffff;
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
            color: #09090b;
        }
        .vol-v1 { background: linear-gradient(90deg, #3b82f6, #06b6d4); box-shadow: 0 0 15px rgba(6, 182, 212, 0.4); }
        .vol-v2 { background: linear-gradient(90deg, #8b5cf6, #d946ef); box-shadow: 0 0 15px rgba(217, 70, 239, 0.4); }
        .vol-v3 { background: linear-gradient(90deg, #10b981, #a3e635); box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }

        .subtitle {
            font-size: 14pt;
            line-height: 1.6;
            color: #cbd5e1;
            max-width: 150mm;
            border-left: 3px solid rgba(255, 255, 255, 0.2);
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
            border-top: 1px dashed rgba(255, 255, 255, 0.15);
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
            <svg class="animal-svg" viewBox="0 0 100 100" fill="none" stroke="#22d3ee" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15,50 C15,25 32,15 50,15 C68,15 85,25 85,45 C85,65 68,75 50,75 C35,75 25,65 25,52 C25,38 38,30 50,30 C60,30 68,38 68,48 C68,56 58,62 50,62 C44,62 40,56 42,51 C43,46 48,46 48,49" />
                <path d="M15,50 C13,52 10,50 9,47 C8,44 10,42 13,43" />
                <path d="M9,47 L4,47 M5,45 L1,44 M5,49 L1,50" />
                <circle cx="50" cy="15" r="2" fill="#0ea5e9" /><circle cx="68" cy="15" r="1.5" fill="#0ea5e9" /><circle cx="85" cy="45" r="2" fill="#0ea5e9" />
                <path d="M28,62 L32,59 M32,66 L36,63" stroke="rgba(34, 211, 238, 0.5)" />
            </svg>
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
            <svg class="animal-svg" viewBox="0 0 100 100" fill="none" stroke="#e879f9" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M25,20 L35,27 L65,27 L75,20 L80,40 C80,65 72,82 50,82 C28,82 20,65 20,40 Z" />
                <circle cx="40" cy="42" r="8" /><circle cx="60" cy="42" r="8" />
                <circle cx="40" cy="42" r="2.5" fill="#e879f9" /><circle cx="60" cy="42" r="2.5" fill="#e879f9" />
                <path d="M47,47 L53,47 L50,56 Z" fill="#e879f9" />
                <path d="M20,45 C26,52 32,52 37,45 M80,45 C74,52 68,52 63,45" />
                <line x1="45" y1="62" x2="42" y2="65" stroke="rgba(232, 121, 249, 0.5)" /><line x1="50" y1="62" x2="47" y2="65" stroke="rgba(232, 121, 249, 0.5)" />
                <circle cx="25" cy="20" r="2" fill="#d946ef" /><circle cx="75" cy="20" r="2" fill="#d946ef" />
                <circle cx="50" cy="82" r="2" fill="#d946ef" />
            </svg>
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
            <svg class="animal-svg" viewBox="0 0 100 100" fill="none" stroke="#4ade80" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M30,38 C30,12 70,12 70,38 C70,48 64,54 50,54 C36,54 30,48 30,38 Z" />
                <circle cx="42" cy="40" r="2" fill="#4ade80" /><circle cx="58" cy="40" r="2" fill="#4ade80" />
                <path d="M40,53 C30,62 18,58 12,45 C7,35 15,22 25,28" />
                <path d="M44,54 C34,69 16,72 8,60 C3,50 11,38 22,43" />
                <path d="M47,54 C38,75 22,85 14,75 C9,67 16,54 28,56" />
                <path d="M60,53 C70,62 82,58 88,45 C93,35 85,22 75,28" />
                <path d="M56,54 C66,69 84,72 92,60 C97,50 89,38 78,43" />
                <path d="M53,54 C62,75 78,85 86,75 C91,67 84,54 72,56" />
                <circle cx="12" cy="45" r="2" fill="#22c55e" /><circle cx="8" cy="60" r="2" fill="#22c55e" /><circle cx="14" cy="75" r="2" fill="#22c55e" />
                <circle cx="88" cy="45" r="2" fill="#22c55e" /><circle cx="92" cy="60" r="2" fill="#22c55e" /><circle cx="86" cy="75" r="2" fill="#22c55e" />
            </svg>
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

with open("Copertine_Python_DarkNeon_Cyber.html", "w", encoding="utf-8") as f:
    f.write(html_content)

output_pdf = "Copertine_Python_DarkNeon_Cyber.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_content(html_content)
    page.pdf(path=output_pdf, format="A4", print_background=True)
    browser.close()

print("File generati")