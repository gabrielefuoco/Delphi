const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const buildDir = process.argv[2];
if (!buildDir) {
    console.error("ERRORE: Manca il path della cartella .build.");
    process.exit(1);
}

const bodyMdPath = path.join(buildDir, 'web_body.md');
if (!fs.existsSync(bodyMdPath)) {
    console.log("Nessun web_body.md trovato.");
    process.exit(0);
}

const mermaidDir = path.join(buildDir, 'mermaid');
if (!fs.existsSync(mermaidDir)) {
    fs.mkdirSync(mermaidDir, { recursive: true });
}

let content = fs.readFileSync(bodyMdPath, 'utf8');

// Regex per estrarre blocchi mermaid
const regex = /```mermaid\r?\n([\s\S]*?)```/g;
let match;
const blocks = [];
while ((match = regex.exec(content)) !== null) {
    blocks.push({
        fullText: match[0],
        code: match[1]
    });
}

if (blocks.length === 0) {
    console.log("Nessun diagramma Mermaid da pre-renderizzare.");
    process.exit(0);
}

(async () => {
    const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
    const page = await browser.newPage();
    
    // Inietta Mermaid v10
    await page.setContent(`
        <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
            </head>
            <body></body>
        </html>
    `);

    const themeArg = process.argv[3] || 'default';
    
    // Inizializza mermaid con il tema richiesto e lo stesso font usato nel PDF
    await page.evaluate((theme) => {
        let mermaidConfig = { 
            startOnLoad: false, 
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"'
        };
        
        if (theme === 'bw') {
            mermaidConfig.theme = 'base';
            mermaidConfig.themeVariables = {
                primaryColor: '#fafafa',       // Colore chiarissimo per i contenitori
                primaryTextColor: '#111111',   // Testo scuro dentro i contenitori
                primaryBorderColor: '#444444', // Bordo scuro
                lineColor: '#333333',          // Linee di collegamento scure
                secondaryColor: '#f4f4f4',
                tertiaryColor: '#eaeaea',
                nodeBorder: '#444444',
                clusterBkg: '#ffffff',         // Sfondo trasparente/bianco per i cluster
                clusterBorder: '#666666',
                // Variabili per sequenceDiagram e note
                noteBkgColor: '#fafafa',
                noteTextColor: '#111111',
                noteBorderColor: '#444444',
                noteBkg: '#fafafa',
                actorBkg: '#fafafa',
                actorBorder: '#444444',
                actorTextColor: '#111111',
                signalColor: '#333333',
                signalTextColor: '#111111',
                stateBkg: '#fafafa',
                stateBorder: '#444444',
                stateLabelColor: '#111111',
                altBackground: '#ffffff'
            };
        } else {
            mermaidConfig.theme = theme;
        }
        
        mermaid.initialize(mermaidConfig);
    }, themeArg);

    let modifiedContent = content;

    for (let i = 0; i < blocks.length; i++) {
        const block = blocks[i];
        
        let codeToRender = block.code;
        if (themeArg === 'bw') {
            // Rimuoviamo gli stili inline (colori hardcoded) per forzare il tema B&W
            codeToRender = codeToRender.replace(/^[ \t]*(style|classDef|class|linkStyle)[ \t]+.*$/gm, '');
        }
        
        try {
            const resultObj = await page.evaluate(async (code, id) => {
                const { svg } = await mermaid.render('mermaid-' + id, code);
                
                // Creiamo un div temporaneo per ispezionare l'SVG
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = svg;
                document.body.appendChild(tempDiv);
                
                const nodeCount = tempDiv.querySelectorAll('.node, .cluster, foreignObject').length || 1;
                const textNodes = tempDiv.querySelectorAll('text, foreignObject');
                let textLength = 0;
                textNodes.forEach(t => { textLength += (t.textContent || '').trim().length; });
                
                document.body.removeChild(tempDiv);
                
                return { svg, nodeCount, textLength };
            }, codeToRender, i);

            const result = resultObj.svg;
            const nodeCount = resultObj.nodeCount;
            const textLength = resultObj.textLength;

            // Estrai viewBox per controllare le dimensioni originali calcolate
            let w = 800, h = 600;
            const viewBoxMatch = result.match(/viewBox="([^"]+)"/);
            if (viewBoxMatch) {
                const parts = viewBoxMatch[1].split(' ');
                w = parseFloat(parts[2]) || w;
                h = parseFloat(parts[3]) || h;
                
                if (w > 1000 || h > 1000) {
                    console.warn(`\n[WARNING] Diagramma Mermaid ${i} ha dimensioni estreme (L: ${w}px, A: ${h}px).`);
                    console.warn(`Verra' eseguito un resize forzato proporzionale.`);
                    console.warn(`Codice incriminato:\n${block.code.split('\n')[0]} ...`);
                }
            }

            // Calcolo Dimensione Giustificata
            let maxJustifiedWidth = (nodeCount * 100) + (textLength * 5);
            let targetW = Math.min(w * 0.8, maxJustifiedWidth);
            
            // Console log per debug delle scelte del motore
            if (targetW < w * 0.8) {
                console.log(`[INFO] Diagramma ${i} compattato intelligentemente: viewBox ${w}px -> target ${targetW.toFixed(0)}px (Nodi: ${nodeCount}, Testo: ${textLength})`);
            }

            // Restrizione per altezza massima (abbassata a 600px per i diagrammi verticali)
            if (h * (targetW / w) > 600) {
                targetW = w * (600 / h);
            }

            // Puliamo il tag SVG nativo da style e width/height in conflitto, SOLO sul tag radice <svg>!
            // Non usare espressioni regolari globali su tutto l'SVG altrimenti si distruggono i nodi!
            let finalSvg = result.replace(/<svg([^>]*)>/, (match, attrs) => {
                let newAttrs = attrs.replace(/width="[^"]*"/, '')
                                    .replace(/height="[^"]*"/, '')
                                    .replace(/style="[^"]*"/, '');
                return `<svg width="100%" height="auto" style="display: block;" ${newAttrs}>`;
            });
            
            // Creiamo un wrapper che forza la scala proporzionale
            const replacement = `\n\n<div class="mermaid-container" style="display: flex; justify-content: center; margin: 25px 0;">
<div style="width: 100%; max-width: ${targetW}px;">
${finalSvg}
</div>
</div>\n\n`;
            
            modifiedContent = modifiedContent.replace(block.fullText, replacement);

        } catch (e) {
            console.error(`Errore nel pre-rendering del diagramma ${i}:`, e.message);
        }
    }

    fs.writeFileSync(bodyMdPath, modifiedContent, 'utf8');
    await browser.close();
    console.log(`\n✅ Pre-rendering di ${blocks.length} diagrammi completato con successo.`);
})();
