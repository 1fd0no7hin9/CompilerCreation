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
#have to use _if1_ as var in asm

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
    f.write("endif_%d\n" %(if_count - else_count + 1)) 

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
    
    try:
        sign.index(token[0])
        if(len(token) == 3):
            print("def")
            print(token)
            ax = expression_(token[1])
            f.write("mov ax, %s\n"%(str(ax)))
            f.write("push ax\n")
            
            bx = expression_(token[2])
            f.write("mov bx, %s\n"%str(bx))
            f.write("pop ax\n")
            if(token[0] == '+' or token[0] == '-'):
                f.write("%s ax, bx\n"%(a[token[0]]))
            else:
                f.write("mov dx, 0\n")
                f.write("%s bx\n"%(a[token[0]]))

        elif(len(token) == 2):
            print("efg")
            ax = expression_(token[1])
            f.write("mov ax, %s\n"%(str(ax)))
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
    
    if(token[0] == '?'):
        print("token if")
        sign = token[0]
        condition_if = token[1]
        statement_if = token[2]
        expression_(condition_if[1])
        if_(sign, statement_if)
        return
    elif(token[0] == '?>'):
        print("token else")
        statement_else = token[1]
        else_(statement_else)
        return
    elif(token[0] == '<<'):
        print("assign")
        
        return
    elif(token[0][0] == '[]'):
        #print("loop")
        #condition = token[0][1]
        #statement = token[1][1]
        #loop_(condition[0], condition[1], condition[2], statement)
        return
    else:
        print("anything else")
        
        return


f= open("text.txt","a")

test_token = input("insert token : ")
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
    print(token)
    define_tokenType(token)
#f.close()
