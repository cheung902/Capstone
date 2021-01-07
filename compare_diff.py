import json
import pandas as pd
import difflib as diff
from commonFNC import *
from fpdf import FPDF
import diff_match_patch as dmp_module
import numpy as np
import cv2


def compare_f1_f2():

	print("-----------------------------------")
	print("Comparing files ")
	print("-----------------------------------")

	ori_word_position = []
	comp_word_position = []
	#Comparison Report
	insertion_num = 0
	deletion_num = 0

	ori_data_frame, comp_data_frame = get_data_frame()

	ori_max_block = ori_data_frame["block_num_adjusted"].max()
	comp_max_block = comp_data_frame["block_num_adjusted"].max()
	ori_max_page = ori_data_frame["page_num"].max()
	comp_max_page = comp_data_frame["page_num"].max()

	for ori_block_num in range(0, ori_max_block):
		ori_block_text = get_group_of_text(ori_data_frame, "block_num_adjusted", ori_block_num)
		ori_block_text = " ".join(ori_block_text)

		for comp_block_num in range(ori_block_num, comp_max_block):
			comp_block_text = get_group_of_text(comp_data_frame, "block_num_adjusted", comp_block_num)
			comp_block_text = " ".join(comp_block_text)

			comparing_text_block = diff.SequenceMatcher(None, ori_block_text, comp_block_text)
			block_similarity = comparing_text_block.ratio()

			if block_similarity == 1 and ori_block_num == comp_block_num:
				break

			elif block_similarity > 0.8 and block_similarity != 1:

				block_inserted = comp_block_num - ori_block_num
				ori_data_frame['block_num_adjusted'].values[ori_data_frame['block_num_adjusted'] >= ori_block_num] += block_inserted
				ori_diff, comp_diff, insertion_num, deletion_num = diff_match(ori_block_text, comp_block_text, insertion_num, deletion_num)
				if (comp_diff != None):

					comp_word_and_line_num = get_diff_word_and_line_num(data_frame= comp_data_frame,
																		diff_list = comp_diff,
																		block_num= comp_block_num)

					ori_word_and_line_num = get_diff_word_and_line_num(data_frame=ori_data_frame,
																		diff_list=ori_diff,
																		block_num=ori_block_num)

					comp_word_position = get_word_position(data_frame = comp_data_frame,
														   block_num = comp_block_num,
														   word_and_line_num_list = comp_word_and_line_num,
														   position_list = comp_word_position)


					ori_word_position = get_word_position(data_frame=ori_data_frame,
														   block_num=ori_block_num,
														   word_and_line_num_list=ori_word_and_line_num,
														   position_list=ori_word_position)

					break
	label_word(ori_word_position, ori_max_page, "ori")
	label_word(comp_word_position, comp_max_page, "comp")
	return insertion_num, deletion_num, ori_max_page, comp_max_page

def get_word_position(data_frame, block_num, word_and_line_num_list, position_list):
	for index, row in data_frame.iterrows():
		if row['block_num_adjusted'] == block_num:
			for i in word_and_line_num_list:
				if i[0] == row['word_num'] and i[1] == row['line_num']:
					# print("word number:", diff_word)
					# print("word:", row['text'])
					# print(row['block_num_adjusted'], comp_block_num, comp_diff)
					position_list.append(
						[data_frame.loc[index, ["page_num", "height", "left", "top", "width", "text"]],i[2]])

	return position_list

def get_diff_word_and_line_num(data_frame, diff_list, block_num):
	list = []
	diff_list_split = diff_list.split()
	for i, element in enumerate(diff_list_split):
		if "**%%$$*" in element:
			word = element.replace("**%%$$*", "")
			line = data_frame[(data_frame['text'] == word)
											& (data_frame['block_num_adjusted'] == block_num)
											& (data_frame['word_num'] == i + 1)]['line_num'].values
			list.append([i + 1, line, "-1"])
		elif "**%%$$#" in element:
			word = element.replace("**%%$$#", "")
			line = data_frame[(data_frame['text'] == word)
							  & (data_frame['block_num_adjusted'] == block_num)
							  & (data_frame['word_num'] == i + 1)]['line_num'].values
			list.append([i + 1, line, "1"])
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
					print(item[0]['text'])
					cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 0, 0), -1)
				else:
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
	return ori_data_frame, comp_data_frame

def diff_match(line1, line2, insertion_num, deletion_num):

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
			ori_output.append(addTextLabel(i[1], "**%%$$*"))
			comp_output.append("**%%$$*")
			deletion_num+=1
		elif i[0] == 1:
			ori_output.append("**%%$$#")
			comp_output.append("**%%$$#" + i[1])
			insertion_num+=1

	diff = dmp.diff_main(line2, line1)
	dmp.diff_cleanupEfficiency(diff)
	ori_output = "".join(ori_output)
	comp_output = "".join(comp_output)
	print("ori",ori_output)
	print("comp", comp_output)
	print("----------- end of 1 block comparison -----------")
	return ori_output, comp_output, insertion_num, deletion_num

def get_group_of_text(data_frame, col_name, block_num):

	text = []
	block_num = block_num
	block_text = data_frame[data_frame[col_name] == block_num]['text']

	for i in block_text:
		text.append(i)

	block_text = ' '.join(text)
	block_text = block_text.split("  ")
	block_text = [x for x in block_text if x]

	return block_text

def delete_line(original_file, line_number):

	""" Delete a line from a file at the given line number """
	is_skipped = False
	current_index = 0
	dummy_file = original_file + '.bak'
	# Open original file in read only mode and dummy file in write mode
	with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
		# Line by line copy data from original file to dummy file
		for line in read_obj:
			# If current line number matches the given line number then skip copying
			if current_index != line_number:
				write_obj.write(line)
			else:
				is_skipped = True
			current_index += 1
	# If any line is skipped then rename dummy file as original file
	if is_skipped:
		os.remove(original_file)
		os.rename(dummy_file, original_file)
	else:
		os.remove(dummy_file)

def addTextLabel(text, symbol):
	text = text.split(" ")
	lenText = len(text)
	output = ""
	for num, item in enumerate(text):
		if item != "":
			output = symbol + item
			output = " " * num + output
			if lenText > num:
				output = output + " " * (lenText - num - 1)
	return output

if __name__ == '__main__':
	insertion_num, deletion_num, ori_max_page, comp_max_page = compare_f1_f2()
	print(insertion_num,deletion_num)