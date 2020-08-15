def compare_f1_f2(comp,ori):


	# Open file for reading in text mode (default mode)
	comp_txt = open("output/" + comp + "_cleared.txt")
	ori_txt = open("output/" + ori + "_cleared.txt")
	comp_outfile = "output/" + comp + "_result.txt"
	ori_outfile = "output/" + ori + "_result.txt"
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
		else:
			comp_result.writelines("line " + str(line_no) + " is same as the original file\n")
			ori_result.writelines("line " + str(line_no) + " is same as the compare file\n")
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