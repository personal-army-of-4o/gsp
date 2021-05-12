import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import FallingEdge
from cocotb.triggers import RisingEdge
from cocotb.triggers import ClockCycles
from cocotb.result import TestFailure
from uart import uart
from ahbuart_test import ahbuart_test
from cocotb_test import run
from cocotb_test import p as ptc
from ahbuart import ahbuart


@cocotb.test()
async def uart_test0(dut):
    u = uart(rx = dut.oRs_dbg, tx = dut.iRs_dbg, verbose = False)
    u = ahbuart(u)
    cocotb.fork(Clock(dut.iClk, 20, 'ns').start())
    dut.iGpio <= 0x1FF
    dut.iReset <= 0
    await Timer(10000, 'ns')
    dut.iReset <= 1
    await Timer(285000, 'ns')
    await run(ahbuart_test, u)
