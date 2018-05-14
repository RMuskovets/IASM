from asmast import *
from tkinter import *
def fopen(regs):
	regs['al'] = open(regs['eax'], regs['ebx'])
def fclose(regs):
	regs['al'].close()
	regs['al'] = None
def fread(stack, regs):
	stack.append(regs['al'].read())
def flen(stack, regs):
	import os
	stack.append(os.stat(regs['al'].name).st_size)
def fwrite(regs):
	regs['al'].write(regs['ecx'])
def get_in(stack):
	import sys
	stack.append(sys.stdin.readline())
def convert(type, regs, stack):
	stack.append(eval(type + '(' + regs['edx'] + ')'))
def length(stack, regs):
	stack.append(len(regs['al']))

def setval(regs, name, val):
	regs[name] = val

class Interpreter:
	regs = dict([(x, None) for x in 'eax ebx ecx edx al ah bl bh cl ch dl dh ax bx cx dx eip esp ebp ip sp bp esi\
		 edi si di of df if tf sf zf af pf cf cs ds ss es fs gs'.split()])
	def run(prog):
		stack = []
		variables = {}
		i = 0
		while i < len(prog.opers):
			goto = 0
			op = prog.opers[i]
			name = op.name
			if name == 'mov':
				reg = isinstance(op.ops[0], Register)
				val = Interpreter.regs[op.ops[0].name] if reg else op.ops[0].i
				Interpreter.regs[op.ops[1].name] = val
			elif name == 'set':
				reg = isinstance(op.ops[0], Register)
				val = Interpreter.regs[op.ops[0].name] if reg else op.ops[0].i
				variables[op.ops[1].name] = val
			elif name == 'sets':
				variables[op.ops[0].name] = stack[0]
				del stack[0]
			elif name == 'get':
				Interpreter.regs[op.ops[1].name] = variables[op.ops[0].name]
			elif name == 'gets':
				stack.append(variables[op.ops[0].name])
			elif name == 'add':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				stack.append(val1 + val2)
			elif name == 'sub':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				stack.append(val1 - val2)
			elif name == 'mul':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				stack.append(val1 * val2)
			elif name == 'div':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				stack.append(val1 / val2)
			elif name == 'shr':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				stack.append(val1 >> val2)
			elif name == 'shl':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				stack.append(val1 << val2)
			elif name == 'and':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				stack.append(val1 and val2)
			elif name == 'xor':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				stack.append(val1 ^ val2)
			elif name == 'or':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				stack.append(val1 or val2)
			elif name == 'not':
				reg = isinstance(op.ops[0], Register)
				val = Interpreter.regs[op.ops[0].name] if reg else op.ops[0].i
				stack.append(not val)
			elif name == 'push':
				reg = isinstance(op.ops[0], Register)
				val = Interpreter.regs[op.ops[0].name] if reg else op.ops[0].i
				stack.append(val)
			elif name == 'pop':
				assert isinstance(op.ops[0], Register)
				rgn = op.ops[0].name
				Interpreter.regs[rgn] = stack[-1]
				del stack[-1]
			elif name == 'int':
				functions = [
					lambda: fopen(Interpreter.regs),
					lambda: fclose(Interpreter.regs),
					lambda: fread(stack, Interpreter.regs),
					lambda: flen(stack, Interpreter.regs),
					lambda: fwrite(Interpreter.regs),
					lambda: print (Interpreter.regs['al']),
					lambda: get_in(stack),
					lambda: convert(int, Interpreter.regs, stack),
					lambda: convert(float, Interpreter.regs, stack),
					lambda: convert(str, Interpreter.regs, stack),
					lambda: length(stack, Interpreter.regs),
					lambda: stack.append(eval(Interpreter.regs['edx'])),
					lambda: exec(Interpreter.regs['edx'])
				]
				reg = isinstance(op.ops[0], Register)
				val = Interpreter.regs[op.ops[0].name] if reg else op.ops[0].i
				functions[val]()
			elif name == 'cmp':
				reg1 = isinstance(op.ops[0], Register)
				reg2 = isinstance(op.ops[1], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				val2 = Interpreter.regs[op.ops[1].name] if reg2 else op.ops[1].i
				vl = (0 if val1 == val2 else (-1 if val1 < val2 else 1))
				stack.append(vl)
			elif name == 'jmp':
				reg1 = isinstance(op.ops[0], Register)
				val1 = Interpreter.regs[op.ops[0].name] if reg1 else op.ops[0].i
				if stack[0]:
					goto = val1
			if goto:
				i = goto
				goto = 0
			else:
				i += 1
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument('file', help='The source IASM file')
	from asmlex import *
	args = parser.parse_args()
	text = open(args.file).read()
	lxr = Lexer()
	ast = Parser().parse(lxr.scan(text))
	Interpreter.run(ast)