#Name: Cripto 7.0
#Copyright: Cripto S.A
#Author: Érick Oliveira
#Date: 03/19/2019
#Description: Encoding Algorithm

import binascii
import string
import random
import math

class posGenerator:

		def generate(): #Generate a valid set of possibilities randomly
			possibleCharacters = string.ascii_letters + string.digits + "'!@#$%¨&*()-=+_|/?~[}]{^.,;><"
			pos = ''
			for i in range(0,16):
				flag = 0
				while flag != -1:
					rd = random.choice(possibleCharacters)
					flag = pos.find(rd)
				pos += rd
			return pos

class binaryOpeations:

	def decToBin(number): #get a binary code for a number (forcing 8 bits)
		temp = str(bin(number))
		binary = ''
		if number >= 47 and number <= 57:
			binary += '0'
		if number == 43:
			binary += '0'
		for bit in temp:
			if bit != 'b':
				binary += bit
		return binary

	def binToDec(string): #Converts a binary number to decimal
		soma = 0
		exp = len(string)-1
		for i in range(0,len(string)):
			if string[i] == '1':
				soma += 2 ** exp
			exp -= 1
		return soma

	def xor(bit1, bit2):
		if bit1 == bit2: 
			return False
		return True

	def separate(binary, length): #Split the binary input in blocks of 'length' bits
		separated = []
		aux = ''
		cont = 0
		for bit in binary:
			aux += bit
			cont += 1
			if cont == length:
				separated.append(aux)
				aux = ''
				cont = 0
		return separated

	def stringToBin(string): #Converts a string to binary
		binary = ''
		for letter in string:
			binary += binaryOpeations.decToBin(ord(letter))
		return binary

	def binaryToString(binary): #Converts binary string to an ascii string
		string = ''
		for byte in binary: 
			string += chr(binaryOpeations.binToDec(byte))
		return string

class cripto:

	def balanceKey(len_plain, key): #Balance key and plain text's length (for encoding)
		if len(key) < len_plain:
			key *= math.floor(len_plain/len(key)) + 1 
		return key

	def reverseAndHex(plain): #Reverse the input and encode it to hexadecimal
		return plain[::-1].encode('utf-8').hex()

	def calculateXOR(plain, key): #Doing XOR operation
		cont = -1
		output = ''
		for char in plain:
			cont += 1
			if binaryOpeations.xor(plain[cont], key[cont]):
				output += '1'
			else:
				output += '0'
		return output

	def getBlocksValue(blocks): #Gets the decimal value for each block of bits
		values = []
		for block in blocks:
			values.append(binaryOpeations.binToDec(block))
		return values

	def turnIntoChar(values): #Turns the block's values vector in a string
		output = ''
		for value in values:
			output += pos[value]
		return output

	def mapIntoValues(string): #Turns an encoded string to pos's values vector
		values = []
		for char in string:
			values.append(pos.find(char))
		return values

	def valuesTobin(values): #Converts each block's value to binary
		binary = []
		for value in values:
			binary.append(binaryOpeations.decToBin(value))
		return binary

	def force4bits(binary): #Forces 4 bits in a vector of binary numbers
		output = []
		for number in binary:
			if len(number) == 4:
				output.append(number)
			elif len(number) == 5:
				temp = ''
				for index in range(1,5):
					temp += number[index]
				output.append(temp)
			elif len(number) < 4:
				temp = ''
				for index in range(0,4-len(number)):
					temp += '0'
				temp += number
				output.append(temp)
		return output

	def joinBlocks(blocks): #Join separeted blocks
		output = ''
		for block in blocks:
			output += block
		return output

	def balanceKey2(len_binary, key): #Balances key and plain text's length (for decoding)
		len_plain = len_binary/8
		if len(key) < len_plain:
			key *= math.floor(len_plain/len(key)) + 1 
		return key

	def filter(string): #Removes unwanted characters from binascii.unhexlify's function output
		output = ''
		for index in range(1,len(string)-1):
			if string[index] != "'":
				output += string[index]	
		return output

	def unhexAndReverse(string): #Decodes a string from hexadecimal and reverse it
		return cripto.filter(str(binascii.unhexlify(string))[::-1])

	def decode(encoded, key): #Decodes an encoded text
		values = cripto.mapIntoValues(encoded)
		binary = cripto.valuesTobin(values)
		blocks = cripto.force4bits(binary)
		joined = cripto.joinBlocks(blocks)
		key = cripto.balanceKey2(len(joined), key)
		key = binaryOpeations.stringToBin(key)
		xor_output = cripto.calculateXOR(joined,key)
		separated = binaryOpeations.separate(xor_output, 8)
		string = binaryOpeations.binaryToString(separated)
		string = cripto.unhexAndReverse(string)
		return string

	def encode(plain, key): #Encodes a plain text
		plain = cripto.reverseAndHex(plain)
		key = cripto.balanceKey(len(plain), key)
		plain = binaryOpeations.stringToBin(plain)
		key = binaryOpeations.stringToBin(key)
		xor_output = cripto.calculateXOR(plain,key)
		separated = binaryOpeations.separate(xor_output, 4)
		values = cripto.getBlocksValue(separated)
		output = cripto.turnIntoChar(values)
		return output

#Usage
pos = posGenerator.generate() #To generate a valid set of possi
#pos = 'SlgORwyf4bZqDdEQ' #Using a given set of possibilities
ent = 'Futebol eh um esporte estranho' #Input
key = 'cavaloassado' #Output
encoded = cripto.encode(ent, key)
print('Set of possibilities: {}'.format(pos))
print(encoded)
decoded = cripto.decode(encoded, key)
print(decoded)