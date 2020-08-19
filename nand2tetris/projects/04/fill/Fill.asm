// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP)
    // input
    @KBD
    D=M
    @BLACK
    D;JGT
    // white
    @color
    M=0
    @DRAW
    0;JMP
(BLACK)
    @color
    M=-1
(DRAW)
    @y
    M=0
(DRAWLOOP)
    @y
    D=M
    @8192
    D=D-A
    @DRAWEND
    D;JGE

    @y
    D=M
    @SCREEN
    D=A+D
    @address
    M=D-1
    @x
    M=0

(DRAWCOL)
    @x
    D=M
    @32
    D=D-A
    @DRAWCOLEND
    D;JGE

    @address
    M=M+1
    @color
    D=M
    @address
    A=M
    M=D

    @x
    M=M+1
    @DRAWCOL
    0;JMP
(DRAWCOLEND)

    // next Loop
    @32
    D=A
    @y
    M=M+D

    @DRAWLOOP
    0;JMP
(DRAWEND)
    @LOOP
    0;JMP

