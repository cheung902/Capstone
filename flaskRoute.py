from flask import  render_template,send_from_directory,Blueprint,jsonify
from werkzeug.exceptions import HTTPException

ref_page = Blueprint('simple_page', __name__,)

@ref_page.route('/viewer/web/viewer.html')
def viewerHtml():
	return render_template('viewer/web/viewer.html')

@ref_page.route('/viewer/web/annotate.html')
def annotateHtml():
	return render_template('viewer/web/annotate.html')

@ref_page.route('/viewer/web/annotate.js')
def annotate_Js():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/annotate.js')  

@ref_page.route('/viewer/web/annotate.css')
def annotate_Css():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/annotate.css')  

@ref_page.route('/contract_sample/comp_sample.pdf')
def comp_sample():
    return send_from_directory(ref_page.root_path, 'contract_sample/comp_sample.pdf')


@ref_page.route('/node_modules/annotpdf/_bundles/pdfAnnotate.js')
def pdfannot():
    return send_from_directory(ref_page.root_path, 'node_modules/annotpdf/_bundles/pdfAnnotate.js')  

@ref_page.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

@ref_page.route('/viewer/web/test.pdf')
def pdf():
    return send_from_directory(ref_page.root_path, 'templates/test.pdf')

@ref_page.route('/viewer/web/comp.pdf')
def compPdf():
    return send_from_directory(ref_page.root_path, 'output/comp.pdf')

@ref_page.route('/viewer/web/ori.pdf')
def oriPdf():
    return send_from_directory(ref_page.root_path, 'output/ori.pdf')

@ref_page.route('/viewer/web/comp_final.pdf')
def compPdf_final():
    return send_from_directory(ref_page.root_path, 'output/comp_final.pdf')

@ref_page.route('/viewer/web/ori_final.pdf')
def oriPdf_final():
    return send_from_directory(ref_page.root_path, 'output/ori_final.pdf')

@ref_page.route('/viewer/web/comp_sample.pdf')
def compPdf_sample():
    return send_from_directory(ref_page.root_path, 'contract_sample/comp_sample.pdf')

@ref_page.route('/viewer/web/ori_sample.pdf')
def oriPdf_sample():
    return send_from_directory(ref_page.root_path, 'contract_sample/ori_sample.pdf')

@ref_page.route('/viewer/web/comp.pdf')
def compPdf_trial():
    return send_from_directory(ref_page.root_path, 'output/comp.pdf')

@ref_page.route('/viewer/web/ori.pdf')
def oriPdf_trial():
    return send_from_directory(ref_page.root_path, 'output/ori.pdf')

@ref_page.route('/upload.html')
def uploadHtml():
    return send_from_directory(ref_page.root_path, 'templates/upload.html')

@ref_page.route('/sample.html')
def sampleHtml():
    return send_from_directory(ref_page.root_path, 'templates/sample.html')

@ref_page.route('/css/upload_style.css')
def uploadCss():
    return send_from_directory(ref_page.root_path, 'templates/css/upload_style.css')

@ref_page.route('/css/loading_style.css')
def loadingCss():
    return send_from_directory(ref_page.root_path, 'templates/css/loading_style.css')

@ref_page.route('/css/sample_style.css')
def sampleCss():
    return send_from_directory(ref_page.root_path, 'templates/css/sample_style.css')

@ref_page.route('/css/pdf_view/pdf_view.css')
def pdf_view_Css():
    return send_from_directory(ref_page.root_path, 'templates/css/pdf_view/pdf_view.css')

@ref_page.route('/css/pdf_view/pdfjs.css')
def pdf_view_pdfjs_Css():
    return send_from_directory(ref_page.root_path, 'templates/css/pdf_view/pdfjs.css')

@ref_page.route('/css/pdf_annotate.css')
def pdf_annotate_Css():
    return send_from_directory(ref_page.root_path, 'templates/css/pdf_annotate.css')

@ref_page.route('/js/upload.js')
def uploadJs():
    return send_from_directory(ref_page.root_path, 'templates/js/upload.js')

@ref_page.route('/js/sample.js')
def sampleJs():
    return send_from_directory(ref_page.root_path, 'templates/js/sample.js')

@ref_page.route('/js/pdf_view.js')
def pdf_view_Js():
    return send_from_directory(ref_page.root_path, 'templates/js/pdf_view.js')

@ref_page.route('/js/pdf_view_test.js')
def pdf_view_test_Js():
    return send_from_directory(ref_page.root_path, 'templates/js/pdf_view_test.js')

@ref_page.route('/js/pdf_annotate.js')
def pdf_annotate_Js():
    return send_from_directory(ref_page.root_path, 'templates/js/pdf_annotate.js')  

@ref_page.route('/viewer/web/viewer.js')
def viewer_Js():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/viewer.js')  

@ref_page.route('/js/annotate.js')
def pdff_annotate_Js():
    return send_from_directory(ref_page.root_path, 'templates/js/annotate.js')

@ref_page.route('/viewer/web/locale/locale.properties')
def locale_properties():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/locale/locale.properties')

@ref_page.route('/viewer/web/locale/en-GB/viewer.properties')
def viewer_properties():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/locale/en-GB/viewer.properties')

@ref_page.route('/viewer/build/pdf.js')
def pdfJs():
    return send_from_directory(ref_page.root_path, 'templates/viewer/build/pdf.js')

@ref_page.route('/viewer/build/pdf.js.map')
def pdfJsMap():
    return send_from_directory(ref_page.root_path, 'templates/viewer/build/pdf.js.map')

