from PIL import Image, ImageEnhance
import cv2 as cv
Image.MAX_IMAGE_PIXELS = None
import timeit



def pre_process(imgName, size, contrast, dpiNum):

	print("Preprocessing: " + imgName)
	start = timeit.default_timer()

	img = cv.imread("images/" + imgName, 0)
	img = cv.GaussianBlur(img, (5, 5), 0)
	cv.imwrite("images/" + imgName, img)

	img = Image.open("images/" + imgName)

	enhancer = ImageEnhance.Contrast(img)
	img = enhancer.enhance(contrast)

	# new_size = tuple(size * x for x in img.size)
	# img = img.resize(new_size, Image.ANTIALIAS)
	#
	# new_size = (1920, 1080)
	# img = img.resize(new_size, Image.ANTIALIAS)

	img.save("images/" + imgName, dpi=(dpiNum, dpiNum))


	stop = timeit.default_timer()
	print('Time for preprocess ' + imgName + ': ', stop - start)
