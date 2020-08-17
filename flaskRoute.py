from flask import  render_template,send_from_directory,Blueprint,jsonify
from werkzeug.exceptions import HTTPException

ref_page = Blueprint('simple_page', __name__,)

@ref_page.route('/viewer/web/viewer.html')
def viewerHtml():
	return render_template('viewer/web/viewer.html')

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
    return send_from_directory(ref_page.root_path, 'output/diff.pdf')

@ref_page.route('/viewer/web/ori.pdf')
def oriPdf():
    return send_from_directory(ref_page.root_path, 'output/ori.pdf')

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

@ref_page.route('/viewer/web/images/toolbarButton-viewThumbnail@2x.png')
def toolbarButton_viewThumbnail():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-viewThumbnail@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-search@2x.png')
def toolbarButton_earch():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-search@2x.png')

@ref_page.route('/viewer/web/images/viewOutline@2x.png')
def viewOutline():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/viewOutline@2x.png')

@ref_page.route('/viewer/web/images/sidebarToggle@2x.png')
def sidebarToggle():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/sidebarToggle@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-pageUp@2x.png')
def toolbarButton_pageUp():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-pageUp@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-viewAttachments@2x.png')
def toolbarButton_viewAttachments():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-viewAttachments@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-viewOutline@2x.png')
def toolbarButton_viewOutline():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-viewOutline@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-sidebarToggle@2x.png')
def toolbarButton_sidebarToggle():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-sidebarToggle@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-pageDown@2x.png')
def toolbarButton_pageDown():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-pageDown@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-print@2x.png')
def toolbarButton_print():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-print@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarToggle@2x.png')
def secondaryToolbarToggle():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarToggle@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-bookmark@2x.png')
def toolbarButton_bookmark():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-bookmark@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-secondaryToolbarToggle@2x.png')
def toolbarButton_secondaryToolbarToggle():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-secondaryToolbarToggle@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-zoomOut@2x.png')
def toolbarButton_zoomOut():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-zoomOut@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-zoomIn@2x.png')
def toolbarButton_zoomIn():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-zoomIn@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-menuArrows@2x.png')
def toolbarButton_menuArrows():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-menuArrows@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-download@2x.png')
def toolbarButton_download():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-download@2x.png')

@ref_page.route('/viewer/web/images/shadow.png')
def shadow():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/shadow.png')

@ref_page.route('/viewer/web/images/loading-icon.gif')
def loading_icon():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/loading-icon.gif')

@ref_page.route('/viewer/web/images/loading-small@2x.png')
def loading_small():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/loading-small@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-presentationMode@2x.png')
def toolbarButton_presentationMode():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-presentationMode@2x.png')

@ref_page.route('/viewer/web/images/toolbarButton-openFile@2x.png')
def toolbarButton_openFile():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/toolbarButton-openFile@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-firstPage@2x.png')
def secondaryToolbarButton_firstPage():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-firstPage@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-lastPage@2x.png')
def secondaryToolbarButton_lastPage():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-lastPage@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-rotateCw@2x.png')
def secondaryToolbarButton_rotateCw():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-rotateCw@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-rotateCcw@2x.png')
def secondaryToolbarButton_rotateCcw():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-rotateCcw@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-selectTool@2x.png')
def secondaryToolbarButton_selectTool():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-selectTool@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-handTool@2x.png')
def secondaryToolbarButton_handTool():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-handTool@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-scrollVertical@2x.png')
def secondaryToolbarButton_scrollVertical():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-scrollVertical@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-scrollHorizontal@2x.png')
def secondaryToolbarButton_scrollHorizontal():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-scrollHorizontal@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-scrollWrapped@2x.png')
def secondaryToolbarButton_scrollWrapped():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-scrollWrapped@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-spreadNone@2x.png')
def secondaryToolbarButton_spreadNone():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-spreadNone@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-spreadOdd@2x.png')
def secondaryToolbarButton_spreadOdd():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-spreadOdd@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-spreadEven@2x.png')
def secondaryToolbarButton_spreadEven():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-spreadEven@2x.png')

@ref_page.route('/viewer/web/images/secondaryToolbarButton-documentProperties@2x.png')
def secondaryToolbarButton_documentProperties():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/secondaryToolbarButton-documentProperties@2x.png')

@ref_page.route('/viewer/web/images/findbarButton-next@2x.png')
def findbarButton_next():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/findbarButton-next@2x.png')

@ref_page.route('/viewer/web/images/findbarButton-previous@2x.png')
def findbarButton_previous():
    return send_from_directory(ref_page.root_path, 'templates/viewer/web/images/findbarButton-previous@2x.png')

