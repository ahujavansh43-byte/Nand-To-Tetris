// Test labels and variables

@10
D=A

@counter
M=D

(LOOP)
@counter
D=M
@END
D;JEQ

@LOOP
0;JMP

(END)
@END
0;JMP