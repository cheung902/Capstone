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
from operator import itemgetter
from itertools import groupby


def compare_f1_f2(extract_list=""):
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
	extract_list = ["Name", "Address"]
	# try:
	# ignore_comp = session.get('ignore_region_comp')
	# shdChange_comp = session.get('shdChange_region_comp')
	# shdNotChange_comp = session.get('shdNotChange_region_comp')
	# ignore_ori = session.get('ignore_region_ori')
	# shdChange_ori = session.get('shdChange_region_ori')
	# shdNotChange_ori = session.get('shdNotChange_region_ori')
	# caseSensitive = session.get('caseSensitive')

	ignore_comp = []
	shdChange_comp = []
	shdNotChange_comp = []
	ignore_ori = []
	shdChange_ori = []
	shdNotChange_ori = []
	caseSensitive = []

	# except:
	# 	ignore_comp = ""
	# 	shdChange_comp = ""
	# 	shdNotChange_comp = ""
	# 	# ignore_region_ori = [['0', ['268.7658306188925', '1660.489706840391', '471.0328990228013', '1599.5325081433225']], ['0', ['268.7658306188925', '1242.1016612377848', '440.5542996742671', '1161.7489902280129']]]
	# 	# ignore_ori = [['0', ['274.30739413680783', '1649.4065798045604', '465.491335504886', '1596.7617263843647']], ['0', ['529.2193159609121', '1466.5349837133551', '734.2571661237786', '1419.4316938110749']], ['0', ['271.53661237785013', '1236.5600977198696', '437.78351791530946', '1164.5197719869705']]]
	# 	ignore_ori = [['0', ['410.0757003257329', '236.30788273615613', '626.19667752443', '172.57990228013037']]]
	# 	shdChange_ori = ""
	# 	shdNotChange_ori = ""


	ori_data_frame, comp_data_frame = get_data_frame()
	ori_max_page = ori_data_frame["page_num"].max()
	comp_max_page = comp_data_frame["page_num"].max()
	ori_text = get_group_of_text(ori_data_frame)
	comp_text = get_group_of_text(comp_data_frame)
	ori_overlap = overlapWithMarkedRegion(ori_data_frame, ignore_ori, "ori")
	comp_overlap = overlapWithMarkedRegion(comp_data_frame, ignore_comp, "comp")
	ori_diff, comp_diff, insertion_num, deletion_num, case_diff_num = diff_match(ori_text, comp_text, insertion_num,
																				 deletion_num, case_diff_num,
																				 insert_label, delete_label,
																				 case_label, caseSensitive)

	if (comp_diff != None):
		ori_word_position, pos_num_list_ori = get_position(diff_list=ori_diff,
										 insert_label=insert_label, delete_label=delete_label,
										 case_label = case_label)

		comp_word_position, pos_num_list_comp = get_position(diff_list=comp_diff,
										  insert_label=insert_label, delete_label=delete_label,
										  case_label = case_label)

		word_list_ori = removeOverlap(ori_data_frame, pos_num_list_ori, ori_overlap)
		word_list_comp = removeOverlap(comp_data_frame, pos_num_list_comp, comp_overlap)
		highlight(ori_data_frame, word_list_ori, "ori")
		highlight(comp_data_frame, word_list_comp, "comp")

	extractResult = extract_info(comp_data_frame, extract_list)
	for item in extractResult:
		print(item[0])
	return insertion_num, deletion_num, case_diff_num, ori_max_page, comp_max_page, extractResult

def get_position( diff_list, insert_label, delete_label, case_label):
	print("---------------Getting Word Number and Line Number-------------")
	position_list = []
	position_list_num = []
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
			word_end_num = 0
			word_start_num = num
			num +=1
			while insert_label_end not in diff_list_split[num]:
				num += 1
			if (insert_label_end in diff_list_split[num]):
				word_end_num = num
			position_list_num.append([["1"],[word_start_num+1, word_end_num+1]])
			continue
		elif delete_label_start in element:
			word_end_num = 0
			word_start_num = num
			num += 1
			while delete_label_end not in diff_list_split[num]:
				num += 1
			if delete_label_end in diff_list_split[num]:
				word_end_num = num
			position_list_num.append([["-1"],[word_start_num+1, word_end_num+1]])
			continue

		elif case_label_start in element:
			word_end_num = 0
			word_start_num = num
			num += 1
			while case_label_end not in diff_list_split[num]:
				num += 1
			if case_label_end in diff_list_split[num]:
				word_end_num = num
			position_list_num.append([["2"], [word_start_num+1, word_end_num+1]])
			continue

		elif delete_label in element:
			position_list_num.append(["1", [num+1]])

		elif insert_label in element:
			position_list_num.append(["1", [num+1]])
		elif case_label in element:

			position_list_num.append(["2", [num+1]])
	return position_list, position_list_num

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

