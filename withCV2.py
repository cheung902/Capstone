import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

PDF_file = "ECsample_eng.pdf"

# Store all the pages of the PDF in a variable
pages = convert_from_path(PDF_file, 500)

# Counter to store images of each page of PDF to image
image_counter = 1

# Iterate through all the pages stored above
for page in pages:
	# Declaring filename for each page of PDF as JPG
	# For each page, filename will be:
	# PDF page 1 -> page_1.jpg
	# PDF page 2 -> page_2.jpg
	# PDF page 3 -> page_3.jpg
	# ....
	# PDF page n -> page_n.jpg
	filename = "page_" + str(image_counter) + ".jpg"

	# Save the image of the page in system
	page.save(filename, 'JPEG')

	# Increment the counter to update filename
	image_counter = image_counter + 1

''' 
Part #2 - Recognizing text from the images using OCR 
'''

# Variable to get count of total number of pages
filelimit = image_counter - 1

# Creating a text file to write the output
outfile = "out_text.txt"

# Open the file in append mode so that
# All contents of all images are added to the same file
f = open(outfile, "a")

# Iterate from 1 to total number of pages
for i in range(1, filelimit + 1):
	# Set filename to recognize text from
	# Again, these files will be:
	# page_1.jpg
	# page_2.jpg
	# ....
	# page_n.jpg
	filename = "page_" + str(i) + ".jpg"

	# Recognize the text as string in image using pytesserct
	text = str(((pytesseract.image_to_string(Image.open(filename),lang='chi_tra'))))

	# The recognized text is stored in variable text
	# Any string processing may be applied on text
	# Here, basic formatting has been done:
	# In many PDFs, at line ending, if a word can't
	# be written fully, a 'hyphen' is added.
	# The rest of the word is written in the next line
	# Eg: This is a sample text this word here GeeksF-
	# orGeeks is half on first line, remaining on next.
	# To remove this, we replace every '-\n' to ''.
	text = text.replace('-\n', '')

	# Finally, write the processed text to the file.
	f.write(text)

# Close the file after writing all the text.
f.close()


# get grayscale image
def get_grayscale(image):
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
	return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
	return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
	kernel = np.ones((5, 5), np.uint8)
	return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
	kernel = np.ones((5, 5), np.uint8)
	return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
	kernel = np.ones((5, 5), np.uint8)
	return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
	return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
	coords = np.column_stack(np.where(image > 0))
	angle = cv2.minAreaRect(coords)[-1]
	if angle < -45:
		angle = -(90 + angle)

	else:
		angle = -angle
		(h, w) = image.shape[:2]
		center = (w // 2, h // 2)
		M = cv2.getRotationMatrix2D(center, angle, 1.0)
		rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
		return rotated


# template matching
def match_template(image, template):
	return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)