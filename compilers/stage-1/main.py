from Lexer import *
import sys

if __name__ == '__main__':
	lexer = Lexer("/Users/juanpablocabreraquiroga/Documents/Compilers/compilers/stage-1/test_cases/bad/prog1.txt")
 
	
	token = lexer.scan()
	while token.tag != Tag.EOF:
		print(str(token))
		token = lexer.scan()
	print("END")