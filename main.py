from ocr import *
from compare import *
from datetime import datetime
from flaskRoute import ref_page
from multiprocessing import Process
import os
from flask import Flask, render_template, request, flash, session, redirect, jsonify, make_response
from werkzeug.utils import secure_filename
from flask_cache import Cache
from datetime import timedelta

# Here we will use the flask package to communicate between the frontend and backend
# Variables collected from the frontend will be collected via request and store to the session for later processing
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = {'pdf'}
# compare_file = "contract_sample/ECsample_eng.pdf"
# original_file = "contract_sample/TemplateTenancyAgreement.pdf"

contrast = 1.5
size = 1
dpiNum = 300


app = Flask(__name__)
app.register_blueprint(ref_page)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["CACHE_TYPE"] = "simple"
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
cache = Cache(app)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#This first page
#User will upload the document and select the OCR perferences
@app.route('/',methods = ['GET', 'POST'])
def upload_page():
	session.permanent = True
	if (request.method == 'POST'):
		# When use uploaded the two documents, it will get the file name and create file path and save the files temporary
		if (request.form['upload'] == "submit"):
			# session.clear()
			[os.unlink(file.path) for file in os.scandir('output')]
			[os.unlink(file.path) for file in os.scandir('images')]
			[os.unlink(file.path) for file in os.scandir('static/upload')]
			[os.unlink(file.path) for file in os.scandir('compare/comp/images')]
			[os.unlink(file.path) for file in os.scandir('compare/comp/pdfs')]
			[os.unlink(file.path) for file in os.scandir('compare/ori/images')]
			[os.unlink(file.path) for file in os.scandir('compare/ori/pdfs')]

			comp_file = request.files['comp_file']
			ori_file = request.files['ori_file']

			comp_filename_wext = secure_filename("c_" + comp_file.filename)
			ori_filename_wext = secure_filename("o_" + ori_file.filename)
			comp_path = os.path.join(app.config['UPLOAD_FOLDER'], comp_filename_wext)
			ori_path = os.path.join(app.config['UPLOAD_FOLDER'], ori_filename_wext)
			comp_file.save(comp_path)
			ori_file.save(ori_path)

			session['comp'] = comp_path
			session['ori'] = ori_path
			session['comp_filename'] = comp_file.filename
			session['ori_filename'] = ori_file.filename

			if (comp_file.filename == '' or ori_file.filename == ''):
				# return redirect('/pdf_annotate')
				return render_template('upload.html', error = "no_file")
			if (not allowed_file(comp_file.filename) or not allowed_file(ori_file.filename)):
				return render_template('upload.html', error = "file_format")
		# When user submitted the OCR options such as languages and case sensitives
		elif (request.form['upload'] == "filter"):
			lang_list = request.form.getlist('name_language')
			caseSensitive = request.form.get('name_case_diff')
			selectedTmp = request.form.get('name_template')
			extract_list = request.form.get('extract')

			session['caseSensitive'] = caseSensitive
			session['extract_list'] = extract_list
			session['selectedTmp'] = selectedTmp

			comp_path = session.get('comp')
			ori_path = session.get('ori')
			ori_pdf_size = session.get('ori_pdf_size')
			comp_pdf_size = session.get('comp_pdf_size')

			# concat if multiple languages selected
			if len(lang_list) > 1:
				lang = "+".join(lang_list)
			elif len(lang_list) == 1:
				lang = lang_list[0]
			else:
				lang = ""

			print("Language option:", lang)
			print("Case Sensitive Option", caseSensitive)
			print("extract_list", extract_list)

			# Start processing the ocr
			p1 = Process(target=main, args=(comp_path, size, contrast, dpiNum, "comp", lang))
			p1.start()
			print("Compare File Job Start")
			p2 = Process(target=main, args=(ori_path, size, contrast, dpiNum, "ori", lang))
			p2.start()
			print("Original File Job Start")
			p1.join()
			p2.join()

			# after ocr, it will redirect to the annotation page
			return redirect('/pdf_annotate')

	elif (request.method == 'GET'):
		tmp = session.get('tmpName')
		print("tmp", tmp)
		return render_template('upload.html', tmp = tmp)
	return ('', 204)

