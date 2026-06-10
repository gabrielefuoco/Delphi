const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const projectDir = process.argv[2];
if (!projectDir) {
    console.error("ERRORE: Manca il path del progetto.");
    process.exit(1);
}

const chaptersDir = path.join(projectDir, 'chapters');
if (!fs.existsSync(chaptersDir)) {
    console.log("Nessuna cartella chapters trovata, skip validazione.");
    process.exit(0);
}

function findMdFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const filePath = path.join(dir, file);
        if (fs.statSync(filePath).isDirectory()) {
            findMdFiles(filePath, fileList);
        } else if (filePath.endsWith('.md')) {
            fileList.push(filePath);
        }
    }
    return fileList;
}

const mdFiles = findMdFiles(chaptersDir);
let allMermaidBlocks = [];

for (const file of mdFiles) {
    const content = fs.readFileSync(file, 'utf8');
    const regex = /```mermaid\r?\n([\s\S]*?)```/g;
    let match;
    while ((match = regex.exec(content)) !== null) {
        allMermaidBlocks.push({ file, code: match[1] });
    }
}

if (allMermaidBlocks.length === 0) {
    console.log("Nessun blocco mermaid trovato.");
    process.exit(0);
}

(async () => {
    let browser;
    try {
        browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
    } catch(e) {
        // Fallback per vecchie versioni di puppeteer
        browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
    }
    const page = await browser.newPage();

    const html = `
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    </head>
    <body>
        <script>
            mermaid.initialize({ startOnLoad: false });
        </script>
    </body>
    </html>
    `;
    await page.setContent(html);

    let hasError = false;

    console.log(`Validazione di ${allMermaidBlocks.length} diagrammi Mermaid in corso...`);

    for (let i = 0; i < allMermaidBlocks.length; i++) {
        const block = allMermaidBlocks[i];
        try {
            const isSyntaxValid = await page.evaluate(async (code) => {
                try {
                    await mermaid.parse(code);
                    return true;
                } catch(e) {
                    return e.message || String(e);
                }
            }, block.code);

            if (isSyntaxValid !== true) {
                console.error(`\n========================================`);
                console.error(`❌ MERMAID SYNTAX ERROR`);
                console.error(`File: ${block.file}`);
                console.error(`Errore:\n${isSyntaxValid}`);
                console.error(`========================================\n`);
                hasError = true;
            }
        } catch (e) {
             console.error(`❌ MERMAID EVAL ERROR in ${block.file}:`, e);
             hasError = true;
        }
    }

    await browser.close();

    if (hasError) {
        console.error("❌ Validazione fallita: trovati errori di sintassi nei diagrammi Mermaid.");
        process.exit(1);
    } else {
        console.log("✅ Tutti i diagrammi Mermaid sono validi.");
        process.exit(0);
    }
})();
