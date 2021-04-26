import cocotb
from uart import uart
from uart_test import uart_test
from cocotb_test import run


@cocotb.test()
async def uart_test0(dut):
    u = uart(rx = dut.tx, tx = dut.rx)

    await run(uart_test, u)
