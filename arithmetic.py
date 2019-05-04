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
        print(token)
        try:
            #print("token[0] ", token[0])
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

a= input("insert token : ")

f = open("test.txt","a")

token = manageToken(a)
print("equation ", token[1][2])
expression_(token[1][2])
f.close()
