const fs = require('fs');
const path = require('path');
const { mdToPdf } = require('md-to-pdf');

const baseDir = path.join('c:', 'Users', 'gabri', 'APP', 'Indice studi');
const vols = ['vol 1', 'vol 2', 'vol 3'];
const cssPath = path.join(__dirname, 'print-style.css');
const cssContent = fs.readFileSync(cssPath, 'utf8');

// KaTeX CSS caricato come stylesheet nel <head>
const katexCssLink = `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">`;

// Script che verrà eseguito DOPO il rendering HTML, PRIMA della stampa PDF.
// md-to-pdf inietta questo script e aspetta che finisca prima di stampare.
const katexRenderScript = `
const katexScript = document.createElement('script');
katexScript.src = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js';
document.head.appendChild(katexScript);

katexScript.onload = () => {
    const autoRenderScript = document.createElement('script');
    autoRenderScript.src = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js';
    document.head.appendChild(autoRenderScript);

    autoRenderScript.onload = () => {
        renderMathInElement(document.body, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\\\(', right: '\\\\)', display: false},
                {left: '\\\\[', right: '\\\\]', display: true}
            ],
            throwOnError: false
        });
    };
};
`;

(async () => {
    for (const vol of vols) {
        console.log(`\n📘 Assemblando ${vol}...`);
        const volDir = path.join(baseDir, vol);
        
        const files = fs.readdirSync(volDir).filter(f => f.endsWith('.md') && f.startsWith('appunti_p'));
        
        files.sort((a, b) => {
            const numA = parseInt(a.match(/\d+/)[0]);
            const numB = parseInt(b.match(/\d+/)[0]);
            return numA - numB;
        });

        // Prepend il link CSS di KaTeX come HTML grezzo nel markdown
        let mergedMarkdown = katexCssLink + '\n\n';
        for (const file of files) {
            const filePath = path.join(volDir, file);
            let content = fs.readFileSync(filePath, 'utf8');
            mergedMarkdown += content + '\n\n';
        }

        const outPdfPath = path.join(baseDir, `${vol.toUpperCase()}.pdf`);
        const outHtmlPath = path.join(baseDir, `${vol.toUpperCase()}_DEBUG.html`);
        
        // Salva anche l'HTML intermedio per debug/ispezione
        try {
            const result = await mdToPdf(
                { content: mergedMarkdown },
                {
                    body_class: 'markdown-body',
                    css: cssContent,
                    marked_options: { breaks: true },
                    script: [{ content: katexRenderScript }],
                    launch_options: { timeout: 180000, args: ['--no-sandbox'] },
                    as_html: true  // Genera HTML invece di PDF
                }
            );
            fs.writeFileSync(outHtmlPath, result.content, 'utf8');
            console.log(`📄 HTML di debug salvato in: ${outHtmlPath}`);
        } catch (e) {
            console.error(`⚠️ Errore nel salvataggio HTML debug per ${vol}:`, e.message);
        }
        
        console.log(`🚀 Generando il PDF per ${vol} (Timeout esteso a 3 minuti)...`);
        
        try {
            await mdToPdf(
                { content: mergedMarkdown },
                {
                    dest: outPdfPath,
                    body_class: 'markdown-body',
                    css: cssContent,
                    // CRITICO: Abilitare breaks per rispettare i newline singoli
                    marked_options: {
                        breaks: true
                    },
                    // CRITICO: Script iniettato nella pagina ed eseguito PRIMA della stampa
                    script: [{
                        content: katexRenderScript
                    }],
                    // Aspetta che la rete sia ferma (= KaTeX ha finito di scaricarsi e renderizzare)
                    as_html: false,
                    launch_options: { 
                        timeout: 180000,
                        args: ['--no-sandbox']
                    },
                    pdf_options: {
                        format: 'A4',
                        margin: { top: '25mm', right: '25mm', bottom: '25mm', left: '25mm' },
                        printBackground: true,
                        displayHeaderFooter: true,
                        footerTemplate: `
                            <div style="width: 100%; font-size: 10px; font-family: sans-serif; text-align: center; color: #555;">
                                <span class="pageNumber"></span> / <span class="totalPages"></span>
                            </div>
                        `,
                        headerTemplate: '<span></span>',
                        timeout: 180000
                    }
                }
            );
            console.log(`✅ Successo! Salvato in: ${outPdfPath}`);
        } catch (error) {
            console.error(`❌ Errore durante la generazione di ${vol}:`, error);
        }
    }
})();
