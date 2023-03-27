.686
.model flat
public _function

.data


.code
_function PROC
	push ebp
	mov ebp, esp
	push ebx

	mov eax, [ebp + 8]
	mov ebx, [ebp + 12]
	mov ecx, [ebp + 16]

	mul ebx
	add eax, ecx

	pop ebx
	pop ebp
	ret
_function ENDP
END