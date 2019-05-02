import ply.lex as lex
import ply.yacc as yacc

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
t_NEG_NUM = r'-\d+'
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
t_STR = r'[a-zA-Z0-9=,!: ]+'

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

# -----------------------LEXER---------------------------
lexer = lex.lex()

data = ''
file_name = ''
while file_name == '':
    file_name = input('Insert file name: ')
f = open(file_name)
data = f.read()
print(data)

# Give the lexer some input
lexer.input(data) 
tokens_list = []

# Tokenize
while True:
	tok = lexer.token()
	if not tok:
		break      # No more input
	tokens_list.append(tok.value)
# print(tokens_list)
# -------------------------------------------------------

#Parsing Part

# adding new thing here
precedence = (
    ('left','PLUS_OP','MINUS_OP'),
    ('left','MUL_OP','DIV_OP', 'MOD_OP'),
    ('left', 'OPAREN', 'CPAREN'),
    ('left', 'NEG_NUM')
    )

def p_statement_expr(t):
    '''
    statement : expression statement
                | empty
    '''
    if t[1] == None:
        t[0] = t[1]
    else:
        t[0] = (t[1], t[2])

def p_expression_declare(t):
    '''
    expression : DECLARE VAR
                | DECLARE ARRAY_expression
    '''
    t[0] = (t[1], t[2])

def p_expression_assign(t):
    '''
    expression : VAR ASSIGN OP_expression
                | ARRAY_expression ASSIGN OP_expression
    '''
    t[0] = (t[2], t[1], t[3])

def p_expression_print(t):
    '''
    expression : PRINT_NUM VALUE_expression empty
               | PRINT_STR STR NL
               | PRINT_STR STR empty
    '''
    if t[3] == None:
        t[0] = (t[1], t[2])
    else :
        t[0] = (t[1], t[2], t[3])

def p_expression_condition(t):
    '''
    expression : IF_expression empty
               | IF_expression ELSE_expression	   
    '''
    if t[2] == None:
        t[0] = t[1]
    else:
        t[0] = (t[1], t[2])

def p_expression_loop(t):
    '''
    expression : LOOP_COND_expression OC_expression
    '''
    t[0] = (t[1], t[2])

def p_expression_if(t):
    '''
    IF_expression : IF CMP_expression OC_expression 
    '''	
    t[0] = (t[1], t[2], t[3])

def p_expression_else(t):
    '''
    ELSE_expression : ELSE OC_expression 
    '''	
    t[0] = (t[1], t[2])

def p_expression_OC(t):
    '''
    OC_expression : OSTATE statement CSTATE
    '''
    t[0] = ('{}', t[2])


def p_expression_loop_condition(t):
    '''
    LOOP_COND_expression : OLOOP LOOP_IN_expression CLOOP
    '''
    t[0] = ('[]', t[2])

def  p_expression_loop_in_condition(t):
    '''
    LOOP_IN_expression : VALUE_expression LOOP_STOP_expression LOOP_STEP_expression
    '''
    t[0] = (t[1], t[2], t[3])

def p_expression_loop_step(t):
    '''
    LOOP_STEP_expression : COLON VALUE_expression
    '''
    t[0] = (':', t[2])

def p_expression_loop_stop(t):
    '''
    LOOP_STOP_expression : COLON VALUE_expression
    '''
    t[0] = (':', t[2])

def p_expression_op(t):
    '''
    OP_expression : OP_expression MUL_OP OP_expression
                | OP_expression DIV_OP OP_expression
                | OP_expression MOD_OP OP_expression
                | OP_expression PLUS_OP OP_expression
                | OP_expression MINUS_OP OP_expression
                | OPAREN OP_expression CPAREN
                | VALUE_expression empty
    '''
    if t[2] == None:
        t[0] = t[1]
    elif t[1] == 'OPAREN' and t[3] == 'CPAREN':
        t[0] = ('()', t[2])
    else:
        t[0] = (t[2], t[1], t[3])

def p_expression_cmp(t):
    '''
    CMP_expression : VALUE_expression EQ VALUE_expression
               | VALUE_expression GT VALUE_expression
               | VALUE_expression LT VALUE_expression
    '''
    t[0] = (t[2], t[1], t[3])

def p_expression_value(t):
    '''
    VALUE_expression : VAR
                    | DEC_NUM
                    | HEX_NUM
                    | ARRAY_expression
                    | NEG_NUM

    '''
    t[0] = t[1]

def p_expression_array(t):
    '''
    ARRAY_expression : VAR ARRAY VAR
                    | VAR ARRAY DEC_NUM 
    '''
    t[0] = (t[2], t[1], t[3])

def p_empty(t):
    '''
    empty :
    '''
    t[0] = None

def p_error(t):
    print("Syntax error at '%s'" % t)

parser = yacc.yacc()

print(parser.parse(data))
