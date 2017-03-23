#include <p16f917.inc>

#define SW2     PORTA,0
#define LED     PORTD,7

    ORG     0x00
    GOTO    INITIALIZATION
    ORG     0X05
INITIALIZATION
    ; Select bank1
    BSF     STATUS,RP0
    BCF     STATUS,RP1
    ; Configure pin RA0 as input and digital
    BSF     TRISA,0     ; make RA0 an input
    BCF     ANSEL,0     ; make RA0 a digital pin
    ; Configure pm RD7 aas output and digital
    BCF     TRISD,7     ; make RD7 an output

    ; Select bank 0
    BCF     STATUS,RP0

    ; Set LED off
    BCF     LED

MAIN_LOOP
    BTFSC   SW2
    GOTO    MAIN_LOOP
    MOVLW   0X80        ; toggle bit 7 of port D
    XORWF   PORTD,F
    GOTO    MAIN_LOOP
    END
