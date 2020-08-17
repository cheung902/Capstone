# Import libraries
import pytesseract
import timeit
from preprocess import *
from PIL import Image, ImageEnhance
from pdf2image import convert_from_path
from fpdf import FPDF



def ocr(inputFile, size, contrast, dpiNum,fileName,compOrori):

	image_counter = 1
	pdf = FPDF()
	if inputFile.lower().endswith('.pdf'):
		# Store all the pages of the PDF in a variable
		pages = convert_from_path(inputFile,fmt='JPEG')

		# Counter to store images of each page of PDF to image


		# Iterate through all the pages stored above
		# Declaring filename for each page of PDF as JPG
		# Save the image of the page in system
		# Increment the counter to update filename

		for page in pages:

			imgPath = "images/" + compOrori + "_" + str(image_counter) + ".jpg"

			page.save(imgPath)

			if image_counter == 1:
				cover = Image.open(imgPath)
				w, h = cover.size
				pdf = FPDF(unit="pt", format=[w, h])
			image = imgPath
			pdf.add_page()
			pdf.image(image, 0, 0, w, h)


			image_counter = image_counter + 1

	pdf.output("output/" + compOrori + ".pdf", "F")
	# Variable to get count of total number of pages
	fileLimt = image_counter - 1

	# Creating a text file to write the output
	outFile = "output/" + compOrori + ".txt"

	# Open the file in append mode so that
	# All contents of all images are added to the same file
	f = open(outFile, "a+")

	# Iterate from 1 to total number of pages
	# Set filename to recognize text from
	# Increase the Contrast
	# Set DPI to 300 & larger the size
	# Recognize the text as string in image using pytesserct
	# Finally, write the processed text to the file.
	for i in range(1, fileLimt + 1):

		img = compOrori + "_" + str(i) + ".jpg"

		pre_process(img, size, contrast, dpiNum)

		print("Ocring: " + img)
		start = timeit.default_timer()
		text = str((pytesseract.image_to_string(Image.open("images/" + img),lang= "eng")))
		stop = timeit.default_timer()
		print('Time for ocr the ' + img + ': ', stop - start)

		text = text.replace('-\n', '')
		f.write(text + '\n')
		f.write(str(i) + '\n')
	# os.remove(filename)
	# Close the file after writing all the text.
	f.close()

	with open(outFile) as infile , open("output/" + compOrori + "_cleared.txt","w") as outfile:
		for line in infile:
			if not line.strip(): continue  # skip the empty line
			outfile.write(line)

