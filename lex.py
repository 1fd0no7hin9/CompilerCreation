import ply.lex as lex
import ply.yacc as yacc

#List of token names
tokens = (
    'DEC_NUM', 
    'HEX_NUM',
    'VAR',
    'DECLARE',
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
t_STR = r'[a-zA-Z0-9 ]+'

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
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#Parsing Part
global error_occur
error_occur = False
num_lines = 0
# adding new thing here
precedence = (
    ('left','PLUS_OP','MINUS_OP'),
    ('left','MUL_OP','DIV_OP', 'MOD_OP'),
    ('left', 'OPAREN', 'CPAREN')
    )

def p_statement_expr(t):
    '''
    statement : expression statement
                | expression empty
    '''
    if t[2] == None:
        t[0] = t[1]
    else:
        t[0] = (t[1], t[2])

def p_expression_declare(t):
    '''
    expression : DECLARE VAR
                | DECLARE ARRAY_expression
    '''
    t[0] = (t[1], t[2])

def p_expression_declare_error(t):
    '''
    expression : DECLARE error
    '''
    print("Syntax error in declaration at line " + str(t.lineno(2)-num_lines) + ". Bad variable or array name!")

def p_expression_assign(t):
    '''
    expression : VAR ASSIGN OP_expression
                | ARRAY_expression ASSIGN OP_expression
    '''
    t[0] = (t[2], t[1], t[3])

def p_expression_assign_error(t):
    '''
    expression : VAR error OP_expression
                | ARRAY_expression error OP_expression
    '''
    print("Syntax error in assign at line " + str(t.lineno(2)-num_lines) + ". Not assign symbol!")

def p_expression_print(t):
    '''
    expression : PRINT_NUM VALUE_expression empty
               | PRINT_STR STR NL
               | PRINT_STR STR empty
               | PRINT_STR empty NL
    '''
    if t[3] == None:
        t[0] = (t[1], t[2])
    else :
        t[0] = (t[1], t[2], t[3])

def p_expression_print_error(t):
    '''
    expression : PRINT_NUM error empty
               | PRINT_STR error NL
               | PRINT_STR error empty
    '''
    print("Syntax error in printing at line " + str(t.lineno(2)-num_lines) + ". Bad printing value expression!")

def p_expression_condition(t):
    '''
    expression : IF_expression ELSE_expression
                | IF_expression empty
    '''
    if t[2] == None:
        print("Syntax error in if-condition. No else-condition expression!")
        global error_occur 
        error_occur = True
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

def p_expression_if_error(t):
    '''
    IF_expression : error CMP_expression OC_expression 
    '''	
    print("Syntax error in if-condition at line " + str(t.lineno(1)-num_lines) + ". Not if symbol!")

def p_expression_else(t):
    '''
    ELSE_expression : ELSE OC_expression 
    '''	
    t[0] = (t[1], t[2])

def p_expression_else_error(t):
    '''
    ELSE_expression : error OC_expression 
    '''	
    print("Syntax error in else-condition at line " + str(t.lineno(1)-num_lines) + ". Not else symbol!")


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

def p_expression_loop_condition_error(t):
    '''
    LOOP_COND_expression : OLOOP error CLOOP
    '''
    print("Syntax error in loop-condition at line " + str(t.lineno(2)-num_lines) + ". Bad loop condition expression!")

def  p_expression_loop_in_condition(t):
    '''
    LOOP_IN_expression : VALUE_expression LOOP_STOP_expression LOOP_STEP_expression
    '''
    t[0] = (t[1], t[2], t[3])

def p_expression_loop_step(t):
    '''
    LOOP_STEP_expression : COLON VALUE_expression
    '''
    t[0] = t[2]

def p_expression_loop_stop(t):
    '''
    LOOP_STOP_expression : COLON VALUE_expression
    '''
    t[0] = t[2]

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
    elif t[1] == '(' and t[3] == ')':
        t[0] = ('()', t[2])
    else:
        t[0] = (t[2], t[1], t[3])

def p_expression_op_error(t):
    '''
    OP_expression : OP_expression error OP_expression
    '''
    print("Syntax error in operation at line " + str(t.lineno(2)-num_lines) + ". Not operand symbol!")

def p_expression_op_paren_error(t):
    '''
    OP_expression : OPAREN OP_expression empty
    '''
    print("Syntax error in operation at line " + str(t.lineno(1)-num_lines) + ". ')' is missing!")

def p_expression_cmp(t):
    '''
    CMP_expression : OP_expression EQ OP_expression
               | OP_expression GT OP_expression
               | OP_expression LT OP_expression
    '''
    t[0] = (t[2], t[1], t[3])

def p_expression_cmp_error(t):
    '''
    CMP_expression : OP_expression error OP_expression
    '''
    print("Syntax error in if-condition at line " + str(t.lineno(2)-num_lines) + " . Not comparing symbol!")

def p_expression_value(t):
    '''
    VALUE_expression : VAR
                    | DEC_NUM
                    | HEX_NUM
                    | ARRAY_expression
                    | NEG_NUM_expression
    '''
    t[0] = t[1]

def p_expression_array(t):
    '''
    ARRAY_expression : VAR ARRAY VAR
                    | VAR ARRAY DEC_NUM 
    '''
    t[0] = (t[2], t[1], t[3])

def p_expression_neg_num(t):
    '''
    NEG_NUM_expression : MINUS_OP DEC_NUM
    '''
    t[0] = -t[2]

def p_empty(t):
    '''
    empty :
    '''
    t[0] = None

def p_error(t):    
    print("Syntax error:")
    global error_occur 
    error_occur = True

def main():
    lexer = lex.lex()

    # read data
    data = ''
    file_name = ''
    while file_name == '':
        file_name = input('Insert file name: ')
    f = open(file_name)
    data = f.read()
    # print(data)
    f.close()

    # count lines
    f = open(file_name)
    global num_lines
    num_lines = len(f.readlines())-1
    # print(num_lines)
    f.close()

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

    parser = yacc.yacc()
    result = parser.parse(data)
    global error_occur
    if error_occur == True:
        print("Can not generate AST because of error")
        return None
    else:
        return result