#This is the page for annotation.
@app.route('/pdf_annotate',methods = ['GET', 'POST'])	
def annotate():
	if (request.method == 'POST'):
		#  After users proceed to compare, it will start compare the document
		if (request.form["name_next"] == "submit"):
			comp_path = session.get('comp')
			ori_path = session.get('ori')
			comp_filename = session.get('comp_filename')
			ori_filename = session.get('ori_filename')

			insertion_num, deletion_num,\
			case_diff_num, ori_max_page, comp_max_page, extractResult, oriLowConf, compLowConf, oriExtraPage, compExtraPage = compare_f1_f2()
			# Comparison Metrics
			for item in extractResult:
				print(item[0])
				print(item[1])
				print(item[2])
			ori_size = os.path.getsize(ori_path)/1000
			comp_size = os.path.getsize(comp_path)/1000
			process_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			total_changes = insertion_num + deletion_num + case_diff_num
			insertion_radius = insertion_num/total_changes * 880
			deletion_radius = deletion_num/total_changes * 880

			print('Finished')

			return render_template('pdf_view.html',
								process_datetime = process_datetime,
								comp_max_page = comp_max_page, ori_max_page = ori_max_page,
								comp_size = comp_size, ori_size = ori_size,
								comp_filename = comp_filename, ori_filename = ori_filename,
								total_changes = total_changes,
								insertion_num = insertion_num, deletion_num = deletion_num,
								insertion_radius = str(insertion_radius) + ",880" , deletion_radius = str(deletion_radius) + ",880",
								extractResult = extractResult, oriLowConf = oriLowConf, 
								compLowConf = compLowConf,
								oriExtraPage= oriExtraPage, compExtraPage = compExtraPage)
	#if user selected template, the marked regions will be generated automatically and save the coordinates to session.
	selectedTmp = session.get('selectedTmp')
	templates = session.get('tmpName')
	if selectedTmp is not None:
		for template in templates:
			if (templates[0][0]) == selectedTmp:
				session['ignore_region_ori'] = templates[1][0]
				session['shdChange_region_ori'] = templates[1][1]
				session['shdNotChange_region_ori'] = templates[1][2]
				session['ignore_region_comp'] = templates[1][3]
				session['shdChange_region_comp'] = templates[1][4]
				session['shdNotChange_region_comp'] = templates[1][5]

		comp_path = session.get('comp')
		ori_path = session.get('ori')
		comp_filename = session.get('comp_filename')
		ori_filename = session.get('ori_filename')

		insertion_num, deletion_num, \
		case_diff_num, ori_max_page, comp_max_page, extractResult, oriLowConf, compLowConf, oriExtraPage, compExtraPage = compare_f1_f2()
		# Comparison Metrics
		ori_size = os.path.getsize(ori_path) / 1000
		comp_size = os.path.getsize(comp_path) / 1000
		process_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		total_changes = insertion_num + deletion_num + case_diff_num
		insertion_radius = insertion_num / total_changes * 880
		deletion_radius = deletion_num / total_changes * 880

		print('Finished')

		# after collecting all the result, redirect to the report page
		return render_template('pdf_view.html',
							   process_datetime=process_datetime,
							   comp_max_page=comp_max_page, ori_max_page=ori_max_page,
							   comp_size=comp_size, ori_size=ori_size,
							   comp_filename=comp_filename, ori_filename=ori_filename,
							   total_changes=total_changes,
							   insertion_num=insertion_num, deletion_num=deletion_num,
							   insertion_radius=str(insertion_radius) + ",880",
							   deletion_radius=str(deletion_radius) + ",880",
							   extractResult=extractResult, oriLowConf=oriLowConf,
							   compLowConf=compLowConf,
							   oriExtraPage= oriExtraPage, compExtraPage = compExtraPage)
	return render_template('pdf_annotate.html')

