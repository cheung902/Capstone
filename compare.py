import json
import pandas as pd
from commonFNC import *
import diff_match_patch as dmp_module
import numpy as np
import cv2
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2Highlight import createHighlight, addHighlightToPage
from flask import session
from shapely.geometry import Polygon


def compare_f1_f2(extract_list="", caseSensitive = "True"):
	print("-----------------------------------")
	print("Comparing files ")
	print("-----------------------------------")

	# label
	insert_label = "G_label"
	delete_label = "R_label"
	case_label = "B_label"

	# Comparison Report
	insertion_num = 0
	deletion_num = 0
	case_diff_num = 0
	
	#extract
	extract = ['']

	# ignore_region = session.get('ignore_region')
	# shdChange_region = session.get('shdChange_region')
	# shdNotChange_region = session.get('shdNotChange_region')
	ignore_region = ""
	shdChange_region = ""
	shdNotChange_region = ""

	ori_data_frame, comp_data_frame = get_data_frame()
	ori_max_page = ori_data_frame["page_num"].max()
	comp_max_page = comp_data_frame["page_num"].max()
	ori_text = get_group_of_text(ori_data_frame)
	comp_text = get_group_of_text(comp_data_frame)

	ori_diff, comp_diff, insertion_num, deletion_num, case_diff_num = diff_match(ori_text, comp_text, insertion_num,
																				 deletion_num, case_diff_num,
																				 insert_label, delete_label,
																				 case_label, caseSensitive)

	if (comp_diff != None):
		ori_word_position = get_position(data_frame=ori_data_frame, diff_list=ori_diff,
										 insert_label=insert_label, delete_label=delete_label,
										 case_label = case_label)

		comp_word_position = get_position(data_frame=comp_data_frame, diff_list=comp_diff,
										  insert_label=insert_label, delete_label=delete_label,
										  case_label = case_label)

		label_word(ignore_region, shdChange_region, shdNotChange_region, ori_word_position, ori_max_page, "ori")
		label_word(ignore_region, shdChange_region, shdNotChange_region, comp_word_position, comp_max_page, "comp")

	return insertion_num, deletion_num, case_diff_num, ori_max_page, comp_max_page

def get_position(data_frame, diff_list, insert_label, delete_label, case_label):
	print("---------------Getting Word Number and Line Number-------------")
	position_list = []
	diff_list_split = diff_list.split()
	insert_label_start = insert_label + "S-"
	insert_label_end = "-" + insert_label + "S"
	delete_label_start = delete_label + "S-"
	delete_label_end = "-" + delete_label + "S"
	case_label_start = case_label + "S-"
	case_label_end = "-" + case_label + "S"
	insert_label = insert_label + "-"
	delete_label = delete_label + "-"
	case_label = case_label + "-"
	for num, element in enumerate(diff_list_split):
		if (insert_label_start in element):
			word = element.replace(insert_label_start, "")
			append_position_list(data_frame = data_frame, position_list = position_list, num = num, word = word, insert_or_delete="1s")
			num +=1
			while insert_label_end not in diff_list_split[num]:
				word = diff_list_split[num]
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word = word, insert_or_delete="1")
				num += 1

			if (insert_label_end in diff_list_split[num]):
				word = diff_list_split[num].replace(insert_label_end, "")
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word = word, insert_or_delete="1e")
				continue

		elif delete_label_start in element:
			word = element.replace(delete_label_start, "")
			append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="-1s")
			num += 1
			while delete_label_end not in diff_list_split[num]:
				word = diff_list_split[num]
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="-1")
				num += 1
			if delete_label_end in diff_list_split[num]:
				word = diff_list_split[num].replace(delete_label_end, "")
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="-1e")
				continue

		elif case_label_start in element:
			word = element.replace(case_label_start, "")

			append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="2s")
			num += 1
			while case_label_end not in diff_list_split[num]:
				word = diff_list_split[num]
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="2")
				num += 1
			if case_label_end in diff_list_split[num]:
				word = diff_list_split[num].replace(case_label_end, "")
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="2e")
				continue

		elif delete_label in element:
			word = element.replace(delete_label, "")
			append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="-1")

		elif insert_label in element:
			word = element.replace(insert_label, "")
			append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="1")

		elif case_label in element:

			word = element.replace(case_label, "")
			append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="2")

	return position_list


