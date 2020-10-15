// bootStrap
@256
D=A
@SP
M=D
// call Sys.init 0
@Sys.vm-Sys.init-return-000 // 1
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
(Sys.vm-Sys.init-return-000) // 6
// function Sys.init 0
(Sys.init)
// push constant 6
@6
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// push constant 8
@8
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// call Class1.set 2
@Sys.vm-Class1.set-return-001 // 1
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
@2
D=D+A
@SP
D=M-D
@ARG
M=D
@SP // 4
D=M
@LCL
M=D
@Class1.set // 5
0;JMP
(Sys.vm-Class1.set-return-001) // 6
// pop temp 0 // Dumps the return value
@5
D=A
@0
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push constant 23
@23
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// push constant 15
@15
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// call Class2.set 2
@Sys.vm-Class2.set-return-002 // 1
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
@2
D=D+A
@SP
D=M-D
@ARG
M=D
@SP // 4
D=M
@LCL
M=D
@Class2.set // 5
0;JMP
(Sys.vm-Class2.set-return-002) // 6
// pop temp 0 // Dumps the return value
@5
D=A
@0
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// call Class1.get 0
@Sys.vm-Class1.get-return-003 // 1
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
@Class1.get // 5
0;JMP
(Sys.vm-Class1.get-return-003) // 6
// call Class2.get 0
@Sys.vm-Class2.get-return-004 // 1
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
@Class2.get // 5
0;JMP
(Sys.vm-Class2.get-return-004) // 6
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0;JMP
// function Class1.set 0
(Class1.set)
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
// pop static 0
@SP
A=M-1
D=M
@Class1.vm.static.0
M=D
@SP
M=M-1
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
// pop static 1
@SP
A=M-1
D=M
@Class1.vm.static.1
M=D
@SP
M=M-1
// push constant 0
@0
D=A
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
// function Class1.get 0
(Class1.get)
// push static 0
@Class1.vm.static.0
D=M
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// push static 1
@Class1.vm.static.1
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
// function Class2.set 0
(Class2.set)
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
// pop static 0
@SP
A=M-1
D=M
@Class2.vm.static.0
M=D
@SP
M=M-1
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
// pop static 1
@SP
A=M-1
D=M
@Class2.vm.static.1
M=D
@SP
M=M-1
// push constant 0
@0
D=A
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
// function Class2.get 0
(Class2.get)
// push static 0
@Class2.vm.static.0
D=M
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// push static 1
@Class2.vm.static.1
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