# Since we are using pdf.js, There are two pdf windows embedded into the iframe.
# Which means there are two html and js worksheet for the two pdf viewers.

# This part is to collect the coordinates of marked regions specified by user on the original document.
@app.route('/annotate_ori',methods = ['GET', 'POST'])
def annotate_ori():
	print("submitted", "\n")
	array_value = list(request.form.to_dict(flat=False).values())
	ignore_ori, shdChange_ori, shdNotChange_ori, extract_ori = [],[],[], []
	for index, item in enumerate(array_value):
		if item[1] == "ignore":
			pageNum = item[0]
			ignore_ori.append([pageNum, array_value[index+1]])
		elif item[1] == "shdChange":
			pageNum = item[0]
			shdChange_ori.append([pageNum, array_value[index + 1]])
		elif item[1] == "shdNotChange":
			pageNum = item[0]
			shdNotChange_ori.append([pageNum, array_value[index + 1]])
		elif item[1] == "extract":
			pageNum = item[0]
			extract_ori.append([pageNum, array_value[index + 1]])

	session['ignore_region_ori'] = ignore_ori
	session['shdChange_region_ori'] = shdChange_ori
	session['shdNotChange_region_ori'] = shdChange_ori
	session['extract_region_ori'] = extract_ori
	return ('', 204)

# This part is to collect the coordinates of marked regions specified by user on the targeted document.
@app.route('/annotate_comp',methods = ['GET', 'POST'])
def annotate_comp():
	session.permanent = True

	array_value = list(request.form.to_dict(flat=False).values())
	ignore_comp, shdChange_comp, shdNotChange_comp, extract_comp = [],[],[], []
	for index, item in enumerate(array_value):
		if item[1] == "ignore":
			pageNum = item[0]
			ignore_comp.append([pageNum, array_value[index+1]])
		elif item[1] == "shdChange":
			pageNum = item[0]
			shdChange_comp.append([pageNum, array_value[index + 1]])
		elif item[1] == "shdNotChange":
			pageNum = item[0]
			shdNotChange_comp.append([pageNum, array_value[index + 1]])
		elif item[1] == "extract":
			pageNum = item[0]
			extract_comp.append([pageNum, array_value[index + 1]])
	session['ignore_region_comp'] = ignore_comp
	session['shdChange_region_comp'] = shdChange_comp
	session['shdNotChange_region_comp'] = shdChange_comp
	session['extract_region_comp'] = extract_comp

# If user choose to save the marked regions as template to use for similar documents, it will save all coordinates.
@app.route('/saveTmp',methods = ['GET', 'POST'])
def saveTmp():
	name = list(request.form.to_dict(flat=False).values())[0][0]
	ignore_comp = session.get('ignore_region_comp')
	shdChange_comp = session.get('shdChange_region_comp')
	shdNotChange_comp = session.get('shdNotChange_region_comp')
	ignore_ori = session.get('ignore_region_ori')
	shdChange_ori = session.get('shdChange_region_ori')
	shdNotChange_ori = session.get('shdNotChange_region_ori')

	value = [ignore_ori, shdChange_ori, shdNotChange_ori, ignore_comp, shdChange_comp, shdNotChange_comp]

	if 'tmpName' not in session:
		session['tmpName'] = []
	tmpList = session.get('tmpName')
	tmpList.append([name, value])
	session['tmpName'] = tmpList
	

	return ('', 204)

@app.route('/tmpDelete',methods = ['GET' 'POST'])	
def tmpDelete():
	print(request)
	name = list(request.form.to_dict(flat=False).values())
	print(name)
	return ('', 204)

@app.route('/pdf_view',methods = ['GET' 'POST'])	
def pdf_view():
	return ('', 204)

@app.after_request
def add_header(response):	
	response.cache_control.no_store = True
	return response

def main(input_pdf, size, contrast, dpiNum, compOrOri, lang):
	ocr(input_pdf, size, contrast, dpiNum, compOrOri, lang)

if __name__ == '__main__':
	app.secret_key = 'some secret key'
	app.run()
