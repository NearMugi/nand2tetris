// bootStrap
@256
D=A
@SP
M=D
// call Sys.init 0
@Sys.init-ret // 1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL // 2
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5 // 3
D=A
@0
D=D+A
@SP
D=M-D
@ARG
M=D
@SP // 4
D=M
@LCL
M=D
@Sys.init // 5
0;JMP
(Sys.init-ret) // 6
// function Sys.init 0
(Sys.init)
// push constant 4
@4
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// call Main.fibonacci 1   // computes the 4'th fibonacci element
@Main.fibonacci-ret // 1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL // 2
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5 // 3
D=A
@1
D=D+A
@SP
D=M-D
@ARG
M=D
@SP // 4
D=M
@LCL
M=D
@Main.fibonacci // 5
0;JMP
(Main.fibonacci-ret) // 6
// label WHILE
(WHILE)
// goto WHILE              // loops infinitely
@WHILE
0;JMP
// function Main.fibonacci 0
(Main.fibonacci)
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
// push constant 2
@2
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// lt                     // checks if n<2
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
@R13 // 4-1
D=D-M
@BUNKI_TRUE_000 // 4-2
D;JLT
@SP // 4-3-False
A=M-1
M=0
@BUNKI_END_000
0;JMP
(BUNKI_TRUE_000) // 4-3-True
@SP
A=M-1
M=-1
(BUNKI_END_000)
// if-goto IF_TRUE
@SP
AM=M-1
D=M
@IF_TRUE
D;JNE
// goto IF_FALSE
@IF_FALSE
0;JMP
// label IF_TRUE          // if n<2, return n
(IF_TRUE)
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
// label IF_FALSE         // if n>=2, returns fib(n-2)+fib(n-1)
(IF_FALSE)
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
// push constant 2
@2
D=A
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
// call Main.fibonacci 1  // computes fib(n-2)
@Main.fibonacci-ret // 1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL // 2
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5 // 3
D=A
@1
D=D+A
@SP
D=M-D
@ARG
M=D
@SP // 4
D=M
@LCL
M=D
@Main.fibonacci // 5
0;JMP
(Main.fibonacci-ret) // 6
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
// push constant 1
@1
D=A
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
// call Main.fibonacci 1  // computes fib(n-1)
@Main.fibonacci-ret // 1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL // 2
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5 // 3
D=A
@1
D=D+A
@SP
D=M-D
@ARG
M=D
@SP // 4
D=M
@LCL
M=D
@Main.fibonacci // 5
0;JMP
(Main.fibonacci-ret) // 6
// add                    // returns fib(n-1) + fib(n-2)
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
