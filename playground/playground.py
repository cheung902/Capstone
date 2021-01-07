import re
string = "  insert me lah ok  "
print(len(string))

print(string)

num_in_string = len(string)
print(num_in_string)

def addTextLabel(text):
	text = text.split(" ")
	print(text)
	lenText = len(text)
	tmp =[]
	output = ""

	for num,i in enumerate(text):
		if i != "":
			tmp.append(num)

	for num, item in enumerate(text):
		if item != "":
			output = "**##$$" + item
			output = "1" * num + output
			if lenText > num:
				output = output + "1" * (lenText - num - 1)
	return output
print(addTextLabel(string))