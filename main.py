from ocr import *
from compare import *
from datetime import datetime
from flaskRoute import ref_page
from multiprocessing import Process
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_cache import Cache

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = {'pdf'}
compare_file = "contract_sample/ECsample_eng.pdf"
original_file = "contract_sample/TemplateTenancyAgreement.pdf"

contrast = 1.5
size = 1
dpiNum = 300


app = Flask(__name__)
app.register_blueprint(ref_page)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["CACHE_TYPE"] = "null"
cache = Cache(app)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods = ['GET', 'POST'])
def upload_page():

	if (request.method == 'POST'):

		if ('comp_file' not in request.files or 'ori_file' not in request.files):
			return render_template('upload.html', msg = 'No file selected')

		comp_file = request.files['comp_file']
		ori_file = request.files['ori_file']
		if (comp_file.filename == '' or ori_file.filename == ''):
			return render_template('upload.html', msg='Please make sure to upload both files to do the comparison')

		if (not allowed_file(comp_file.filename) or not allowed_file(ori_file.filename)):
			return render_template('upload.html', msg='File format in one of the file is not accepted')

		[os.unlink(file.path) for file in os.scandir('output')]
		[os.unlink(file.path) for file in os.scandir('images')]
		[os.unlink(file.path) for file in os.scandir('static/upload')]
		[os.unlink(file.path) for file in os.scandir('compare/comp/images')]
		[os.unlink(file.path) for file in os.scandir('compare/comp/pdfs')]
		[os.unlink(file.path) for file in os.scandir('compare/ori/images')]
		[os.unlink(file.path) for file in os.scandir('compare/ori/pdfs')]

		comp_filename_wext = secure_filename("c_" + comp_file.filename)
		ori_filename_wext = secure_filename("o_" + ori_file.filename)

		comp_path = os.path.join(app.config['UPLOAD_FOLDER'], comp_filename_wext)
		ori_path = os.path.join(app.config['UPLOAD_FOLDER'], ori_filename_wext)
		comp_file.save(comp_path)
		ori_file.save(ori_path)

		p1 = Process(target=main, args=(comp_path, size, contrast, dpiNum, "comp"))
		p1.start()
		print("Compare File Job Start")
		p2 = Process(target=main, args=(ori_path, size, contrast, dpiNum, "ori"))
		p2.start()
		print("Original File Job Start")
		p1.join()
		p2.join()

		insertion_num, deletion_num, ori_max_page, comp_max_page = compare_f1_f2()

		# Comparison Metrics
		ori_size = os.path.getsize(ori_path)/1000
		comp_size = os.path.getsize(comp_path)/1000
		process_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		total_changes = insertion_num + deletion_num
		insertion_radius = insertion_num/total_changes * 880
		deletion_radius = deletion_num/total_changes * 880

		print('Finished')
		return render_template('pdf_view.html',
							process_datetime = process_datetime,
							comp_max_page = comp_max_page,
							ori_max_page = ori_max_page,
							comp_size = comp_size,
							ori_size = ori_size,
							comp_filename = comp_file.filename,
							ori_filename = ori_file.filename,
							total_changes = total_changes,
							insertion_num = insertion_num,
							deletion_num = deletion_num,
							insertion_radius = str(insertion_radius) + ",880" ,
							deletion_radius = str(deletion_radius) + ",880")

	elif (request.method == 'GET'):
		return render_template('upload.html')
	return render_template('upload.html')


@app.after_request
def add_header(response):
	response.cache_control.no_store = True
	return response

def main(input_pdf, size, contrast, dpiNum, compOrOri):
	ocr(input_pdf, size, contrast, dpiNum, compOrOri)

if __name__ == '__main__':
	app.secret_key = 'some secret key'
	app.run()
