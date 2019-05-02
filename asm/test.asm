.model tiny
.data
msg db 'Hello, world!$',0
.code
org 0100h

main:

mov ax, 3
mov bx, 2

cmp ax, bx	;condition if >
jl exp1		;
mov ah, 02h	;-----------
mov dl, '1'	;expression if
int 21h		;----------
jmp endexp1	;

exp1:		;condition else
mov ah, 02h	;----------
mov dl, '2'	;expression else
int 21h		;----------

endexp1:

ret
end main
