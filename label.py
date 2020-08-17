import pytesseract
from pytesseract import Output
import os
import cv2
from fpdf import FPDF

def label():
	totalPageComp = open("output/comp_cleared.txt").readlines()[-1]
	pdf = FPDF()

	for page in range(1, int(totalPageComp) + 1):
		with open("compare/comp/txtFile/" + str(page) + "_.txt") as file:
			img = cv2.imread('images/comp_' + str(page) + ".jpg")
			d = pytesseract.image_to_data(img, output_type=Output.DICT, lang='eng')
			n_boxes = len(d['level'])
			overlay = img.copy()
			print(d)
			for line in file:
				wordList = line.split()
				print(wordList)
				for i in range(0,n_boxes):
					text = d['text'][i]
					print(text, text == "Yes")
					if text in wordList:
						print(text,i)
						(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
						print(x,y,w,h)
						# cv2.rectangle(img, (x, y), (x1 + w1, y1 + h1), (0, 255, 0), 2)
						cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 0, 0), -1)
						# cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)

			alpha = 0.4  # Transparency factor.
			# Following line overlays transparent rectangle over the image
			img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

			r = 1000.0 / img_new.shape[1]  # resizing image without loosing aspect ratio
			dim = (1000, int(img_new.shape[0] * r))
			# perform the actual resizing of the image and show it
			resized = cv2.resize(img_new, dim, interpolation=cv2.INTER_AREA)

			added_image = cv2.addWeighted(img, 0.9, overlay, 0.5, 0)
			cv2.imwrite('compare/comp/images/' + str(page) + '.jpg', added_image)

			# cv2.imshow('img', resized)
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
	for i in range(1, int(totalPageComp) + 1):
			pdf.add_page()
			pdf.image("compare/comp/images/" +str(i)+ ".jpg", x=0, y=0, w=210, h=297)
	pdf.output("output/diff.pdf", "F")
