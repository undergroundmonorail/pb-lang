#!/bin/python2

import sys
import time

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
	for line in code.split('\n'):
		if line[0] == ' ':
			print 'stop doing this horrible thing'
			1/0
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
	# Only ask for input the first time x>=0, y=-1 is read
	if y == -1 and x >= 0:
		get_input()
		
		def no_input_check(x,y):
			if (x, y) not in canvas:
				canvas[(x,y)] = (0, 0)
			return canvas[(x,y)]
		
		canvas_read.__code__ = no_input_check.__code__
	
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
	
def execute(tokens, delay):
	global X # l
	global Y # m
	global P # a
	global T # o
	
	global canvas
	
	for token in tokens:
		if delay != 0:
			output(delay)
			
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
				execute(code, delay)

curr_colour = 7

def get_input():
	global canvas
	
	if sys.stdin.isatty():
		# interactive input
		if curr_colour != 7:
			sys.stdout.write('\033[' + str(37) + 'm')
		print "Enter program's input. Empty line to terminate."
		
		user_input = '\n'.join(iter(raw_input, ''))
		
		if curr_colour != 7:
			sys.stdout.write('\033[' + str(30 + [7, 2, 3, 4, 5, 6, 0][curr_colour]) + 'm')
	else:
		user_input = sys.stdin.read()
	
	for x, c in enumerate(user_input):
		canvas[(x, -1)] = (ord(c), 0)

def output(delay, done=False):
	if delay != 0:
		sys.stdout.write('\033[2J\033[1;1f')
	
	for key in canvas.keys():
		if canvas[key] == (0, 0):
			del canvas[key]
	
	global curr_colour
	curr_colour = 7
	
	try:max_y = max(map(lambda t:t[1], canvas.keys()) + [1])
	except:max_y = 1
	
	for row in xrange(max_y + 1):
		try:max_x = max(map(lambda t:t[0], filter(lambda t:t[1] == row, canvas.keys())))
		except:max_x = 0
		
		o = []
		for column in xrange(max_x + 1):
			char, colour = canvas_read(column, row)
			char = char or 32
			o.append((char, colour))
		if o == [(32, 0)]:
			o = []
		
		if RAW:
			print o
		else:
			while delay != 0 and row == Y and len(o)-1 < X and not done:
				o.append((32, o[-1][1]) if o else (32, [7, 1, 2, 3, 4, 5, 6, 0][curr_colour]))
			
			buffer = ''
			for i, c in enumerate(o):
				c = (c[0], [7, 1, 2, 3, 4, 5, 6, 0][c[1]])
				if c[1] != [7, 1, 2, 3, 4, 5, 6, 0][curr_colour]:
					buffer += '\033[' + str(c[1]+30) + 'm'
					curr_colour = [7, 1, 2, 3, 4, 5, 6, 0][c[1]]
				if row == Y and X == i and delay != 0 and not done:
					buffer += colorama.Back.RED + chr(c[0]) + colorama.Back.RESET
				else:
					buffer += chr(c[0])
			print buffer
		
	while delay != 0 and row < Y and not done:
		row += 1
		if row == Y:
			column = 0
			while column < X:
				sys.stdout.write(' ')
				column += 1
			print colorama.Back.RED + ' ' + colorama.Back.RESET
		else: print
	
	if curr_colour != 7: sys.stdout.write('\033[' + str(37) + 'm')
	if delay != 0:
		time.sleep(delay / 1000.0)
		
				

def main(args):
	global RAW
	
	delay = 0
	for i, arg in enumerate(args):
		if arg.startswith("-d="):
			delay = int(arg[3:])
			args.pop(i)
			break
	for i, arg in enumerate(args):
		if arg.startswith('-r'):
			RAW = True
			args.pop(i)
			break
	
	if len(args) != 1:
		exit('Too many arguments!!')
	
	file = args[0]
	
	if not RAW:
		colorama.init()
	code = read_code(file)
	tokens = tokenize(code)
	execute(tokens, delay)
	if delay != 0:
		sys.stdout.write('\033[2J\033[1;1f')
	output(0, True)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		main(sys.argv[1:])
	else:
		exit('Usage: pbi.py program.pb')
