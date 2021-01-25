import os
import pytesseract
import cv2
from PyPDF2 import PdfFileMerger

def removeFiles(path_list):
	for file in path_list:
		os.remove(file)
		print(file + " removed.")

def getLineNum(stringList):
	return int(''.join(filter(str.isdigit, stringList)))

def createSearchablePDF(input_path, output_path):
	img = cv2.imread(input_path)
	img = pytesseract.image_to_pdf_or_hocr(img, extension="pdf")
	pdf = open(output_path, "w+b")
	pdf.write(img)

def mergePDF(input_paths, output_path):
	pdf_merger = PdfFileMerger()

	for path in input_paths:
		pdf_merger.append(path)

	with open(output_path, 'wb') as fileobj:
		pdf_merger.write(fileobj)

