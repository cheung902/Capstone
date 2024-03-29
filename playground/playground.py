# Import libraries
import pytesseract
import cv2
from preprocess import *
from pdf2image import convert_from_path
from PyPDF2 import PdfFileMerger
import json
from commonFNC import *


def ocr(inputFile, size, contrast, dpiNum, compOrori, lang):
	image_counter = 1
	data = []

	if inputFile.lower().endswith('.pdf'):
		# Store all the pages of the PDF in a variable
		pages = convert_from_path(inputFile, fmt='tiff')

		# Counter to store images of each page of PDF to image
		# Iterate through all the pages stored above
		# Declaring filename for each page of PDF as JPG
		# Save the image of the page in system
		# Increment the counter to update filename

		for page in pages:

			imgPath = "../images/" + compOrori + "_" + str(image_counter) + ".tiff"

			if compOrori == "comp":
				imgPath_comp = "../compare/comp/images/" + compOrori + "_" + str(image_counter) + ".tiff"
			else:
				imgPath_comp = "../compare/ori/images/" + compOrori + "_" + str(image_counter) + ".tiff"

			page.save(imgPath)
			page.save(imgPath_comp)
			image_counter = image_counter + 1

	# Variable to get count of total number of pages
	fileLimt = image_counter - 1

	# Iterate from 1 to total number of pages
	# Set filename to recognize text from
	# Increase the Contrast
	# Set DPI to 300 & larger the size
	# Recognize the text as string in image using pytesserct
	# Finally, write the processed text to the file.
	for i in range(1, fileLimt + 1):

		imgFile = compOrori + "_" + str(i) + ".tiff"

		pre_process(imgFile, size, contrast, dpiNum)

		print("Ocring: " + imgFile)
		start = timeit.default_timer()

		img = cv2.imread("images/" + imgFile)

		if lang != "":
			data.append(pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=lang))
		else:
			data.append(pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT))
		stop = timeit.default_timer()
		print('Time for ocr the ' + imgFile + ': ', stop - start)

	with open("../output/" + compOrori + ".txt", 'w') as file:
		file.write(json.dumps(data))

	pdf_paths = []
	for i in range(1, fileLimt + 1):
		input_path = "../images/" + compOrori + "_" + str(i) + ".tiff"
		output_path = "../compare/" + compOrori + "/pdfs/" + compOrori + "_" + str(i) + ".pdf"
		pdf_paths.append(output_path)

		createSearchablePDF(input_path=input_path, output_path=output_path)
	# pdf_paths.append("output/diff" + str(i) + ".pdf")
	# with open("output/diff" + str(i) +".pdf", "wb") as pdf:
	# 	pdf.write(img2pdf.convert("compare/comp/images/comp_" + str(i) + ".tiff"))

	out_path = "../output/" + compOrori + ".pdf"
	mergePDF(pdf_paths, out_path)


# def createSearchablePDF(imgFile, imgName):
# 	img = cv2.imread("images/" + imgFile)
# 	img = pytesseract.image_to_pdf_or_hocr(img, extension="pdf")
# 	pdf = open("output/" + imgName + ".pdf", "w+b")
# 	pdf.write(bytearray(img))


def mergePDF(input_paths, output_path):
	pdf_merger = PdfFileMerger()

	for path in input_paths:
		pdf_merger.append(path)

	with open(output_path, 'wb') as fileobj:
		pdf_merger.write(fileobj)


def addLineIndex(input_path, output_path):
	with open(input_path) as finp, open(output_path, "w") as fout:
		for index, line in enumerate(finp):
			fout.write(str(index) + ": " + line)


if __name__ == '__main__':
	ocr("testing_1.pdf", 1.5, 1.5, 300, "comp", "")