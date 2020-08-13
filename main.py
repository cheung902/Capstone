from ocr import *
from compare import *
# from label import *
import timeit
from multiprocessing import Process
import os
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'pdf'}
compare_file = "contract_sample/ECsample_eng.pdf"
original_file = "contract_sample/TemplateTenancyAgreement.pdf"

f1 = 'Com'
f2 = 'Ori'
contrast = 1.5
size = 1
dpiNum = 100


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods = ['GET','POST'])
def upload_page():

	if request.method =='POST':

		if 'comp_file' not in request.files or 'ori_file' not in request.files:
			return render_template('upload.html',msg = 'No file selected')

		comp_file = request.files['comp_file']
		ori_file = request.files['ori_file']
		if comp_file.filename == '' or ori_file.filename == '':
			return render_template('upload.html', msg='Please make sure to upload both files to do the comparison')

		if 	not allowed_file(comp_file.filename) or not allowed_file(ori_file.filename):
			return render_template('upload.html', msg='File format in one of the file is not accepted')

		[os.unlink(file.path) for file in os.scandir('output')]

		comp_filename_wext = secure_filename("c_" + comp_file.filename)
		ori_filename_wext = secure_filename("o_" + ori_file.filename)

		com_path = os.path.join(app.config['UPLOAD_FOLDER'],comp_filename_wext)
		ori_path = os.path.join(app.config['UPLOAD_FOLDER'], ori_filename_wext)
		comp_file.save(com_path)
		ori_file.save(ori_path)

		comp_filename =  ('.').join(comp_filename_wext.split('.')[:-1])
		ori_filename =  ('.').join(ori_filename_wext.split('.')[:-1])

		p1 = Process(target=main, args=(com_path, f1, size, contrast, dpiNum, comp_filename))
		p1.start()
		print("Compare File Job Start")
		p2 = Process(target=main, args=(ori_path, f2, size, contrast, dpiNum, ori_filename))
		p2.start()
		print("Original File Job Start")
		p1.join()
		p2.join()

		compare_f1_f2(comp_filename,ori_filename)
		return render_template('upload.html', msg = 'Successfully processed')

	elif request.method =='GET':
		return render_template('upload.html')
	return render_template('upload.html')



def main(input_pdf, file, size, contrast, dpiNum,fileName):

	ocr(input_pdf, file, size, contrast, dpiNum,fileName)


if __name__ == '__main__':
	app.secret_key = 'some secret key'
	app.run()

	start = timeit.default_timer()

	# ocr start -> image to text
	# p1 = Process(target=main,args = (compare_file, f1, size, contrast, dpiNum,f1_name))
	# p1.start()
	# print("Compare File Job Start")
	# p2 = Process(target=main, args = (original_file, f2, size, contrast, dpiNum,f2_name))
	# p2.start()
	# print("Original File Job Start")
	# p1.join()
	# p2.join()

	# compare difference of the two text file

	# [os.unlink(file.path) for file in os.scandir('images')]


	stop = timeit.default_timer()

	print('Time: ', stop - start)
