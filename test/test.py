# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut._log.info("Test project behavior")

    # ===========================
    # Test Case 1: ADD (5 + 3)
    # ===========================
    dut.ui_in.value = 0b0000_0000 | (0b000 << 4) | 5  # Opcode = 000 (ADD), a = 5
    dut.uio_in.value = 3  # b = 3
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 8, f"ADD failed! Expected 8, got {int(dut.uo_out.value)}"

    # ===========================
    # Test Case 2: SUB (7 - 2)
    # ===========================
    dut.ui_in.value = 0b0000_0000 | (0b001 << 4) | 7  # Opcode = 001 (SUB), a = 7
    dut.uio_in.value = 2  # b = 2
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 5, f"SUB failed! Expected 5, got {int(dut.uo_out.value)}"

    # ===========================
    # Test Case 3: AND (5 & 3)
    # ===========================
    dut.ui_in.value = 0b0000_0000 | (0b010 << 4) | 5  # Opcode = 010 (AND), a = 5
    dut.uio_in.value = 3  # b = 3
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 1, f"AND failed! Expected 1, got {int(dut.uo_out.value)}"

    # ===========================
    # Test Case 4: OR (5 | 3)
    # ===========================
    dut.ui_in.value = 0b0000_0000 | (0b011 << 4) | 5  # Opcode = 011 (OR), a = 5
    dut.uio_in.value = 3  # b = 3
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 7, f"OR failed! Expected 7, got {int(dut.uo_out.value)}"

    # ===========================
    # Test Case 5: XOR (5 ^ 3)
    # ===========================
    dut.ui_in.value = 0b0000_0000 | (0b100 << 4) | 5  # Opcode = 100 (XOR), a = 5
    dut.uio_in.value = 3  # b = 3
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 6, f"XOR failed! Expected 6, got {int(dut.uo_out.value)}"

    # ===========================
    # Test Case 6: XNOR ~(5 ^ 3)
    # ===========================
    dut.ui_in.value = 0b0000_0000 | (0b101 << 4) | 5  # Opcode = 101 (XNOR), a = 5
    dut.uio_in.value = 3  # b = 3
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 9, f"XNOR failed! Expected 9, got {int(dut.uo_out.value)}"

    # ===========================
    # Test Case 7: LEFT SHIFT (5 << 1)
    # ===========================
    dut.ui_in.value = 0b0000_0000 | (0b110 << 4) | 5  # Opcode = 110 (LEFT SHIFT), a = 5
    dut.uio_in.value = 0  # b not used
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 10, f"LEFT SHIFT failed! Expected 10, got {int(dut.uo_out.value)}"

    # ===========================
    # Test Case 8: RIGHT SHIFT (5 >> 1)
    # ===========================
    dut.ui_in.value = 0b0000_0000 | (0b111 << 4) | 5  # Opcode = 111 (RIGHT SHIFT), a = 5
    dut.uio_in.value = 0  # b not used
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 2, f"RIGHT SHIFT failed! Expected 2, got {int(dut.uo_out.value)}"

    # ===========================
    # Final message and test end
    # ===========================
    dut._log.info("All test cases passed!")
