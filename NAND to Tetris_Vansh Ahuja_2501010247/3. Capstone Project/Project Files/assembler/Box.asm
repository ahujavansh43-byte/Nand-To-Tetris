
// CAPSTONE PROJECT - DRAW A BOX
// Starting row: 47
// Height: 20 rows
// Width: 64 pixels = 4 words

(START)
    // Check keyboard
    @KBD
    D=M
    @DRAW
    D;JGT

    @ERASE
    0;JMP

(DRAW)
    @R4
    M=-1
    @FILL
    0;JMP

(ERASE)
    @R4
    M=0

(FILL)
    // SCREEN + (47 * 32) = 17888
    @17888
    D=A
    @R0
    M=D

    // 20 rows
    @20
    D=A
    @R1
    M=D

(ROW)
    // Save current row address
    @R0
    D=M
    @R3
    M=D

    // Four words per row
    @4
    D=A
    @R2
    M=D

(WORD)
    // Write black (-1) or white (0)
    @R4
    D=M
    @R3
    A=M
    M=D

    // Next word
    @R3
    M=M+1

    // Decrease word counter
    @R2
    MD=M-1
    @WORD
    D;JGT

    // Next screen row: +32 words
    @R0
    D=M
    @32
    D=D+A
    @R0
    M=D

    // Decrease row counter
    @R1
    MD=M-1
    @ROW
    D;JGT

    // Check keyboard again
    @START
    0;JMP
