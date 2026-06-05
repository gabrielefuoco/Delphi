const fs = require('fs');
const path = require('path');
const { mdToPdf } = require('md-to-pdf');

// Legge i percorsi da linea di comando:
// node build_pdfs.js <input.md> <output.pdf>
const inputMdPath = process.argv[2];
const outPdfPath = process.argv[3];

if (!inputMdPath || !outPdfPath) {
    console.error("Uso: node build_pdfs.js <input.md> <output.pdf>");
    process.exit(1);
}

const cssPath = path.join(__dirname, 'print-style.css');
const cssContent = fs.existsSync(cssPath) ? fs.readFileSync(cssPath, 'utf8') : '';

// KaTeX CSS
const katexCssLink = `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">`;

// KaTeX Render Script
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
    console.log(`\n📘 Assemblando PDF da: ${inputMdPath}`);
    
    let content = fs.readFileSync(inputMdPath, 'utf8');
    
    // Protezione Formule Matematiche:
    // Evitiamo che il parser Markdown trasformi gli underscore (_) in corsivi (<em>)
    // o i doppi backslash (\\) in singoli, distruggendo la sintassi KaTeX.
    // Sostituiamo questi caratteri critici con HTML entities, che il DOM decodificherà 
    // automaticamente prima che KaTeX li legga.
    const protectMath = (mathStr) => {
        return mathStr
            .replace(/\\/g, '&#92;')
            .replace(/_/g, '&#95;')
            .replace(/\*/g, '&#42;')
            .replace(/~/g, '&#126;');
    };

    content = content.replace(/\$\$(.*?)\$\$/gs, (match, p1) => '$$' + protectMath(p1) + '$$');
    content = content.replace(/(?<!\$)\$([^$\n]+?)\$(?!\$)/g, (match, p1) => '$' + protectMath(p1) + '$');

    let mergedMarkdown = katexCssLink + '\n\n' + content;

    console.log(`🚀 Generando il PDF...`);
    
    try {
        await mdToPdf(
            { content: mergedMarkdown },
            {
                dest: outPdfPath,
                body_class: 'markdown-body',
                css: cssContent,
                marked_options: {
                    breaks: true
                },
                script: [{
                    content: katexRenderScript
                }],
                as_html: false,
                launch_options: { 
                    timeout: 180000,
                    args: ['--no-sandbox']
                },
                pdf_options: {
                    format: 'A4',
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
        console.error(`❌ Errore durante la generazione:`, error);
        process.exit(1);
    }
})();
