from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2Highlight import createHighlight, addHighlightToPage

pdfInput = PdfFileReader(open("../contract_sample/comp_sample.pdf", "rb"))
pdfOutput = PdfFileWriter()

page1 = pdfInput.getPage(0)

highlight = createHighlight(524,1449.83, 709, 1477.83, {
    "author": "",
    "contents": "Bla-bla-bla"
})

addHighlightToPage(highlight, page1, pdfOutput)


pdfOutput.addPage(page1)

outputStream = open("output.pdf", "wb")
pdfOutput.write(outputStream)