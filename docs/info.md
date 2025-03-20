<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The alu_4bit module performs arithmetic and logical operations on two 4-bit operands (a and b) based on a 3-bit opcode. The operations include addition, subtraction, AND, OR, XOR, XNOR, left shift, and right shift. The result is computed and output along with carry and zero flags.

## How to test

To test the ALU, provide input values to ui_in and uio_in where:

ui_in[3:0] → Operand A

ui_in[6:4] → Opcode

uio_in[3:0] → Operand B

Observe the result on uo_out[3:0] and status flags (uo_out[4] for carry and uo_out[5] for zero).

## External hardware

LEDs
