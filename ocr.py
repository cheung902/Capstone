# Import libraries
from preprocess import *
from PIL import Image, ImageEnhance
import pytesseract
from pdf2image import convert_from_path

def ocr(input_pdf, fileNum, size, contrast, dpiNum,fileName):
	'''
	Part #1 : Converting PDF to images
	'''

	# Store all the pages of the PDF in a variable
	pages = convert_from_path(input_pdf, 500)

	# Counter to store images of each page of PDF to image
	image_counter = 1

	# Iterate through all the pages stored above
	# Declaring filename for each page of PDF as JPG
	# Save the image of the page in system
	# Increment the counter to update filename
	for page in pages:

		imgName = "page_" + str(fileNum) + "_" + str(image_counter) + ".jpg"
		print("image" + imgName)
		page.save("images/" + imgName, 'JPEG')
		image_counter = image_counter + 1

	''' 
	Part #2 - Recognizing text from the images using OCR 
	'''
	# Variable to get count of total number of pages
	fileLimt = image_counter - 1

	# Creating a text file to write the output
	outFile = "output/" + fileName

	# Open the file in append mode so that
	# All contents of all images are added to the same file
	f = open(outFile, "a")

	# Iterate from 1 to total number of pages
	# Set filename to recognize text from
	# Increase the Contrast
	# Set DPI to 300 & larger the size
	# Recognize the text as string in image using pytesserct
	# Finally, write the processed text to the file.
	for i in range(1, fileLimt + 1):

		img = "page_" + str(i) + "_" + str(fileNum) + ".jpg"
		print("ocr" + img)
		pre_process(img, size, contrast, dpiNum)

		text = str((pytesseract.image_to_string(Image.open("images/" + img))))
		text = text.replace('-\n', '')

		f.write(text)

	# os.remove(filename)
	# Close the file after writing all the text.
	f.close()
