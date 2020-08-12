from ocr import *
from compare import *
import timeit
from multiprocessing import Process
import os

compare_file = "contract_sample/ECsample_eng.pdf"
original_file = "contract_sample/TemplateTenancyAgreement.pdf"

f1 = 'Com'
f2 = 'Ori'
contrast = 1.5
size = 1
dpiNum = 100

f1_name = "contrast" + str(contrast) + "_Size" + str(size) + "_Dpi" + str(dpiNum) + "_file" + f1 + ".txt"
f2_name = "contrast" + str(contrast) + "_Size" + str(size) + "_Dpi" + str(dpiNum) + "_file" + f2 + ".txt"

def main(input_pdf, file, size, contrast, dpiNum,fileName):

	ocr(input_pdf, file, size, contrast, dpiNum,fileName)


if __name__ == '__main__':
	start = timeit.default_timer()

	# ocr start -> image to text
	p1 = Process(target=main,args = (compare_file, f1, size, contrast, dpiNum,f1_name))
	p1.start()
	print("Compare File Job Start")
	p2 = Process(target=main, args = (original_file, f2, size, contrast, dpiNum,f2_name))
	p2.start()
	print("Original File Job Start")
	p1.join()
	p2.join()

	# compare difference of the two text file
	compare_f1_f2(f1_name, f2_name)
	# [os.unlink(file.path) for file in os.scandir('images')]

	stop = timeit.default_timer()

	print('Time: ', stop - start)