def label_word(ignore_region, shdChange_region, shdNotChange_region, diff_list, max_page, compOrori):
	print("Creating ", compOrori, ".pdf")

	pdfInput = PdfFileReader(open("output/" + compOrori + ".pdf", "rb"))

	numOfPages = pdfInput.getNumPages()
	pdfOutput = PdfFileWriter()

	for diff_pageIndex in range(0, numOfPages):
		page = pdfInput.getPage(diff_pageIndex)
		pypdf2_height = page.mediaBox.getHeight()
		pypdf2_width = page.mediaBox.getWidth()

		#top left and bottom right
		img = cv2.imread('images/' + compOrori + '_' + str(diff_pageIndex + 1) + ".tiff")
		cv2_height, cv2_width, _ = img.shape

		nh = pypdf2_height/cv2_height
		nw = pypdf2_width/cv2_width
		for index, item in enumerate(diff_list):
			if item[0] - 1 == diff_pageIndex:
				overlap = False
				(x, y, w, h) = (item[1][0], item[1][1], item[1][2], item[1][3])
				#transform to pypdf2 region
				(x_1, y_1, x_2, y_2) = (x*nw, (cv2_height - y - h)*nh, (x + w) *nw, (cv2_height - y)*nh)
				diff_region = [x_1, y_1, x_2, y_2]
				if (ignore_region is not None):
					for marked_region in ignore_region:
						marked_pageIndex = int(marked_region[0][0])
						if (marked_pageIndex == diff_pageIndex):
							overlap = cal_overlap_area(marked_region, diff_region)
							if (overlap == True):
								break
				if overlap == True:
					break


				if item[2] == "-1":
					print("Deleted: ", item[3])
					highlight = createHighlight(x1=x_1, y1=y_1, x2=x_2, y2=y_2,
												meta={"author": "", "contents": "Bla-bla-bla"},
												color=[1, 0.5, 0])
					addHighlightToPage(highlight, page, pdfOutput)
				elif item[2] == "1":
					print("Deleted: ", item[3])
					highlight = createHighlight(x1=x_1, y1=y_1, x2=x_2, y2=y_2,
												meta={"author": "", "contents": "Bla-bla-bla"},
												color=[0, 1, 0])
					addHighlightToPage(highlight, page, pdfOutput)
				elif item[2] == "2":
					print("Deleted: ", item[3])
					highlight = createHighlight(x1=x_1, y1=y_1, x2=x_2, y2=y_2,
												meta={"author": "", "contents": "Bla-bla-bla"},
												color=[0, 0.5, 1])
					addHighlightToPage(highlight, page, pdfOutput)
		print("create page", diff_pageIndex)
		pdfOutput.addPage(page)
	outputStream = open("output/" +compOrori + "_final.pdf", "wb")
	pdfOutput.write(outputStream)
	# outputStream.close()
	# os.rename("output/" + compOrori + "_final.pdf", "output/" + compOrori + ".pdf")
	# removeFiles(pdf_paths)


def diff_match(line1, line2, insertion_num, deletion_num, case_diff_num, insert_label, delete_label, case_label, caseSensitive):

	ori_output = []
	comp_output = []

	dmp = dmp_module.diff_match_patch()
	diff = dmp.diff_main(line1, line2)
	dmp.diff_cleanupEfficiency(diff)
	print("difference: ", diff)

	skip = False
	print("CaseSensitive: ", caseSensitive)
	if caseSensitive == "True":
		for index, element in enumerate(diff):
			# try:
				if (skip is True):
					skip = False
					continue
				if (element[0] == 0):
					ori_output.append(element[1])
					comp_output.append(element[1])
					skip = False
				elif (element[0] == -1 or element[0] == 1):
					next_item = diff[index + 1][1]
					if (next_item.lower() == element[1].lower()):
						if (element[0] == -1):
							ori_output.append(addTextLabel(text=element[1], label=case_label))
							comp_output.append(addTextLabel(text=next_item, label=case_label))
							case_diff_num += 1
						elif (element[0] == 1):
							comp_output.append(addTextLabel(text=element[1], label=case_label))
							ori_output.append(addTextLabel(text=next_item, label=case_label))
							case_diff_num += 1
						skip = True
					else:
						if (element[0] == -1):
							if (element[1].isspace()):
								ori_output.append(element[1])
							else:
								ori_output.append(addTextLabel(text=element[1], label=delete_label))
							deletion_num += 1
						elif (element[0] == 1):
							if (element[1].isspace()):
								comp_output.append(element[1])
							else:
								comp_output.append(addTextLabel(text=element[1], label=insert_label))
							insertion_num += 1
	else:
		for index, element in enumerate(diff):
			if (skip is True):
				skip = False
				continue
			if (element[0] == 0):
				ori_output.append(element[1])
				comp_output.append(element[1])
				skip = False
			elif (element[0] == -1 or element[0] == 1):
				if len(diff) == 1:
					if element[0] == -1:
						ori_output.append(addTextLabel(text=element[1], label=delete_label))
					elif element[0] == 1:
						comp_output.append(addTextLabel(text=element[1], label=insert_label))
					break
				next_item = diff[index + 1][1]
				if (next_item.lower() == element[1].lower()):
					ori_output.append(element[1])
					comp_output.append(element[1])
					skip = True
				else:
					if (element[0] == -1):
						if (element[1].isspace()):
							ori_output.append(element[1])
						else:
							ori_output.append(addTextLabel(text=element[1], label=delete_label))
						deletion_num += 1
					elif (element[0] == 1):
						if (element[1].isspace()):
							comp_output.append(element[1])
						else:
							comp_output.append(addTextLabel(text=element[1], label=insert_label))
						insertion_num += 1

	ori_output = "".join(ori_output)
	comp_output = "".join(comp_output)
	print("ori", ori_output)
	print("comp", comp_output)
	print("----------- end of 1 block comparison -----------")
	return ori_output, comp_output, insertion_num, deletion_num, case_diff_num


