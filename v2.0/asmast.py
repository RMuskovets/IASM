class Node:
	pass
class Operand(Node):
	def __init__(self, name, args, lineno):
		super(Operand, self).__init__()
		self.ops = args
		self.name = name
		self.lineno = lineno
	def __str__(self):
		return ('Operand %s: [' + str(self.ops) + ']') % self.name
class Register(Node):
	def __init__(self, name):
		super(Register, self).__init__()
		self.name = name
	def __str__(self):
		return str(type(self)) + ': ' + self.name
class String(Node):
	def __init__(self, data):
		super(String, self).__init__()
		self.i = data[1:-1]
	def __str__(self):
		return str(type(self)) + ': ' + str(self.data)
class Int(Node):
	def __init__(self, i):
		super(Int, self).__init__()
		self.i = i
	def __str__(self):
		return str(type(self)) + ': ' + str(self.i)
class Program(Node):
	count = 0
	def __init__(self, opers):
		Program.count += 1
		self.count = Program.count
		self.opers = opers
	def __str__(self):
		return '%s: #%s, [%s]' % ('Program', self.count, str(self.opers))
class Id(Register):
	def __init__(self, name):
		super(Id, self).__init__(name)
class Parser:
	def parse(self, lex):
		lex = [x for x in lex]
		for x in lex:
			if x[0] == 'COMMENT' or x[0] == 'COMMA':
				del lex[lex.index(x)]
		opers = []
		i = 0
		while i < len(lex):
			d = lex[i]
			a = Node()
			if d[0] == 'OPERAND':
				a = Operand(d[1], [], i+1)
				i += 1
				while i < len(lex) and lex[i][0] != 'OPERAND' and lex[i][0] != 'END':
					d = lex[i]
					b = Node()
					i += 1
					if d[0] == 'REGISTER':
						b = Register(d[1])
					elif d[0] == 'INT' or d[0] == 'HEX':
						b = Int(int(d[1], 10 if 'a' not in d[1].lower() else 16))
					elif d[0] == 'STRING':
						b = String(d[1])
					elif d[0] == 'ID':
						b = Id(d[1])
					a.ops += [b]
				i -= 1
			opers += [a]
			i += 1
		return Program(opers)

def test(lex):
	print(Parser().parse(lex))