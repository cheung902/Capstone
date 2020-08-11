from PIL import Image, ImageEnhance
Image.MAX_IMAGE_PIXELS = None
import timeit


def pre_process(fileName, size, contrast, dpiNum):

	img = Image.open("images/" + fileName)

	enhancer = ImageEnhance.Contrast(img)
	img = enhancer.enhance(contrast)

	new_size = tuple(size * x for x in img.size)
	img = img.resize(new_size, Image.ANTIALIAS)
	img.save("images/" + fileName, dpi=(dpiNum, dpiNum))