@ref_page.route('/viewer/build/pdf.worker.js')
def pdfWorkerJs():
    return send_from_directory(ref_page.root_path, 'templates/viewer/build/pdf.worker.js')

@ref_page.route('/viewer/build/pdf.worker.js.map')
def pdfWorkerJsMap():
    return send_from_directory(ref_page.root_path, 'templates/viewer/build/pdf.worker.js.map')
@ref_page.route('/viewer/web/viewer.css')
def viewerCss():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/viewer.css')

@ref_page.route('/viewer/web/viewer.js')
def viewerJs():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/viewer.js')

@ref_page.route('/viewer/web/viewer.js.map')
def viewerJsMap():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/viewer.js.map')

@ref_page.route('/viewer/web/images/texture.png')
def texture():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/texture.png')

@ref_page.route('/viewer/web/images/toolbarButton-viewThumbnail.svg')
def toolbarButton_viewThumbnail():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-viewThumbnail.svg')

@ref_page.route('/viewer/web/images/toolbarButton-search.svg')
def toolbarButton_earch():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-search.svg')

@ref_page.route('/viewer/web/images/toolbarButton-viewOutline.svg')
def viewOutline():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-viewOutline.svg')

@ref_page.route('/viewer/web/images/sidebarToggle.svg')
def sidebarToggle():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/sidebarToggle.svg')

@ref_page.route('/viewer/web/images/toolbarButton-pageUp.svg')
def toolbarButton_pageUp():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-pageUp.svg')

@ref_page.route('/viewer/web/images/toolbarButton-viewAttachments.svg')
def toolbarButton_viewAttachments():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-viewAttachments.svg')

@ref_page.route('/viewer/web/images/toolbarButton-viewOutline.svg')
def toolbarButton_viewOutline():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-viewOutline.svg')

@ref_page.route('/viewer/web/images/toolbarButton-sidebarToggle.svg')
def toolbarButton_sidebarToggle():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-sidebarToggle.svg')

@ref_page.route('/viewer/web/images/toolbarButton-pageDown.svg')
def toolbarButton_pageDown():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-pageDown.svg')

@ref_page.route('/viewer/web/images/toolbarButton-print.svg')
def toolbarButton_print():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-print.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarToggle.svg')
def secondaryToolbarToggle():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarToggle.svg')

@ref_page.route('/viewer/web/images/toolbarButton-bookmark.svg')
def toolbarButton_bookmark():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-bookmark.svg')

@ref_page.route('/viewer/web/images/toolbarButton-secondaryToolbarToggle.svg')
def toolbarButton_secondaryToolbarToggle():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-secondaryToolbarToggle.svg')

@ref_page.route('/viewer/web/images/toolbarButton-zoomOut.svg')
def toolbarButton_zoomOut():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-zoomOut.svg')

@ref_page.route('/viewer/web/images/toolbarButton-zoomIn.svg')
def toolbarButton_zoomIn():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-zoomIn.svg')

@ref_page.route('/viewer/web/images/toolbarButton-menuArrow.svg')
def toolbarButton_menuArrows():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-menuArrow.svg')

@ref_page.route('/viewer/web/images/toolbarButton-download.svg')
def toolbarButton_download():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-download.svg')

@ref_page.route('/viewer/web/images/shadow.png')
def shadow():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/shadow.png')

@ref_page.route('/viewer/web/images/loading-icon.gif')
def loading_icon():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/loading-icon.gif')

@ref_page.route('/viewer/web/images/loading.svg')
def loading_small():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/loading.svg')

@ref_page.route('/viewer/web/images/toolbarButton-presentationMode.svg')
def toolbarButton_presentationMode():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-presentationMode.svg')

@ref_page.route('/viewer/web/images/toolbarButton-openFile.svg')
def toolbarButton_openFile():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-openFile.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-firstPage.svg')
def secondaryToolbarButton_firstPage():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-firstPage.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-lastPage.svg')
def secondaryToolbarButton_lastPage():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-lastPage.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-rotateCw.svg')
def secondaryToolbarButton_rotateCw():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-rotateCw.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-rotateCcw.svg')
def secondaryToolbarButton_rotateCcw():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-rotateCcw.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-selectTool.svg')
def secondaryToolbarButton_selectTool():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-selectTool.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-handTool.svg')
def secondaryToolbarButton_handTool():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-handTool.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-scrollVertical.svg')
def secondaryToolbarButton_scrollVertical():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-scrollVertical.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-scrollHorizontal.svg')
def secondaryToolbarButton_scrollHorizontal():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-scrollHorizontal.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-scrollWrapped.svg')
def secondaryToolbarButton_scrollWrapped():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-scrollWrapped.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-spreadNone.svg')
def secondaryToolbarButton_spreadNone():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-spreadNone.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-spreadOdd.svg')
def secondaryToolbarButton_spreadOdd():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-spreadOdd.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-spreadEven.svg')
def secondaryToolbarButton_spreadEven():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-spreadEven.svg')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-documentProperties.svg')
def secondaryToolbarButton_documentProperties():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-documentProperties.svg')

@ref_page.route('/viewer/web/images/findbarButton-next.svg')
def findbarButton_next():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/findbarButton-next.svg')

@ref_page.route('/viewer/web/images/findbarButton-previous.svg')
def findbarButton_previous():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/findbarButton-previous.svg')

@ref_page.route('/viewer/web/images/toolbarButton-viewLayers.svg')
def viewLayers():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-viewLayers.svg')