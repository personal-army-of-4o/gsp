import queue
from nmigen.sim import *


class uart:
    def __init__(self, rx, tx, brate = 115200):
        self.rx = rx
        self.tx = tx
        self.rxbuf = queue.Queue()
        self.txbuf = queue.Queue()
        self.go_on = True
        self.step = 1 / brate

    def put(self, data, block = True):
        if isinstance(data, list):
            for i in range(data):
                if self.put(data[i], block):
                    return data[i:]
        else:
            try:
                self.txbuf.put(data, block)
            except:
                return data

    def get(self, block = True, len = 1):
        if len == 1:
            try:
                return self.rxbuf.get(block)
            except:
                return None
        elif len > 1:
            ret = []
            for _ in range(len):
                add = self.get()
                if add:
                    ret.append(add)
            return ret

    def get_test_processes(self):
        return [self.txp, self.rxp]

    def kill(self):
        self.go_on = False

    def txp(self):
        yield self.tx.eq(1)
        yield Delay(self.step*4)
        while self.go_on:
            print("txp")
            d = None
            try:
                d = self.txbuf.get(block = False)
            except:
                pass
            if d != None:
                yield from self._tx(d)
            else:
                yield Delay(self.step)
        print("txp done")

    def rxp(self):
        while self.go_on:
            print("rxp")
            d = (yield from self._rx())
            self.rxbuf.put(d)
        print("rxp done")

    def _tx(self, d):
        yield self.tx.eq(0)
        yield Delay(self.step)
        for i in range(8):
            yield self.tx.eq(d % 2)
            d = d >> 1
            yield Delay(self.step)
        yield self.tx.eq(1)
        yield Delay(self.step)

    def _rx(self):
        d = 0
        while (yield self.rx) != 1:
            if self.go_on == False:
                return
            yield Delay(self.step)
        while (yield self.rx) == 1:
            if self.go_on == False:
                return
            yield Delay(self.step)
        for i in range(8):
            yield Delay(self.step)
            d |= ((yield self.rx) % 2) << i
        yield Delay(self.step)
        if (yield self.rx) != 1:
            print("got break")
            while (yield self.rx) != 1:
                if self.go_on == False:
                    return
                print("waiting for 1", (yield self.rx), "step", self.step)
                yield Delay(self.step)
        else:
            yield Delay(self.step)
            return d

