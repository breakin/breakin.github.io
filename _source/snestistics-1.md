---
layout: post
date: 2013-05-18
title: Snestistics - First published code!
tags: snes, programming, asm, snestistics
theme: snestistics
landing: index, snestistics
---
I've finally put some code up on the net!

First I have a modified snes9x branch at https://github.com/breakin/snes9x-debugtrace.
It is currently a trap since it is just a clean copy of snes9x, without my actual modifications added yet. It should output .snestrace-files and it will soon. But not yet.

Then I have create the fantastic tool snestistics. It can be found at [https://github.com/breakin/snestistics](https://github.com/breakin/snestistics).

It should work with a variety of snes-roms, but it has only been tested with Zelda 3 NTSC. Visual Studio 2012 projects files are included. It has only been tested with that compiler.

There is one example included with preliminary label definitions and a .snestrace-file that I created by playing through small parts of Zelda 3. By running snestistics an assmebler file of 19000 lines is created. It can be cleanly compiled using WLA DX and it patches on top of the original ROM-file without creating any differences.

Going forward I will most likely extend the list of known labels in Zelda 3 and try to understand more of it. That was my original goal, right?

Lastly and last, here is a small snippet from the asm-file that is outputted just to show the power of it all. Notice that even though the jumps are not deterministic (for various reasons, in this snippet it is always because the databank could be different from the program bank and that there could be a jump straight into this code) the correct taken labels are printed in the comment. If multiple targets exists, there will be multiple labels in the comment! Next step is to figure out what label_00D537 does and give it a proper name!

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.BANK $00 SLOT 0
.ORG $D231-$8000
.SECTION SnestisticsSection10 OVERWRITE

; Things under investigation
load_stuff_1:

    PHB 
    PHK 
    PLB 
    REP #$20
    STZ $0A
    STZ $0C
    LDA #$0480.W
    STA $06
    SEP #$20
    LDA #$07.B
    JSR $D537.W ; label_00D537 [00D537]
    LDA #$07.B
    JSR $D537.W ; label_00D537 [00D537]
    LDA #$03.B
    JSR $D537.W ; label_00D537 [00D537]
    LDY #$5F.B
    LDA #$04.B
    JSR $D54E.W ; decompress_and_unpack_image_tableA [00D54E]
    LDA #$03.B
    JSR $D553.W ; unpack_image_source7f4000 [00D553]
    LDA #$01.B
    JSR $D553.W ; unpack_image_source7f4000 [00D553]
    LDA #$04.B
    JSR $D537.W ; label_00D537 [00D537]
    LDY #$60.B
    LDA #$0E.B
    JSR $D54E.W ; decompress_and_unpack_image_tableA [00D54E]
    LDA #$07.B
    JSR $D553.W ; unpack_image_source7f4000 [00D553]
    LDY #$5F.B
    LDA #$02.B
    JSR $D54E.W ; decompress_and_unpack_image_tableA [00D54E]
    LDY #$54.B
    JSR $E766.W ; decompress_tableA_dest7f4000_indexY [00E766]
    REP #$30
    LDA $00
    LDX #$1480.W
    PHA 
    LDY #$0008.W
    JSR $D61C.W ; unpack_image_inner [00D61C]
    PLA 
    CLC 
    ADC #$0180.W
    LDY #$0008.W
    JSR $D61C.W ; unpack_image_inner [00D61C]
    SEP #$30
    LDY #$60.B
    JSR $E766.W ; decompress_tableA_dest7f4000_indexY [00E766]
    REP #$30
    LDA $00
    LDX #$2280.W
    LDY #$0003.W
    PHA 
    JSR $D61C.W ; unpack_image_inner [00D61C]
    PLA 
    CLC 
    ADC #$0180.W
    LDY #$0003.W
    JSR $D61C.W ; unpack_image_inner [00D61C]
    SEP #$30
    JSR $D3C6.W ; label_00D3C6 [00D3C6]
    PLB
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~