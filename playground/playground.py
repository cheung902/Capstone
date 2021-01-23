from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2Highlight import createHighlight, addHighlightToPage

pdfInput = PdfFileReader(open("../contract_sample/comp_sample.pdf", "rb"))
pdfOutput = PdfFileWriter()

page1 = pdfInput.getPage(0)

highlight = createHighlight(906.171875,1976.7284375, 1110.3644561767578, 2011.7284375, {
    "author": "",
    "contents": "Bla-bla-bla"
})

addHighlightToPage(highlight, page1, pdfOutput)

highlight = createHighlight(200.171875,1976.7284375, -1110.3644561767578, 2011.7284375, {
    "author": "",
    "contents": "Bla-bla-bla"
})

addHighlightToPage(highlight, page1, pdfOutput)

pdfOutput.addPage(page1)

outputStream = open("output.pdf", "wb")
pdfOutput.write(outputStream)