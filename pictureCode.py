# To-Do List
# output to file 
# add command line excutability
# suppress / deal with error messages when incorrect decode happens
# create and actually fill dictionary with lists of possible pixels to make quicker work of large files

from PIL import Image
import numpy as np
import sys, getopt, random

# reads the plain text file into a string
def readPlainTextFile(inputFile):
	file = open(inputFile, 'r')
	text = file.read()
	file.close()
	return(text)

# writing the encoded text to a file
def writeEncodedFile(encodedList, outputFile):
	file = open(outputFile, 'w')
	for element in encodedList:
		line=str(element)+"\n"
		file.write(line)
	file.close()

# reading in the encoded text from a file
def readEncodedFile(inputFile):
	with open(inputFile) as file:
		encodedList = file.read().splitlines()
	file.close()
	encodedList = list(map(int, encodedList))
	return(encodedList)

# encodes a string of text based on an image
def encode(text, image):
	print("Encoding the message")
	img = Image.open(image)
	pixelArray = np.array(img)
	encodedList = []
	for char in text:
		charValue = ord(char)
		RGB = random.randint(0,2)
		xyList = []
		for y in range(pixelArray.shape[1]):
			for x in range(pixelArray.shape[0]):
				if charValue == pixelArray[x,y][RGB]:
					xyList.append([x,y,RGB])
		print('.', end='', flush=True)
		encodedList.extend(xyList[random.randint(0,len(xyList)-1)])
	print()
	return(encodedList)

# takes an encoded list and returns a decoded string based on an image
def decode(encodedList, image):
	img = Image.open(image)
	pixelArray = np.array(img)
	decodedLetters = []
	for i in range(0,len(encodedList),3):
		x = encodedList[i]
		y = encodedList[i+1]
		RGB = encodedList[i+2]
		decodedLetters.append(chr(pixelArray[x,y][RGB]))
	decodedString = ''.join(decodedLetters)
	return(decodedString)

def main(argv):
	toEncode = False
	inputFile = ''
	outputFile = ''
	imageFile = ''
	plainText = ''

	if argv[0] == "decode":
		toEncode = False
	elif argv[0] == "encode":
		toEncode = True
	elif argv[0] == "-h":
		print("Encoding a message:")
		print(" pictureCode.py encode -i <FileWithPlainTextToEncode> -o <outputFile> -p <pictureFile>")
		print(" or")
		print(" pictureCode.py encode -o <outputFile> -p <pictureFile> -m <messageToBeEncoded>")
		print("Decoding a message:")
		print(" pictureCode.py decode -i <FileWithEncodedMessage> -p <picutreFile>")
		sys.exit(0)

	try:
		opts, args = getopt.getopt(argv[1:],"he:d:i:o:p:m:",["encode","decode","inputFile=","outputFile","pictureFile=","message="])
	except getopt.GetoptError:
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-i", "--inputFile"):
			inputFile = arg
		elif opt in ("-o","--outputFile"):
			outputFile = arg
		elif opt in ("-m","--message"):
			plainText = arg
		elif opt in ("-p", "--pictureFile"):
			imageFile = arg
		# Need to figure out how to avoid passing a -i and -m
		# For the moment -i will override -m
	if toEncode:
		# encoding the message
		if inputFile != '':
			plainText = readPlainTextFile(inputFile)
		writeEncodedFile(encode(plainText,imageFile),outputFile)
		print("Message encoded and saved in",outputFile)
	else:
		# decoding the message
		print(decode(readEncodedFile(inputFile),imageFile))

if __name__ == "__main__":
   main(sys.argv[1:])