def word_num_get_block_num(data_frame, word_num):
	return data_frame[data_frame['word_num'] == word_num].iloc[0]['block_num_adjusted']

def word_num_get_line_num(data_frame, word_num):
	return data_frame[data_frame['word_num'] == word_num].iloc[0]['line_num']

def word_num_get_page_num(data_frame, word_num):
	return data_frame[data_frame['word_num'] == word_num].iloc[0]['page_num']

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
		if overlap_area > 0:
			print("overlap_area: ", overlap_area)
			return True
	return False

def extract_info(data_frame, list):
	final_list = []

	print("Start extraction")
	for word in list:
		extracted_list = []
		block = data_frame[data_frame['text'].str.contains(word)][['block_num_adjusted','word_num','page_num']]
		# block_word_num = block.drop_duplicates(subset=["block_num_adjusted"]).values.tolist()
		# print(block)
		# print(block_word_num)
		block_word_num =  block.drop_duplicates(subset = ["block_num_adjusted"]).values.tolist()
		block_text = get_block_text(data_frame, word, block_word_num)
		print(block_text)
		for text in block_text:
			text_list = text[0].split(" ")
			extractSplit(word, text_list, extracted_list, text[1])
		final_list.append([word, extracted_list])
		# print("final", extracted_list)
	return final_list

def extractSplit(word, text, extracted_list, page_num):
	tmp_1 = []
	for index, str in enumerate(text):
		if len(text) == 1:
			extracted_list.append([text, page_num])
			return
		elif (index == len(text) - 1):
			extracted_list.append([text, page_num])
			return
		tmp_1.append(str)
		if word in text[index + 1]:
			extracted_list.append([tmp_1, page_num])
			tmp_2 = text[index+1:]
			extractSplit(word, tmp_2, extracted_list, page_num)
			break

def get_block_text(data_frame, word, block_num_list):
	text_list = []
	for index in block_num_list:
		block_num = index[0]
		word_num = index[1]
		page_num = index[2]
		text = data_frame[(data_frame['block_num_adjusted'] == block_num) & (data_frame['word_num']>= word_num)]['text'].values.tolist()
		text = " ".join(text)
		text_list.append([text, page_num])
	return text_list

def pypdf2_cv2_coordinates(dataFrame, compOrori):
	pdfInput = PdfFileReader(open("output/" + compOrori + ".pdf", "rb"))
	numOfPages = pdfInput.getNumPages()

	for pageIndex in range(0, numOfPages):
		page = pdfInput.getPage(pageIndex)
		pypdf2_height = page.mediaBox.getHeight()
		pypdf2_width = page.mediaBox.getWidth()

		#top left and bottom right
		img = cv2.imread('images/' + compOrori + '_' + str(pageIndex + 1) + ".tiff")
		cv2_height, cv2_width, _ = img.shape
		nh = pypdf2_height/cv2_height
		nw = pypdf2_width/cv2_width

		dataFrame.loc[dataFrame.page_num == pageIndex + 1, 'x_1'] = dataFrame['left'] * nw
		dataFrame.loc[dataFrame.page_num == pageIndex + 1, 'x_2'] = (dataFrame['left'] + dataFrame['width']) * nw
		dataFrame.loc[dataFrame.page_num == pageIndex + 1, 'y_1'] = (cv2_height - dataFrame['top'] - dataFrame['height']) * nh
		dataFrame.loc[dataFrame.page_num == pageIndex + 1, 'y_2'] = (cv2_height - dataFrame['top']) * nh
	return dataFrame

def overlapWithMarkedRegion(dataFrame, markedRegion, compOrori):
	word_num = []
	dataFrame = pypdf2_cv2_coordinates(dataFrame, compOrori)
	for index, row in dataFrame.iterrows():
		diff_region = [row['x_1'], row['y_1'], row['x_2'], row['y_2']]
		if markedRegion is not None:
			for marked in markedRegion:
				marked_pageIndex = int(marked[0][0])
				if (row['page_num'] - 1 == marked_pageIndex and row['word_num'] != 0):
					if (cal_overlap_area(marked, diff_region)):
						word_num.append(row['word_num'])
	return word_num

def removeOverlap(dataFrame, word_list, overlapWord_num):
	output_list = []
	print("ori_list", word_list)
	print(overlapWord_num)
	for index, diff in enumerate(word_list):
		word_num = diff[1]
		if len(word_num) == 1:
			if word_num[0] in overlapWord_num:
				print("removed: ", diff)
			else:
				output_list.append([diff[0], [diff[1]]])
				continue
		elif len(word_num) == 2:
			tmp = []
			tmp.extend(range(word_num[0], word_num[1] + 1))
			tmp = [x for x in tmp if x not in overlapWord_num]
			tmp = [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(tmp), lambda x: x[0]-x[1])]
			if len(tmp) != 0:
				tmp = [diff[0][0], tmp]
				output_list.append(tmp)
	print(output_list)
	return output_list

