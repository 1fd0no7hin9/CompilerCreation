import ply.lex as lex

#List of token names
tokens = (
	'DEC_NUM', 
	'HEX_NUM',
	'VAR',
	'DECLARE',
	'NEG_NUM', 
	'MUL_OP', 
	'DIV_OP', 
	'MOD_OP',
	'PLUS_OP', 
	'MINUS_OP',
	'OPAREN', 
	'CPAREN',
	'ARRAY',
	'ASSIGN',
	'PRINT_NUM',
	'PRINT_STR',
	'NL',
	'IF',
	'ELSE',
	'EQ',
	'GT',
	'LT',
	'OSTATE',
	'CSTATE',
	'OLOOP', 
	'COLON', 
	'CLOOP',
	'STR'
)

#Regular expression rules
t_VAR = r'[a-zA-Z][a-zA-Z0-9]*\$'
t_DECLARE = r'&'
t_NEG_NUM = r'^-\d+'
t_MUL_OP = r'\*'
t_DIV_OP = r'/'
t_MOD_OP = r'%'
t_PLUS_OP = r'\+'
t_MINUS_OP = r'-'
t_OPAREN = r'\('
t_CPAREN = r'\)'
t_ARRAY = r'\#'
t_ASSIGN = r'<<'
t_PRINT_NUM = r'@'
t_PRINT_STR = r'>>'
t_NL = r':NL'
t_IF = r'\?'
t_ELSE = r'\?>'
t_EQ = r'='
t_GT = r'>'
t_LT = r'<'
t_OSTATE = r'\{'
t_CSTATE = r'\}'
t_OLOOP = r'\['
t_COLON = r':'
t_CLOOP = r'\]'
t_STR = r'[a-zA-Z0-9_ ]+'

def t_DEC_NUM(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_HEX_NUM(t):
	r'0[xX][0-9a-fA-F]+'
	t.value = int(t.value,16)
	return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()

data = '''
&array$#20

array$#0 << 32
array$#1 << 30
array$#2 << 0
array$#3 << 1
array$#4 << 9
array$#5 << 20
array$#6 << 32
array$#7 << 32
array$#8 << 32
array$#9 << 32
array$#10 << 32
array$#11 << 32
array$#12 << 32
array$#13 << 32
array$#14 << 32
array$#15 << 32
array$#16 << 32
array$#17 << 32
array$#18 << 32
array$#19 << 32

&index$ << 1
&min$ << array$#0

[index$:19:1]{
	?min$ > array$#index${
		min$ << array$#index$
	}
}

>> min_number:
@min$
'''
 
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
	tok = lexer.token()
	if not tok: 
		break      # No more input
	print(tok)
