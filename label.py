import re
import cv2
import pytesseract
from pytesseract import Output

img = cv2.imread('images/page_Com_1.tif')
img = cv2.resize(img,(1680,2400))
d = pytesseract.image_to_data(img, output_type=Output.DICT)
keys = list(d.keys())

date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'

n_boxes = len(d['text'])
for i in range(n_boxes):
	if int(d['conf'][i]) > 60:
		if d['text'][i] == 'Employment':
			(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
			img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()