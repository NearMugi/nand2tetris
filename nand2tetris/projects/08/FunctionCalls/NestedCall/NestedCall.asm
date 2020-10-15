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
// push constant 4000	// test THIS and THAT context save
@4000
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// pop pointer 0
@3
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
// push constant 5000
@5000
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// pop pointer 1
@3
D=A
@1
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
// call Sys.main 0
@Sys.vm-Sys.main-return-001 // 1
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
@Sys.main // 5
0;JMP
(Sys.vm-Sys.main-return-001) // 6
// pop temp 1
@5
D=A
@1
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
// label LOOP
(LOOP)
// goto LOOP
@LOOP
0;JMP
// function Sys.main 5
(Sys.main)
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
@SP
A=M
M=0
@SP
M=M+1
// push constant 4001
@4001
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// pop pointer 0
@3
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
// push constant 5001
@5001
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// pop pointer 1
@3
D=A
@1
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
// push constant 200
@200
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// pop local 1
@LCL
D=M
@1
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
// push constant 40
@40
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// pop local 2
@LCL
D=M
@2
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
// push constant 6
@6
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// pop local 3
@LCL
D=M
@3
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
// push constant 123
@123
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// call Sys.add12 1
@Sys.vm-Sys.add12-return-002 // 1
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
@Sys.add12 // 5
0;JMP
(Sys.vm-Sys.add12-return-002) // 6
// pop temp 0
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
// push local 2
@LCL
D=M
@2 // 2
A=D+A
D=M
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// push local 3
@LCL
D=M
@3 // 2
A=D+A
D=M
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// push local 4
@LCL
D=M
@4 // 2
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
// function Sys.add12 0
(Sys.add12)
// push constant 4002
@4002
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// pop pointer 0
@3
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
// push constant 5002
@5002
D=A
@SP // 3
A=M
M=D
@SP // 4
M=M+1
// pop pointer 1
@3
D=A
@1
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
// push constant 12
@12
D=A
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
