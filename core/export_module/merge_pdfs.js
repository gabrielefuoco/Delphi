const fs = require('fs');
const { PDFDocument } = require('pdf-lib');

const coverPdfPath = process.argv[2];
const bodyPdfPath = process.argv[3];
const outPdfPath = process.argv[4];

if (!coverPdfPath || !bodyPdfPath || !outPdfPath) {
    console.error("Uso: node merge_pdfs.js <cover.pdf> <body.pdf> <output.pdf>");
    process.exit(1);
}

(async () => {
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
        
        console.log(`✅ Fusione completata in: ${outPdfPath}`);
    } catch (error) {
        console.error(`❌ Errore durante l'unione:`, error);
        process.exit(1);
    }
})();
