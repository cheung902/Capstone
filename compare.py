import shutil
import os

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

def compare_f1_f2():


	# Open file for reading in text mode (default mode)
	comp_txt = open("output/comp.txt")
	ori_txt = open("output/ori.txt")
	comp_outfile = "output/comp_result.txt"
	ori_outfile = "output/ori_result.txt"
	comp_result = open(comp_outfile, "a")
	ori_result = open(ori_outfile, "a")
	# Print confirmation
	print("-----------------------------------")
	print("Comparing files ")
	print("-----------------------------------")

	# Read the first line from the files
	comp_line = comp_txt.readline()
	ori_line = ori_txt.readline()

	# Initialize counter for line number
	line_no = 1

	# Loop if either file1 or file2 has not reached EOF
	while comp_line != '' or ori_line != '':

		# Strip the leading whitespaces
		comp_line = comp_line.rstrip()
		ori_line = ori_line.rstrip()

		# Compare the lines from both file
		if comp_line != ori_line:
			comp_result.writelines(comp_line + "\n")
			ori_result.writelines(ori_line + "\n")
		# Read the next line from the file
		comp_line = comp_txt.readline()
		ori_line = ori_txt.readline()

		# Increment line counter
		line_no += 1


	# Close the files
	comp_txt.close()
	ori_txt.close()
	comp_result.close()
	ori_result.close()

	totalPageComp = open("output/comp_cleared.txt").readlines()[-1]
	shutil.copy('output/comp_result.txt', 'compare/comp/pdfs/comp.txt')

	for i in range(1, int(totalPageComp) + 1):
		with open("compare/comp/pdfs/comp.txt") as file, open("compare/comp/pdfs/" + str(i) + "_.txt", "w") as file2:
			for line in file:
				if line != str(i)+'\n':
					file2.write(line)
					delete_line("compare/comp/pdfs/comp.txt", 0)
				else:
					delete_line("compare/comp/pdfs/comp.txt", 0)
					break

if __name__ == '__main__':
	compare_f1_f2()