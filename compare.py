import json
import pandas as pd
from commonFNC import *
import diff_match_patch as dmp_module
import numpy as np
import cv2


def compare_f1_f2():

	print("-----------------------------------")
	print("Comparing files ")
	print("-----------------------------------")

	# label
	insert_label = "G_label"
	delete_label = "R_label"
	caseSensitive = True
	# Comparison Report
	insertion_num = 0
	deletion_num = 0

	ori_data_frame, comp_data_frame = get_data_frame()
	ori_max_page = ori_data_frame["page_num"].max()
	comp_max_page = comp_data_frame["page_num"].max()
	ori_text = get_group_of_text(ori_data_frame)
	comp_text = get_group_of_text(comp_data_frame)

	ori_diff, comp_diff, insertion_num, deletion_num = diff_match(ori_text, comp_text,
																  insertion_num, deletion_num,
																  insert_label, delete_label, caseSensitive)

	if (comp_diff != None):
		ori_word_position = get_position(data_frame=ori_data_frame, diff_list=ori_diff,
										 insert_label=insert_label, delete_label=delete_label)

		comp_word_position = get_position(data_frame=comp_data_frame, diff_list=comp_diff,
										  insert_label=insert_label, delete_label=delete_label)

		label_word(ori_word_position, ori_max_page, "ori")
		label_word(comp_word_position, comp_max_page, "comp")

	return insertion_num, deletion_num, ori_max_page, comp_max_page

def get_word_position(data_frame, word_and_line_num_list, position_list):
	for index, row in data_frame.iterrows():
		for i in word_and_line_num_list:
			if i[0] == row['word_num'] and i[1] == row['line_num']:
				position_list.append(
					[data_frame.loc[index, ["page_num", "height", "left", "top", "width", "text"]], i[2]])

	return position_list


def get_position(data_frame, diff_list, insert_label, delete_label):
	print("---------------Getting Word Number and Line Number-------------")
	print(diff_list)
	position_list = []
	diff_list_split = diff_list.split()
	insert_label_start = insert_label + "S-"
	insert_label_end = "-" + insert_label + "S"
	delete_label_start = delete_label + "S-"
	delete_label_end = "-" + delete_label + "S"
	insert_label = insert_label + "-"
	delete_label = delete_label + "-"
	print(diff_list_split)
	for num, element in enumerate(diff_list_split):
		if (insert_label_start in element):
			word = element.replace(insert_label_start, "")
			append_position_list(data_frame = data_frame, position_list = position_list, num = num, word = word, insert_or_delete="1")
			num +=1
			while insert_label_end not in diff_list_split[num]:
				word = diff_list_split[num]
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word = word, insert_or_delete="1")
				num += 1

			if (insert_label_end in diff_list_split[num]):
				word = diff_list_split[num].replace(insert_label_end, "")
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word = word, insert_or_delete="1")
				continue

		elif delete_label_start in element:
			word = element.replace(delete_label_start, "")
			append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="-1")
			num += 1
			while delete_label_end not in diff_list_split[num]:
				word = diff_list_split[num]
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="-1")
				num += 1
			if delete_label_end in diff_list_split[num]:
				word = diff_list_split[num].replace(delete_label_end, "")
				append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="-1")
				continue

		elif delete_label in element:
			word = element.replace(delete_label, "")
			append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="-1")

		elif insert_label in element:
			word = element.replace(insert_label, "")
			append_position_list(data_frame=data_frame, position_list=position_list, num=num, word=word, insert_or_delete="1")

	return position_list


def label_word(diff_list, max_page, compOrori):
	page_exist = []
	for item in diff_list:
		page_exist.append(item[0])
	page_exist = list(set(page_exist))

	for page in page_exist:
		img = cv2.imread('images/' + compOrori + '_' + str(page) + ".tiff")
		overlay = img.copy()
		for item in diff_list:
			if item[0] == page:
				(x, y, w, h) = (item[1][0], item[1][1], item[1][2], item[1][3])
				if item[2] == "-1":
					print("Deleted: ", item[3])
					cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 0, 0), -1)
				else:
					print("Inserted: ", item[3])
					cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), -1)
				alpha = 0.1  # Trxansparency factor.
				# Following line overlays transparent rectangle over the image
				img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
				cv2.imwrite('compare/' + compOrori + '/images/' + compOrori + '_' + str(page) + '.tiff', img_new)

	pdf_paths = []
	for i in range(1, max_page):
		input_path = "compare/" + compOrori + "/images/" + compOrori	+ "_" + str(i) + ".tiff"
		output_path = "compare/" + compOrori + "/pdfs/" + compOrori + "_" + str(i) + ".pdf"
		pdf_paths.append(output_path)

		createSearchablePDF(input_path=input_path, output_path=output_path)
		# pdf_paths.append("output/diff" + str(i) + ".pdf")
		# with open("output/diff" + str(i) +".pdf", "wb") as pdf:
		# 	pdf.write(img2pdf.convert("compare/comp/images/comp_" + str(i) + ".tiff"))

	out_path = "output/" + compOrori + ".pdf"
	mergePDF(pdf_paths, out_path)
	# removeFiles(pdf_paths)


def diff_match(line1, line2, insertion_num, deletion_num, insert_label, delete_label, caseSensitive):

	ori_output = []
	comp_output = []

	dmp = dmp_module.diff_match_patch()
	diff = dmp.diff_main(line1, line2)
	dmp.diff_cleanupEfficiency(diff)
	print("line1: ", line1)
	print("line2: ", line2)
	print("difference: ", diff)

	skip = False
	print("CaseSensitive: ", caseSensitive)
	if caseSensitive is True:
		for i in diff:
			if i[0] == 0:
				ori_output.append(i[1])
				comp_output.append(i[1])
				pass
			elif i[0] == -1:
				ori_output.append(addTextLabel(text=i[1], label=delete_label))
				deletion_num += 1
			elif i[0] == 1:
				comp_output.append(addTextLabel(text=i[1], label=insert_label))
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
				next_item = diff[index + 1][1]
				if (next_item.lower() == element[1].lower()):
					ori_output.append(element[1])
					comp_output.append(element[1])
					skip = True
				else:
					if (element[0] == -1):
						ori_output.append(addTextLabel(text=element[1], label=delete_label))
					elif (element[0] == 1):
						comp_output.append(addTextLabel(text=element[1], label=insert_label))

	ori_output = "".join(ori_output)
	comp_output = "".join(comp_output)
	print("ori", ori_output)
	print("comp", comp_output)
	print("----------- end of 1 block comparison -----------")
	return ori_output, comp_output, insertion_num, deletion_num


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
	print(text, sentence)
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
	print(word, word_num)
	position_list.append([word_position.iloc[0]['page_num'],
				[word_position.iloc[0]['left'], word_position.iloc[0]['top'],
				word_position.iloc[0]['width'], word_position.iloc[0]['height']],
				insert_or_delete, word_position.iloc[0]['text']])


if __name__ == '__main__':
	compare_f1_f2()