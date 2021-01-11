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

	ori_word_position = []
	comp_word_position = []

	#label
	insert_label = "G_label"
	delete_label = "R_label"

	#Comparison Report
	insertion_num = 0
	deletion_num = 0

	ori_data_frame, comp_data_frame = get_data_frame()

	ori_max_page = ori_data_frame["page_num"].max()
	comp_max_page = comp_data_frame["page_num"].max()

	ori_text = get_group_of_text(ori_data_frame)
	comp_text = get_group_of_text(comp_data_frame)

	ori_diff, comp_diff, insertion_num, deletion_num = diff_match(ori_text, comp_text,
																  insertion_num, deletion_num,
																  insert_label, delete_label)

	if (comp_diff != None):
		comp_word_and_line_num = get_diff_word_and_line_num(data_frame=comp_data_frame, diff_list=comp_diff,
															insert_label=insert_label, delete_label=delete_label)

		ori_word_and_line_num = get_diff_word_and_line_num(data_frame=ori_data_frame, diff_list=ori_diff,
														   insert_label=insert_label, delete_label=delete_label)

		comp_word_position = get_word_position(data_frame=comp_data_frame,
											   word_and_line_num_list=comp_word_and_line_num,
											   position_list=comp_word_position)

		ori_word_position = get_word_position(data_frame=ori_data_frame,
											  word_and_line_num_list=ori_word_and_line_num,
											  position_list=ori_word_position)

	label_word(ori_word_position, ori_max_page, "ori")
	label_word(comp_word_position, comp_max_page, "comp")

	return insertion_num, deletion_num, ori_max_page, comp_max_page

def get_word_position(data_frame, word_and_line_num_list, position_list):
	for index, row in data_frame.iterrows():
		for i in word_and_line_num_list:
			if i[0] == row['word_num'] and i[1] == row['line_num']:
				position_list.append(
					[data_frame.loc[index, ["page_num", "height", "left", "top", "width", "text"]],i[2]])

	return position_list

def get_diff_word_and_line_num(data_frame, diff_list, insert_label, delete_label):
	print("---------------Getting Word Number and Line Number-------------")
	list = []
	diff_list_split = diff_list.split()
	insert_label_start = insert_label + "S-"
	insert_label_end = "-" + insert_label + "S"
	delete_label_start = delete_label + "S-"
	delete_label_end = "-" + delete_label + "S"
	insert_label = insert_label + "-"
	delete_label = delete_label + "-"

	for num, element in enumerate(diff_list_split):
		if insert_label_start in element:
			word = element.replace(insert_label_start, "")
			line = data_frame[(data_frame['text'] == word)
											& (data_frame['word_num'] == num + 1)]['line_num'].values
			list.append([num + 1, line, "1"])
			num +=1
			while insert_label_end not in diff_list_split[num]:

				word = diff_list_split[num].replace(insert_label_end, "")
				line = data_frame[(data_frame['text'] == word)
								  & (data_frame['word_num'] == num + 1)]['line_num'].values
				list.append([num + 1, line, "1"])
				num += 1
			if insert_label_end in diff_list_split[num]:
				word = diff_list_split[num].replace(insert_label_end, "")
				line = data_frame[(data_frame['text'] == word)
								  & (data_frame['word_num'] == num + 1)]['line_num'].values
				list.append([num + 1, line, "1"])
				break

		elif delete_label_start in element:
			word = element.replace(delete_label_start, "")
			line = data_frame[(data_frame['text'] == word)
											& (data_frame['word_num'] == num + 1)]['line_num'].values
			list.append([num + 1, line, "-1"])
			num +=1
			while delete_label_end not in diff_list_split[num]:
				word = diff_list_split[num].replace(delete_label_end, "")
				line = data_frame[(data_frame['text'] == word)
								  & (data_frame['word_num'] == num + 1)]['line_num'].values
				list.append([num + 1, line, "-1"])
				num += 1
			if delete_label_end in diff_list_split[num]:
				word = diff_list_split[num].replace(delete_label_end, "")
				line = data_frame[(data_frame['text'] == word)
								  & (data_frame['word_num'] == num + 1)]['line_num'].values
				list.append([num + 1, line, "-1"])
				break

		elif delete_label in element:
			word = element.replace(delete_label, "")
			line = data_frame[(data_frame['text'] == word)
											& (data_frame['word_num'] == num + 1)]['line_num'].values
			list.append([num + 1, line, "-1"])
		elif insert_label in element:
			word = element.replace(insert_label, "")
			line = data_frame[(data_frame['text'] == word)
							  & (data_frame['word_num'] == num + 1)]['line_num'].values
			list.append([num + 1, line, "1"])
	return list

