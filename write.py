#found ?
#looking for con_sign(< > =) ex num1 < num2
#found (<) then write 
#   mov ax, num1
#   mov bx, num2
#   cmp ax, bx
#   jge else_1        :--> found(>):jle, found(=):ne
#   ------------
#   if statement zone
#   jmp endif_1
#   ------------
#   else_:
#   ------------
#   else statement else zone
#   ------------
#   endif_1

#have to use _if1_ as var in asm
#have to use _if2_ as var in asm

if_count = 0
else_count = 0

def if_(sign, statement_token):
    global if_count
    if_count += 1

    f.write("mov ax, _if1_\n")
    f.write("mov bx, _if2_\n")
    f.write("cmp ax, bx\n")
    if(sign == '>'):
        f.write("jle else_%d\n"%(if_count))
        print("condition jle") 
    elif(sign == '<'):
        f.write("jge else_%d\n"%(if_count))
        print("condition jge")
    elif(sign == '='):
        f.write("jne else_%d\n"%(if_count))
        print("condition jne")

    #------------------------
    #if statement zone
    define_tokenType(statement_token)

    f.write("jmp endif_%d\n" %(if_count))

def else_(statement_token):
    global else_count
    else_count += 1
    #------------------------
    #else statement zone
    f.write("else_%d:\n" %(if_count - else_count + 1))
    define_tokenType(statement_token)

    #------------------------
    f.write("endif_%d:\n" %(if_count - else_count + 1)) 

#found []
#
#   mov ax, stop       *push var to register
#   mov bx, step        * ax : final
#   mov cx, begin       * bx : step
#   loop1:              * cx : begin
#   cmp cx, ax          *--------------
#   jge endLoop1        *condition loop
#   ;----------
#   ;statement loop
#   push ax             *-------------
#   push bx             collect loop count for one Loop
#   push cx             *-------------
#   mov ah, 02h         *
#   mov dl, '5'         *loop statement (maybe loop, if_else, assign, ... )
#   int 21h             *
#   pop cx              *------------
#   pop bx              assign loopcount for check
#   pop ax              *------------
#   ;----------
#   add cx, bx          step loop
#   jmp loop1
#   endLoop1:

loop_count = 0
endLoop_count = 0
def loop_(begin, stop, step, statement_token):
    global loop_count
    global endLoop_count
    loop_count += 1
    f.write("mov ax, %s\n"%(begin))
    f.write("mov bx, %s\n"%(step))
    f.write("mov cx, %s\n"%(stop))
    f.write("loop%s:\n"%(loop_count))
    f.write("cmp cx, ax\n")
    f.write("jge endLoop%s\n"%(loop_count))
    f.write("push ax\npush bx\npush cx\n")
    
    define_tokenType(statement_token)

    endLoop_count += 1
    f.write("pop cx\npop bx\npop ax\n")
    f.write("add cx, bx\n")
    f.write("jmp loop%s\n"%(loop_count - endLoop_count + 1))
    f.write("endLoop%s:\n"%(loop_count - endLoop_count + 1))

#add
#mov ax, num1   ;ax = num1
#mov bx, num2   ;bx = num2
#add ax, bx     ;ax = ax + bx

#sub
#mov ax, num1   ;ax = num1
#mov bx, num2   ;bx = num2
#sub ax, bx     ;ax = ax - bx

#mul
#mov ax, num1   ;ax = num1
#mov bx, num2   ;bx = num2
#mul bx         ;ax = ax * bx

#div
#mov dx, 0      
#mov ax, num1   
#mov bx, num2
#div bx         ;ax = ax/bx + dx

