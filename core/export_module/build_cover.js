const { mdToPdf } = require('md-to-pdf');
const fs = require('fs');
const path = require('path');

const coverMdPath = process.argv[2];
const outPdfPath = process.argv[3];

if (!coverMdPath || !outPdfPath) {
    console.error("Uso: node build_cover.js <cover.md> <output.pdf>");
    process.exit(1);
}

const cssPath = path.join(__dirname, 'print-style.css');
const cssContent = fs.existsSync(cssPath) ? fs.readFileSync(cssPath, 'utf8') : '';

(async () => {
    console.log(`🚀 Generando Copertina Web...`);
    try {
        await mdToPdf(
            { content: fs.readFileSync(coverMdPath, 'utf8') },
            {
                dest: outPdfPath,
                body_class: 'markdown-body',
                css: cssContent,
                as_html: false,
                launch_options: { timeout: 180000, args: ['--no-sandbox'] },
                pdf_options: {
                    format: 'A4',
                    printBackground: true,
                    displayHeaderFooter: false,
                    timeout: 180000
                }
            }
        );
        console.log(`✅ Copertina salvata in: ${outPdfPath}`);
    } catch (e) {
        console.error("❌ Errore:", e);
        process.exit(1);
    }
})();
