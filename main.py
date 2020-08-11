from ocr import *
from compare import *
import timeit
from multiprocessing import Process

compare_file = "contract_sample/ECsample_eng.pdf"
original_file = "contract_sample/TemplateTenancyAgreement.pdf"
1
f1_num = 1
f2_num = 2
contrast = 1.5
size = 4
dpiNum = 300

f1_name = "contrast" + str(contrast) + "_Size" + str(size) + "_Dpi" + str(dpiNum) + "_file" + str(f1_num) + "txt"
f2_name = "contrast" + str(contrast) + "_Size" + str(size) + "_Dpi" + str(dpiNum) + "_file" + str(f2_num) + "txt"

if __name__ == '__main__':
	start = timeit.default_timer()

	# ocr start -> image to text
	p1 = Process(target=ocr(compare_file, f1_num, size, contrast, dpiNum,f1_name))
	p1.start()
	p2 = Process(target=ocr(original_file, f2_num, size, contrast, dpiNum,f2_name))
	p2.start()
	p1.join()
	p2.join()
	# procs = []
	# procs.append(Process(target=ocr(compare_file, f1_num, size, contrast, dpiNum, f1_name)))
	# procs.append(Process(target=ocr(compare_file, f1_num, size, contrast, dpiNum, f2_name)))
	# map(lambda x: x.start(), procs)
	# map(lambda x: x.join(), procs)
	# compare difference of the two text file
	compare_f1_f2(f1_name, f2_name)
	stop = timeit.default_timer()

	print('Time: ', stop - start)