def highlight(dataFrame, word_list, compOrori):
	for position in (item for item in word_list):
		new_list = []
		for index, num_list in enumerate(position[1]):
			print("gg",num_list)
			if len(num_list) == 1:
				continue
			split_list(dataFrame, num_list, new_list)
			position[1] = new_list
		print("new", new_list)
	print(word_list)

	highlight_byType(dataFrame, word_list, compOrori)

def split_list(dataFrame, num_list, new_list):
	print("start",num_list )
	for index, num in enumerate(num_list):
		if len(num_list) == 1:
			new_list.append(num_list)
			return
		elif num == num_list[-1]:
			new_list.append(num_list)
			return
		elif (word_num_get_page_num(dataFrame, num) != word_num_get_page_num(dataFrame, num_list[index + 1])) or \
				(word_num_get_block_num(dataFrame, num) != word_num_get_block_num(dataFrame, num_list[index + 1])) or \
				(word_num_get_line_num(dataFrame, num) != word_num_get_line_num(dataFrame, num_list[index + 1])):
			tmp_2, tmp_3 = [],[]
			tmp_2.extend(range(num_list[0], num_list[index+1]))
			tmp_3.extend(range(num_list[index+1], num_list[-1] + 1))
			# tmp.append(split_list(dataFrame, tmp_3, new_list))
			print(tmp_2, "append", tmp_3)
			print("newlist append ", tmp_2)
			print("newlist recursive ", tmp_3)
			new_list.append(tmp_2)
			split_list(dataFrame, tmp_3, new_list)
			break

def highlight_byType(dataFrame, word_list, compOrori):
	print("Creating ", compOrori, ".pdf")
	print(word_list)
	pdfInput = PdfFileReader(open("output/" + compOrori + ".pdf", "rb"))
	numOfPages = pdfInput.getNumPages()
	pdfOutput = PdfFileWriter()

	for pageNum in range(0, numOfPages):
		page = pdfInput.getPage(pageNum)
		for chunk in word_list:
			type = chunk[0]
			for bounding in chunk[1]:
				getPage_num = word_num_get_page_num(dataFrame, bounding[0]) - 1
				if getPage_num == pageNum:
					if len(bounding) == 1:
						word_num = bounding[0]
						position = genBoundingWord(dataFrame, word_num)
					else:
						startNum = bounding[0]
						endNum = bounding[-1]
						position = genBoundingSentence(dataFrame, startNum, endNum)
						print(startNum, endNum, position)
					if type == "1":

						highlight = createHighlight(x1=position[0], y1=position[1], x2=position[2], y2=position[3],
															meta={"author": "", "contents": "Bla-bla-bla"},
															color=[0, 1, 0])
						addHighlightToPage(highlight, page, pdfOutput)
					elif type == "-1":
						highlight = createHighlight(x1=position[0], y1=position[1], x2=position[2], y2=position[3],
													meta={"author": "", "contents": "Bla-bla-bla"},
													color=[1, 0.5, 0])
						addHighlightToPage(highlight, page, pdfOutput)
					elif type == "2":
						highlight = createHighlight(x1=position[0], y1=position[1], x2=position[2], y2=position[3],
													meta={"author": "", "contents": "Bla-bla-bla"},
													color=[0, 0.5, 1])
						addHighlightToPage(highlight, page, pdfOutput)

		print("create page", pageNum)
		pdfOutput.addPage(page)
	outputStream = open("output/" + compOrori + "_final.pdf", "wb")
	pdfOutput.write(outputStream)

def genBoundingWord(dataFrame, wordNum):
	x_1 = dataFrame[dataFrame["word_num"] == wordNum].iloc[0]['x_1']
	x_2 = dataFrame[dataFrame["word_num"] == wordNum].iloc[0]['x_2']
	y_1 = dataFrame[dataFrame["word_num"] == wordNum].iloc[0]['y_1']
	y_2 = dataFrame[dataFrame["word_num"] == wordNum].iloc[0]['y_2']
	return [x_1, y_1, x_2, y_2]

def genBoundingSentence(dataFrame , startNum, endNum ):
	x_1 = dataFrame[dataFrame["word_num"] == startNum].iloc[0]['x_1']
	x_2 = dataFrame[dataFrame["word_num"] == endNum].iloc[0]['x_2']
	y_1 = min(dataFrame[dataFrame["word_num"] == startNum].iloc[0]['y_1'], dataFrame[dataFrame["word_num"] == endNum].iloc[0]['y_1'])
	y_2 = max(dataFrame[dataFrame["word_num"] == startNum].iloc[0]['y_2'], dataFrame[dataFrame["word_num"] == endNum].iloc[0]['y_2'])
	return [x_1, y_1, x_2, y_2]



if __name__ == '__main__':
	compare_f1_f2()