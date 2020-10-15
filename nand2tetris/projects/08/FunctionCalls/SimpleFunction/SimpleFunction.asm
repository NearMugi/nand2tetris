// function SimpleFunction.test 2
(SimpleFunction.test)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
// push local 0
@LCL
D=M
@0 // 2
A=D+A
D=M
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// push local 1
@LCL
D=M
@1 // 2
A=D+A
D=M
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// add
@SP // 1
A=M-1
D=M
@R13
M=D
@SP // 2
M=M-1
@SP // 3
A=M-1
D=M
@R13 // 4
D=D+M
@SP // 5
A=M-1
M=D
// not
@SP // 1
A=M-1
M=!M // 2
// push argument 0
@ARG
D=M
@0 // 2
A=D+A
D=M
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// add
@SP // 1
A=M-1
D=M
@R13
M=D
@SP // 2
M=M-1
@SP // 3
A=M-1
D=M
@R13 // 4
D=D+M
@SP // 5
A=M-1
M=D
// push argument 1
@ARG
D=M
@1 // 2
A=D+A
D=M
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// sub
@SP // 1
A=M-1
D=M
@R13
M=D
@SP // 2
M=M-1
@SP // 3
A=M-1
D=M
@R13 // 4
D=D-M
@SP // 5
A=M-1
M=D
// return
@LCL // 1
D=M
@R13
M=D
@R13 // 2
D=M
@5
A=D-A
D=M
@R14
M=D
@SP // 3
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13 // 4
A=M-1
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14 // 5
A=M
0;JMP
