import sys

mode = sys.argv[1]
inputPath = sys.argv[2]

# reverse the content in InputFile and write it in OutputFile.
if mode == "reverse":
	if len(sys.argv) != 4:
		print("Usage for reverse: python3 file_manipulator.py reverse inputFile OutputFile") 
	else:
		outputPath = sys.argv[3]
		inFile = open(inputPath)
		content = inFile.read()
		inFile.close()
		
		outFile = open(outputPath, "w")
		reversedText = content[::-1]
		outFile.write(reversedText)
		outFile.close()
# copy the content of InputFile to OutputFile.
elif mode == "copy":
	if len(sys.argv) != 4:
		print("Usage for copy: python3 file_manipulator.py copy inputFile OutputFile") 
	else:
		outputPath = sys.argv[3]
		inFile = open(inputPath)
		content = inFile.read()
		inFile.close()
		
		outFile = open(outputPath, "w")
		outFile.write(content)
		outFile.close()
# dupulicate the content of InputFile n times.
elif mode == "duplicate-contents":
	if len(sys.argv) != 4:
		print("Usage for duplicate-contents: python3 file_manipulator.py duplicate-contents inputFile n") 
	else:
		n = int(sys.argv[3])
		inFile = open(inputPath)
		content = inFile.read()
		inFile.close()
		
		outFile = open(inputPath, "w")
		for i in range(0,n):
			outFile.write(content)
		outFile.close()
# replace the word needle in the content to newstring.
elif mode == "replace-string":
	if len(sys.argv) != 5:
		print("Usage for replace-string: python3 file_manipulator.py duplicate-string inputpath needle newstring") 
	else:
		needle = sys.argv[3]
		newstring = sys.argv[4]
		inFile = open(inputPath)
		content = inFile.read()
		inFile.close()
		
		cursor = 0
		words = []
		currentWord = ""
		
		while cursor < len(content):
			# 改行か空白が見つかったら単語としてwordsにcurrentWordを格納
			if content[cursor] == " " or content[cursor] == "\n":
				if currentWord != "":
					words.append(currentWord)
					if content[cursor] == "\n": words.append("\n")
				currentWord = ""
			else:
				currentWord += content[cursor]
			cursor += 1
		words.append(currentWord)	#最後の１単語
		
		outContent = ""
		for word in words:
			if word == needle:
				outContent += newstring + " "
			else:
				outContent += word + " "
				
		outFile = open(inputPath, "w")
		outFile.write(outContent)
		outFile.close()
else:
	print("Invalid command.")