def get_group_of_text(data_frame):

	text = []

	for index, rows in data_frame.iterrows():
		text.append(rows['text'])

	block_text = ' '.join(text)

	return block_text


def get_data_frame():
	# Open file for reading in text mode (default mode)
	with open("output/ori.txt", 'r') as ori_txt:
		ori_list = json.load(ori_txt)
	with open("output/comp.txt", 'r') as comp_txt:
		comp_list = json.load(comp_txt)

	ori_data_frame = pd.DataFrame(columns=[*ori_list[0].keys()])
	block_num = 0
	for i in range(0, len(ori_list)):
		data = pd.DataFrame(ori_list[i])
		data['page_num'] = i + 1
		data['block_num_adjusted'] = data['block_num'] + block_num + 1
		block_num = data['block_num_adjusted'].max()
		ori_data_frame = ori_data_frame.append(data)

	comp_data_frame = pd.DataFrame(columns=[*comp_list[0].keys()])
	block_num = 0
	for i in range(0, len(comp_list)):
		data = pd.DataFrame(comp_list[i])
		data['page_num'] = i + 1
		data['block_num_adjusted'] = data['block_num'] + block_num + 1
		block_num = data['block_num_adjusted'].max()
		comp_data_frame = comp_data_frame.append(data)

	comp_txt.close()
	ori_txt.close()
	ori_data_frame["block_num_adjusted"] = ori_data_frame["block_num_adjusted"].apply(np.int64)
	comp_data_frame["block_num_adjusted"] = comp_data_frame["block_num_adjusted"].apply(np.int64)
	ori_data_frame.reset_index(inplace=True)
	comp_data_frame.reset_index(inplace=True)

	ori_data_frame = adjustWordNum(ori_data_frame)
	comp_data_frame = adjustWordNum(comp_data_frame)

	print(ori_data_frame.to_string())
	return ori_data_frame, comp_data_frame


def adjustWordNum(data_frame):
	for i in range(len(data_frame)):
		if (data_frame.loc[i, 'word_num'] == 0 or data_frame.loc[i, 'text'].strip() == ""):
			data_frame.loc[i, 'word_num'] = 0
			continue
		for j in range(i, 0, -1):
			if (data_frame.loc[j-1, 'word_num'] != 0):
				data_frame.loc[i, 'word_num'] = data_frame.loc[j-1, 'word_num'] + 1
				break
	return data_frame


def addTextLabel(text, label):

	if text == " ":
		return " "
	sentence = text.split()
	sentence_with_space = text.split(" ")
	lenWord = len(sentence)
	lenWord_space = len(sentence_with_space)
	first_text_num = 0
	last_text_num = 0
	labelS = label + "S"

	if (lenWord_space > lenWord) | (lenWord > 1):
		for num, str in enumerate(sentence_with_space):
			if str == sentence[0]:
				first_text_num = num
				break
		for num, str in enumerate(reversed(sentence_with_space)):
			if str == sentence[-1]:
				last_text_num = num
				break

		if lenWord == 1:
			sentence[0] = label + "-" + sentence[0]
			return " " * first_text_num + " ".join(sentence) + " " * last_text_num

		sentence[0] = labelS + "-" + sentence[0]
		sentence[-1] = sentence[-1] + "-" + labelS
		sentence = " " * first_text_num + " ".join(sentence) + " " * last_text_num
	else:
		sentence = label + "-" + sentence[0]

	return sentence


def append_position_list(data_frame, position_list, num, word, insert_or_delete):

	word_num = num + 1
	word_position = data_frame[(data_frame['text'] == word) & (data_frame['word_num'] == word_num)]
	word_page_num = word_position.iloc[0]['page_num']

	position_list.append([word_position.iloc[0]['page_num'],
				[word_position.iloc[0]['left'], word_position.iloc[0]['top'],
				word_position.iloc[0]['width'], word_position.iloc[0]['height']],
				insert_or_delete, word_position.iloc[0]['text']])

def cal_overlap_area(marked_region, diff_region):

	for i in range(1, len(marked_region)):

		marked_x1, marked_y1, marked_x2, marked_y2 = float(marked_region[i][0]), float(marked_region[i][1]),float(marked_region[i][2]),float(marked_region[i][3])
		diff_x1, diff_y1, diff_x2, diff_y2 = diff_region[0], diff_region[1], diff_region[2], diff_region[3]


		marked_polygon = Polygon([(marked_x1, marked_y1), (marked_x2, marked_y1),
						   (marked_x2, marked_y2), (marked_x1, marked_y2)])
		if (marked_polygon.area == 0):
			continue

		diff_polygon = Polygon([(diff_x1, diff_y1), (diff_x2, diff_y1),
						   (diff_x2, diff_y2), (diff_x1, diff_y2)])
		overlap_area = marked_polygon.intersection(diff_polygon).area/ marked_polygon.area
		if overlap_area > 0.6:
			return True
	return False

if __name__ == '__main__':
	compare_f1_f2()