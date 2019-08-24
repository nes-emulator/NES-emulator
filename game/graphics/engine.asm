

   ; Graphics engine variable
   .enum $0700
   x_position       .dsb 1
   y_position       .dsb 1
   mirroring        .dsb 1
   initial_sprite   .dsb 1
   .ende

;----------------
; Receives bomberman position as logical x_position and y_postion
; Moves all his sprites to screen position
;----------------
MoveBomberman:
    PHA
    TYA
    PHA
    TXA
    PHA                 ; Push all registers to stack

    LDA x_position
    ASL A
    ASL A
    ASL A
    ASL A               ; Multiply x position by 16

    CLC
    ADC #$10            ; Add x constant left space to complement
    STA x_position      ; Save new value in same variable

    LDA y_position
    ASL A
    ASL A
    ASL A
    ASL A               ; Multiply y position by 16

    CLC
    ADC #$30            ; Add y constant top space to complement
    STA y_position      ; Save new value in same variable

ManageMoveBomberSprites:
    LDX #$00            ; Load sprite start position

    LDA y_position      ; Write first y position
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextSprite
    LDA x_position      ; Write first x position
    STA FIRST_SPRITE_Y, x

    INX                 ; Go to next sprite of bomberman
    LDA y_position      ; Write second y position
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextSprite
    LDA x_position
    CLC
    ADC #$08            ; Write second x, 8 bits ahead
    STA FIRST_SPRITE_Y, x

    INX                 ; Go to next sprite of bomberman
    LDA y_position
    CLC
    ADC #$08            ; Write third y, 8 bits ahead
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextSprite
    LDA x_position      ; Write third x
    STA FIRST_SPRITE_Y, x

    INX                 ; Go to next sprite of bomberman
    LDA y_position
    CLC
    ADC #$08            ; Write fourth y, 8 bits ahead
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextSprite
    LDA x_position
    CLC
    ADC #$08            ; Write fourth x, 8 bits ahead
    STA FIRST_SPRITE_Y, x

    PLA
    TAY
    PLA
    PXA
    PLA                 ; Pull all registers from stack

    RTS

MoveXRegisterNextSprite:
    INX                 ; Moves x to last part of sprite
    INX
    INX
    RTS


;----------------
; Receives bomberman direction as Register X
; Rotate his sprites to better fit screen
;----------------
MoveBombermanDirection:
    CPX #01            ; Logic for decide which sprite to go for
    BEQ BombermanFacingUp

    CPX #02
    BEQ BombermanFacingDown

    CPX #03
    BEQ BombermanFacingLeft

    CPX #04
    BEQ BombermanFacingRight
    JMP MoveBombermanDirectionEnd

BombermanFacingLeft:
BombermanFacingRight:
    JMP MoveBombermanDirectionEnd

BombermanFacingUp:
    LDA #$0c                ; Start of bomber facing up sprite
    JMP MoveBombermanDirectionLoadSprite

BombermanFacingDown:
    LDA #$06                ; Start of bomber facing down sprite
    JMP MoveBombermanDirectionLoadSprite

MoveBombermanDirectionLoadSprite:
    STA initial_sprite      ; Nex sprite

    LDX #$01                ; Write on first tile number
    STA FIRST_SPRITE_Y, x

    INC initial_sprite      ; Go to next sprite
    LDA initial_sprite

    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x   ; Write second tile number

    CLC
    ADC #$09                ; Get down part of bomberman
    STA initial_sprite

    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x   ; Write third tile number

    INC initial_sprite      ; Go to next sprite
    LDA initial_sprite

    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x   ; Write fourth tile number

MoveBombermanDirectionEnd:
    RTS

MoveXRegisterNextLine:
    INX             ; Sum four
    INX
    INX
    INX
    RTS