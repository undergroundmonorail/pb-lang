#!/bin/python2

import sys

def read_code(file):
	"""Strip comments and meaningless characters"""
	instructions = ('XYPBCT'
	                '><v^[]{}'
	                '0123456789'
	                '+-%/*()'
	                'ctbw!=')
	code = ''
	with open(file) as f:
		for line in f:
			line = line.split('#')[0] # strip comments
			code += ''.join(c for c in line if c in instructions)
	return code

def tokenize(code):
	"""Return a list of all the seperate tokens in the code"""
	tokens = []
	# combine [] and {} blocks into a single token
	square_depth = 0
	curly_depth = 0
	for c in code:
		if square_depth or curly_depth:
			tokens[-1] += c
		else:
			tokens.append(c)
		if c == '[':
			square_depth += 1
		elif c == ']':
			square_depth -= 1
		elif c == '{':
			curly_depth += 1
		elif c == '}':
			curly_depth -= 1
		assert square_depth >= 0
		assert curly_depth >= 0
	assert square_depth == 0
	assert curly_depth == 0
	# stick [] and {} tokens onto the instruction behind them
	while any(map(lambda t: t[0] in '[{', tokens)):
		for i, t in enumerate(tokens):
			if t[0] in '[{':
				tokens[i-1:i+1] = [tokens[i-1] + t]
	return tokens

def execute(tokens, canvas=None, X=0, Y=0, P=0, B=0, C=0, T=0):
	pass
		

def main(file):
	code = read_code(file)
	tokens = tokenize(code)
	
if __name__ == '__main__':
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		exit('Usage: pbi.py program.pb')
