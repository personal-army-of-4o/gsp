from threading import Thread
from nmigen.sim import *
from nMigen_test import mytest, runtests, helper as h, uut_iface
from loopback import loopback
from uart import uart

DEBUG = 1 == 1
VERBOSE = DEBUG

class helper(h):
    def __init__(self):
        self.uut = uut = loopback()
        self.uart = uart(rx = uut.tx, tx = uut.rx)
        super().__init__()

pcs = []

@mytest
class t0(helper):
    def get_test_processes(self):
        uut = self.uut
        uart = self.uart
        def test():
            d = uart.put(0x55)
            d = uart.get()
            print(d)
            uart.kill()
            print("thread done")
        pcs.append(Thread(target = test))
        pcs[0].start()
        return [self.uut, [*uart.get_test_processes()]]

if __name__ == "__main__":
    print("running tests")
    runtests(debug = DEBUG)
    pcs[0].join()
    print("done")
