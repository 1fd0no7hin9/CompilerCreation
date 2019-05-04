.model tiny

.data
;declare var
;num1$ dw ?
;num2$ dw 10h
;declare array
array$ dw 20 DUP (?) 
;msg db 'Hello World$',0 ; print string
;msg2 db 'num1 ',13,10,'$' ; print string with new line	

.code
org 0100h
main:

;assign to var
;mov num1$, 1
;mov num2$, 2h

;assign to array (NOT OKAY!)
;mov ax, num1$
;mov word ptr [array$], 1h
;mov word ptr [array$+ax], 2h
;mov word ptr [array$+2], 3h
;mov dx, word ptr [array$+ax]
;mov ah, 02h
;int 21h

;arithmetic

; plus and minus
;add num1$, 1h ;num1$ += 1 
;sub num1$, 1h ;num1$ -= 1

; mul
;mov dx, 10h ; ax = 1x4
;mov ax, 1h
;imul dx

; div and mod
;mov bl, 3
;mov ax, 10
;idiv bl	   ; al = 3h (quotient), ah = 0h(remainder)

;print array
;mov bx, word ptr [array$+1]
;add bx, 30h
;mov dx, bx
;mov ah, 02h
;int 21h

;print string
;mov ah, 09h
;mov dx, offset msg2
;int 21h

;test balm
;mov ax, 5
;push ax
;mov ax, 3
;push ax
;mov bx, 6
;pop ax
;add ax, bx
;mov ax, ax
;mov bx, ax
;pop ax
;add ax, bx

;print op result plus and minus
;mov ax,num1$
;mov dl,10
;div dl       
;add ax,3030h
;mov dx,ax
;mov ah,02h
;mov dl,dl ; 2nd digit
;int 21h
;mov dl,dh ; 1st digit  
;int 21h

;print op result mul and div
;mov dl,10
;div dl
;add ax,3030h
;mov dx,ax
;mov ah, 02h
;mov dl,dl ; 2nd digit
;int 21h
;mov dl,dh ; 1st digit  
;int 21h

;print for mod op result
;mov bx, 0h
;mov bl, ah
;mov ax,bx
;mov dl,10
;div dl
;add ax, 3030h
;mov dx,ax
;mov ah, 02h
;mov dl,dl ; 2nd digit
;int 21h
;mov dl,dh ; 1st digit  
;int 21h

ret
end main
