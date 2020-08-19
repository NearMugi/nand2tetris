// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
    @cnt
    M=0
    @mult
    M=0
(LOOP)
    @cnt
    D=M
    @R1
    D=D-M
    @SET
    D;JGE

    @R0
    D=M
    @mult
    M=M+D
    @cnt
    M=M+1
    @LOOP
    0;JMP

(SET)
    @mult
    D=M
    @R2
    M=D
(END)
    @END
    0;JMP