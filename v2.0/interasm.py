from compiler import Interpreter as interp
from asmast import Parser as pars
from asmlex import Lexer as lex

inp = '>>> '
exit = 'quit;;'
print ('IASM interactive line.')
print ('To quit, type "%s"' % exit)
lxr = lex()
psr = pars()

s = ''
while s.rstrip() != exit:
	try:
		s = input(inp)
		ast = psr.parse(lxr.scan(s))
		interp.run(ast)
	except AttributeError:
		pass