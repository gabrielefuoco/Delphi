const fs = require('fs');
const path = require('path');
const { mdToPdf } = require('md-to-pdf');
const { PDFDocument } = require('pdf-lib');

// node build_pdfs.js <cover.md> <body.md> <output.pdf>
const coverMdPath = process.argv[2];
const bodyMdPath = process.argv[3];
const outPdfPath = process.argv[4];

if (!coverMdPath || !bodyMdPath || !outPdfPath) {
    console.error("Uso: node build_pdfs.js <cover.md> <body.md> <output.pdf>");
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

const protectMath = (mathStr) => {
    return mathStr
        .replace(/\\/g, '&#92;')
        .replace(/_/g, '&#95;')
        .replace(/\*/g, '&#42;')
        .replace(/~/g, '&#126;');
};

const processMarkdown = (filePath) => {
    let content = fs.readFileSync(filePath, 'utf8');
    content = content.replace(/\$\$(.*?)\$\$/gs, (match, p1) => '$$' + protectMath(p1) + '$$');
    content = content.replace(/(?<!\$)\$([^$\n]+?)\$(?!\$)/g, (match, p1) => '$' + protectMath(p1) + '$');
    return katexCssLink + '\n\n' + content;
};

(async () => {
    console.log(`\n📘 Assemblando PDF in due fasi...`);
    
    let coverMd = processMarkdown(coverMdPath);
    let bodyMd = processMarkdown(bodyMdPath);

    console.log(`🚀 Generando Copertina (Senza footer)...`);
    const coverPdfPath = outPdfPath + '.cover.pdf';
    await mdToPdf(
        { content: coverMd },
        {
            dest: coverPdfPath,
            body_class: 'markdown-body',
            css: cssContent,
            marked_options: { breaks: true },
            script: [{ content: katexRenderScript }],
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

    console.log(`🚀 Generando Corpo e Indice (Con footer)...`);
    const bodyPdfPath = outPdfPath + '.body.pdf';
    await mdToPdf(
        { content: bodyMd },
        {
            dest: bodyPdfPath,
            body_class: 'markdown-body',
            css: cssContent,
            marked_options: { breaks: true },
            script: [{ content: katexRenderScript }],
            as_html: false,
            launch_options: { timeout: 180000, args: ['--no-sandbox'] },
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

    console.log(`🔗 Unione dei PDF in corso...`);
    try {
        const coverPdfBytes = fs.readFileSync(coverPdfPath);
        const bodyPdfBytes = fs.readFileSync(bodyPdfPath);

        const pdfDoc = await PDFDocument.create();
        const coverDoc = await PDFDocument.load(coverPdfBytes);
        const bodyDoc = await PDFDocument.load(bodyPdfBytes);

        const coverPages = await pdfDoc.copyPages(coverDoc, coverDoc.getPageIndices());
        for (const page of coverPages) {
            pdfDoc.addPage(page);
        }

        const bodyPages = await pdfDoc.copyPages(bodyDoc, bodyDoc.getPageIndices());
        for (const page of bodyPages) {
            pdfDoc.addPage(page);
        }

        const mergedPdfBytes = await pdfDoc.save();
        fs.writeFileSync(outPdfPath, mergedPdfBytes);
        
        fs.unlinkSync(coverPdfPath);
        fs.unlinkSync(bodyPdfPath);

        console.log(`✅ Successo! Salvato in: ${outPdfPath}`);
    } catch (error) {
        console.error(`❌ Errore durante l'unione:`, error);
        process.exit(1);
    }
})();
