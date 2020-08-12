from PIL import Image, ImageEnhance
Image.MAX_IMAGE_PIXELS = None
import timeit



def pre_process(fileName, size, contrast, dpiNum):
	print("Preprocessing: " + fileName)
	start = timeit.default_timer()

	img = Image.open("images/" + fileName)

	enhancer = ImageEnhance.Contrast(img)
	img = enhancer.enhance(contrast)

	new_size = tuple(size * x for x in img.size)
	img = img.resize(new_size, Image.ANTIALIAS)
	img.save("images/" + fileName, dpi=(dpiNum, dpiNum))

	stop = timeit.default_timer()
	print('Time for preprocess ' + fileName + ': ', stop - start)