def label_word(diff_list, max_page, compOrori):
	page_exist = []
	for item in diff_list:
		page_exist.append(item[0][0])
	page_exist = list(set(page_exist))

	for page in page_exist:
		img = cv2.imread('images/' + compOrori + '_' + str(page) + ".tiff")
		overlay = img.copy()
		for item in diff_list:
			if item[0][0] == page:
				(x, y, w, h) = (item[0]['left'], item[0]['top'], item[0]['width'], item[0]['height'])
				if item[1] == "-1":
					print(x,y,w,h)
					print("Deleted: ", item[0]['text'])
					cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 0, 0), -1)
				else:
					print("Inserted: ", item[0]['text'])
					cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), -1)
				alpha = 0.1  # Trxansparency factor.
				# Following line overlays transparent rectangle over the image
				img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)


				cv2.imwrite('compare/' + compOrori + '/images/'+ compOrori+'_' + str(page) + '.tiff', img_new)

	pdf_paths = []
	for i in range(1,max_page):
		input_path = "compare/" + compOrori +"/images/"+compOrori+"_" + str(i) + ".tiff"
		output_path = "compare/" + compOrori + "/pdfs/"+compOrori+"_" + str(i) + ".pdf"
		pdf_paths.append(output_path)

		createSearchablePDF(input_path = input_path, output_path = output_path)
		# pdf_paths.append("output/diff" + str(i) + ".pdf")
		# with open("output/diff" + str(i) +".pdf", "wb") as pdf:
		# 	pdf.write(img2pdf.convert("compare/comp/images/comp_" + str(i) + ".tiff"))

	out_path = "output/" + compOrori + ".pdf"
	mergePDF(pdf_paths, out_path)
	#removeFiles(pdf_paths)

def diff_match(line1, line2, insertion_num, deletion_num, insert_label, delete_label):

	ori_output = []
	comp_output = []

	dmp = dmp_module.diff_match_patch()
	diff = dmp.diff_main(line1, line2)
	dmp.diff_cleanupEfficiency(diff)
	print("line1: ", line1)
	print("line2: ", line2)
	print("difference: ", diff)
	for i in diff:
		if i[0] == 0:
			ori_output.append(i[1])
			comp_output.append(i[1])
			pass
		elif i[0] == -1:
			ori_output.append(addTextLabel(text = i[1], label = delete_label))
			deletion_num+=1
		elif i[0] == 1:
			comp_output.append(addTextLabel(text = i[1], label = insert_label))
			insertion_num+=1

	ori_output = "".join(ori_output)
	comp_output = "".join(comp_output)
	print("ori",ori_output)
	print("comp", comp_output)
	print("----------- end of 1 block comparison -----------")
	return ori_output, comp_output, insertion_num, deletion_num

def get_group_of_text(data_frame):

	text = []

	for index,rows in data_frame.iterrows():
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
	for i in range(0,len(ori_list)):
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

	print(comp_data_frame.to_string())
	return ori_data_frame, comp_data_frame

def adjustWordNum(data_frame):
	for i in range(len(data_frame)):
		if data_frame.loc[i, 'word_num'] !=0:
			for j in range(i, 0, -1):
				if data_frame.loc[j-1, 'word_num'] != 0:
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

	if lenWord_space > lenWord:
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
			return " "* first_text_num + " ".join(sentence) + " "* last_text_num

		sentence[0] = labelS + "-" + sentence[0]
		sentence[-1] = sentence[-1] + "-" + labelS
		sentence = " " * first_text_num + " ".join(sentence) + " " * last_text_num
	else:
		sentence = label + "-" + sentence[0]

	return sentence

if __name__ == '__main__':
	compare_f1_f2()