def compare_f1_f2(f1,f2):
	with open('output/' + f1, 'r') as file1:
		with open('output/' + f2, 'r') as file2:
			difference = set(file1).difference(file2)
	difference.discard('\n')

	with open('diff/diff.txt', 'w') as file_out:
		for line in difference:
			file_out.write(line)