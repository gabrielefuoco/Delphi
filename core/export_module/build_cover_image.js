const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const coverHtmlPath = process.argv[2];
const outImagePath = process.argv[3];

if (!coverHtmlPath || !outImagePath) {
    console.error("Uso: node build_cover_image.js <cover.html> <output.png>");
    process.exit(1);
}

const cssPath = path.join(__dirname, 'print-style.css');
const cssContent = fs.existsSync(cssPath) ? fs.readFileSync(cssPath, 'utf8') : '';

(async () => {
    console.log(`🚀 Generando Immagine Copertina per EPUB...`);
    try {
        const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
        const page = await browser.newPage();
        
        // Standard EPUB cover ratio (1:1.6) -> 800x1280
        await page.setViewport({ width: 800, height: 1280, deviceScaleFactor: 3 });

        let htmlContent = fs.readFileSync(coverHtmlPath, 'utf8');
        let fullHtml = `
<!DOCTYPE html>
<html>
<head>
    <style>${cssContent}</style>
    <style>
        body, html { margin: 0; padding: 0; width: 800px; height: 1280px; overflow: hidden; background: white; }
        .markdown-body { margin: 0; padding: 0; height: 100%; width: 100%; }
        /* Forza la copertina ad occupare tutto lo spazio ignorando limiti rigidi */
        .cover-page, .page.theme-ide { 
            width: 100% !important; 
            height: 100% !important; 
            max-width: none !important;
            max-height: none !important;
            box-sizing: border-box; 
            page-break-after: avoid !important; 
        }
    </style>
</head>
<body class="markdown-body">
    ${htmlContent}
</body>
</html>
`;
        await page.setContent(fullHtml, { waitUntil: 'networkidle0' });
        await page.screenshot({ path: outImagePath, type: 'png' });
        
        await browser.close();
        console.log(`✅ Immagine copertina salvata in: ${outImagePath}`);
    } catch (e) {
        console.error("❌ Errore nella generazione dell'immagine:", e);
        process.exit(1);
    }
})();