def expression_(token):
    a = {'+':'add', '-':'sub', '*':'mul', '/':'div', '%':'div'}
    sign = ['()', '+', '-', '*', '/', '%']
    print("expression  come !") 
    try:
        sign.index(token[0])
        if(len(token) == 3):
            print("def")
            print(token)
            ax = expression_(token[1])
            f.write("mov ax, %s\n"%(define_var(ax)))
            f.write("push ax\n")
            
            bx = expression_(token[2])
            f.write("mov bx, %s\n"%(define_var(bx)))
            f.write("pop ax\n")
            if(token[0] == '+' or token[0] == '-'):
                f.write("%s ax, bx\n"%(a[token[0]]))
            else:
                f.write("mov dx, 0\n")
                f.write("%s bx\n"%(a[token[0]]))

        elif(len(token) == 2):
            print("efg")
            ax = expression_(token[1])
            f.write("mov ax, %s\n"%(define_var(ax)))
            #f.write("push ax\n")
        if(token[0] == '%'):
            return 'dx'
        else:    
            return 'ax'
    except Exception as e:
        print(e)
        #print('e' ,token)
        return token
        

def manageToken(token):
    a=[]
    sign_token = ['?','?>','[]','{}','@','<<','&','>>','#']
    while(token):
        try:
#            print("token[0] ", token[0])
            a.append(token[0])
            token = token[1]
            if(token[1]==None):
                a.append(token[0])
                break
            elif(sign_token.index(token[0])):
                a.append(token)
                break
        except Exception as e:
            print('')
            
    return tuple(a)

def define_tokenType(token):
    #to define token's type(if_else, loop, display, assign)
    print(token)
    if(token[0][0] == '?'):
        print("token if_else")
        
        condition_if = token[0][1]
        sign = condition_if[0][0]
        statement_if = token[0][2][1] 
        
        if(type(condition_if[1]).__name__ == 'tuple' and condition_if[1][0] != '#'):
            print("condition[1] ",condition_if[1])
            expression_(condition_if[1])
            f.write("mov _if1_, ax\n")
        else:
            f.write("mov ax, %s\n"%(define_var(condition_if[1])))
            f.write("mov _if1_, ax\n")

        if(type(condition_if[2]).__name__ == 'tuple' and condition_if[2][0] != '#'):
            expression_(condition_if[2])
            f.write("mov _if2_, ax\n")
        else:
            f.write("mov ax, %s\n"%(define_var(condition_if[2])))
            f.write("mov _if2_, ax\n")
        
        if_(sign, statement_if)
        
        print("token else")
        statement_else = token[1][1][1]
        else_(statement_else)

        return
    
    elif(token[0][0] == '[]'):
        print("loop")
        condition = token[0][1]
        statement = token[1][1]
        loop_(define_var(condition[0]), define_var(condition[1]), define_var(condition[2]), statement)
        return
    
    elif(token[0] == '<<'):
        # ('<<', var, var)
        print("assign") 
        var_1 = define_var(token[1])
        var_2 = define_var(token[2])
        f.write("mov %s, %s\n"%(var_1, var_2))
        return
    
    elif(token[0] == '@'):
        print("print  number")
        return
    
    elif(token[0] == '>>'):
        print("print str")
        return
    
    elif(token[0] == '&'):
        print("declare var")
        return
    else:
        print("anything else")
        
        return

def define_var(token):
    #('#', 'array$', 'index$')
    #'var'
    a=''
    if(type(token).__name__ == 'tuple' and token[0] == '#'):
        f.write('mov di, %s\n'%(token[2]))
        a='['+str(token[1])+' + di'+']'
        return a
    elif(type(token).__name__ == 'tuple'):
        expression_(token)
        return 'ax'
    else:
        return str(token)

f= open("text.txt","a")

test_token = input("insert token : ")
#array_(test_token)

#token = ('+', 3, ('*', ('()', ('+', 1, 1)), 2))
#token = ('+', ('+', 3, 1), ('*', 1, 2))
#token = ('+', ('+', 3, 1), ('()', ('*', 1, 2)))
#expression_(test_token)

#a = manageToken(test_token)
#print(a)
#print("==========================================================================")
#for i in a :
#    print(i)

#main:
for token in manageToken(test_token):
    #print(token)
    define_tokenType(token)
f.close()
