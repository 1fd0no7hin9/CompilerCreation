#found ?
#looking for con_sign(< > =) ex num1 < num2
#found (<) then write 
#   mov ax, num1
#   mov bx, num2
#   cmp ax, bx
#   jge exp1        :--> found(>):jle, found(=):ne
#   ------------
#   if statement zone
#   jmp endExp1
#   ------------
#   exp1:
#   ------------
#   else statement else zone
#   ------------
#   endExp1
if_condition = 0
else_condition = 0
token = ((('?', ('=', 'num1$', 'num2$'), ('{}', ('@', 'num1$'))), ('?>', ('{}', ('@', 'num2$')))))

def define_tokenType(token):
    #to define token's type(if_else, loop, display, assign)
    while(token):
        print(token)
        if(token[0][0] == '?'):
            print("token if_else")
            if_(token[0])
            else_(token[1])
            return
        elif(token[0] == '@'):
            print("assign")
            assign_(token)
            return
        else:
            print("anything else")
            return
            
        token = token[0]

def if_(token):
    global if_condition
    if_condition += 1
    f.write("mov ax, %s\n" %(token[1][1].split('$')[0]))
    f.write("mov ax, %s\n" %(token[1][2].split('$')[0]))
    f.write("cmp ax, bx\n")
    if(token[1][0] == '>'):
        f.write("jle exp%d\n"%(if_condition))
        print("condition jle") 
    elif(token[1][0] == '<'):
        f.write("jge exp%d\n"%(if_condition))
        print("condition jge")
    elif(token[1][0] == '='):
        f.write("jne exp%d\n"%(if_condition))
        print("condition jne")

    #------------------------
    #if statement zone
    define_tokenType(token[2][1])

    f.write("jmp endExp%d\n" %(if_condition))

def else_(token):
    global else_condition
    else_condition += 1
    #------------------------
    #else statement zone
    f.write("exp%d:\n" %(if_condition - else_condition + 1))
    define_tokenType(token[1][1])

    #------------------------
    f.write("endExp%d\n" %(if_condition - else_condition + 1)) 

def assign_(token):
    f.write("%s << 2\n"%(token[1].split('$')[0]))

f= open("text.txt","a")
#condition_exp(token)
#print(type(token))
define_tokenType(token)

