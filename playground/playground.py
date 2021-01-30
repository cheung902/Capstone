def extractSplit(word, text, extracted_list):
	tmp_1 = []
	for index, str in enumerate(text):
		if len(text) == 1:
			extracted_list.append(str)
			return
		elif (str == text[-1]):
			extracted_list.append(text)
			return
		tmp_1.append(str)
		if word in text[index + 1]:
			extracted_list.append(tmp_1)
			tmp_2 = text[index+1:]
			print("1", tmp_1)
			print("2", tmp_2)
			extractSplit(word, tmp_2, extracted_list)
			break

extracted_list = []
word = "Name"
text =  ['Name:', 'Name:', 'Business', 'Registration', 'Business', 'Registration', 'Number:', 'Number:', 'Expiry', 'Date:', 'Expiry', 'Date:', 'Name:', 'Name:', 'Business', 'Registration', 'Business', 'Registration', 'Number:', 'Number:', 'Expiry', 'Date:', 'Expiry', 'Date:']
output = extractSplit(word, text, extracted_list)
print(output)
