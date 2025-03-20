/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none



module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Internal signals for ALU inputs and outputs
    wire [3:0] alu_a, alu_b;    // 4-bit operands for ALU
    wire [2:0] alu_op;          // 3-bit opcode
    wire [3:0] alu_result;      // 4-bit ALU result
    wire alu_carry_out;         // Carry out from ALU
    wire alu_zero_flag;         // Zero flag from ALU

    // Assign ALU inputs from ui_in and uio_in
    assign alu_a    = ui_in[3:0];       // Lower 4 bits of ui_in as operand A
    assign alu_b    = uio_in[3:0];      // Lower 4 bits of uio_in as operand B
    assign alu_op   = ui_in[6:4];       // Upper 3 bits of ui_in as opcode

    // Instantiate 4-bit ALU
    alu_4bit alu_instance (
        .a(alu_a),
        .b(alu_b),
        .op(alu_op),
        .result(alu_result),
        .carry_out(alu_carry_out),
        .zero_flag(alu_zero_flag)
    );

    // Assign ALU result and status to output
    assign uo_out[3:0] = alu_result;           // Lower 4 bits for ALU result
    assign uo_out[4]   = alu_carry_out;        // Carry out on bit 4
    assign uo_out[5]   = alu_zero_flag;        // Zero flag on bit 5
    assign uo_out[7:6] = 2'b00;                // Unused bits set to 0

    // Unused IO output and enable assignments
    assign uio_out = 0;
    assign uio_oe  = 0;

    // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule

// 4-bit ALU Module
module alu_4bit (
    input wire [3:0] a,    // 4-bit operand A
    input wire [3:0] b,    // 4-bit operand B
    input wire [2:0] op,   // 3-bit opcode
    output reg [3:0] result, // 4-bit result
    output reg carry_out,  // Carry out for ADD/SUB
    output reg zero_flag   // Zero flag
);

    always @(*) begin
        carry_out = 0;
        case (op)
            3'b000: {carry_out, result} = a + b;      // ADD with carry
            3'b001: result = a - b;                   // SUB without carry
            3'b010: result = a & b;                   // AND
            3'b011: result = a | b;                   // OR
            3'b100: result = a ^ b;                   // XOR
            3'b101: result = ~(a ^ b);                // XNOR
            3'b110: result = a << 1;                  // LEFT SHIFT
            3'b111: result = a >> 1;                  // RIGHT SHIFT
            default: result = 4'b0000;                // Default case
        endcase

        // Set zero flag if result is zero
        zero_flag = (result == 4'b0000) ? 1 : 0;
    end
endmodule

