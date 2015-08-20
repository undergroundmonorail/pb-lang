#!/bin/python2

import sys

RAW = False

try:
	import colorama
except:
	answer = ''
	while answer not in list('ynYN'):
		answer = raw_input('Are you on Windows? (y/n)')
	if answer in 'yY':
		print 'You must install the colorama module before running this program if you wish to see the proper output.'
		RAW = True
	else:
		print "To stop seeing this message, install the colorama module."

# Some might say using global variables for this purpose is bad practice.
# I think those people could stand to be a little bit more adventurous.

canvas = { (0, 0):(0, 0)}
X = 0
Y = 0
P = 0
B = 0
C = 0
T = 0

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

def canvas_read(x, y):
	if (x, y) not in canvas:
		canvas[(x,y)] = (0, 0)
	return canvas[(x,y)]

def update():
	"""Update the B and C variables"""
	global B
	global C
	B, C = canvas_read(X, Y)

def expression(e):
	"""Return the result of an expression"""
	# TODO: make this not a piece of shit
	return eval(e, globals())
	
def execute(tokens):
	global X # l
	global Y # m
	global P # a
	global T # o
	
	global canvas
	
	for token in tokens:
		if token in '^v<>':
			token += '[1]'
		
		if token[0] == '^':
			Y -= expression(token[2:-1])
			update()
		elif token[0] == 'v':
			Y += expression(token[2:-1])
			update()
		elif token[0] == '<':
			X -= expression(token[2:-1])
			update()
		elif token[0] == '>':
			X += expression(token[2:-1])
			update()
		elif token[0] == 't':
			T = expression(token[2:-1])
		elif token[0] == 'b':
			canvas[(X, Y)] = (expression(token[2:-1]), P)
			update()
		elif token == 'c':
			P = (P + 1) % 8
		elif token[0] == 'w':
			condition = token.split('[')[1].split(']')[0]
			break_on_not = '=' in condition
			condition_1, condition_2 = condition.split('!='[break_on_not])
			code = tokenize(token[4+len(condition):-1])
			while (expression(condition_1) == expression(condition_2) and break_on_not) or (expression(condition_1) != expression(condition_2) and not break_on_not):
				execute(code)

def get_input():
	global canvas
	for x, c in enumerate(raw_input('Enter input: ')):
		canvas[(x, -1)] = (ord(c), 0)

def output():
	if not RAW: colorama.init()
	max_x = max(map(lambda t:t[0], canvas.keys()))
	max_y = max(map(lambda t:t[1], canvas.keys()))
	for row in xrange(max_y + 1):
		o = []
		for column in xrange(max_x + 1):
			char, colour = canvas_read(column, row)
			char = char or 32
			o.append((char, colour))
		if RAW:
			print o
		else:
			for i, c in enumerate(o):
				if c[1] == 0: o[i] = (c[0], 7)
				elif c[1] == 7: o[i] = (c[0], 0)
			print ''.join('\033[' + str(c[1]+30) + 'm' + chr(c[0]) for c in o)
				

def main(file):
	get_input()
	code = read_code(file)
	tokens = tokenize(code)
	execute(tokens)
	output()

if __name__ == '__main__':
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		exit('Usage: pbi.py program.pb')
