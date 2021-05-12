import queue
try:
    from nmigen.sim import *
except:
    print("WARNING: failed to load nmigen.sim.*")
try:
    import asyncio
    import cocotb
    from cocotb.triggers import Timer, Edge, First
except:
    print("WARNING: failed to load cocotb stuff")


class uart:
    def __init__(self, rx, tx, brate = 115200, sim='cocotb',  verbose = False):
        self.v = verbose
        self.rx = rx
        self.tx = tx
        self.rxbuf = queue.Queue()
        self.txbuf = queue.Queue()
        self.go_on = True
        self.sim = sim
        if sim == 'nmigen':
            self.step = 1 / brate
        elif sim == 'cocotb':
            t = cocotb.utils.get_time_from_sim_steps(1, 'sec')
            self.cocotb_steps = int((1 / brate) / t)
        if self.v:
            print("uart: verbose mode on")

    def write(self, data):
        self.put(data)

    def read(self, size):
        return self.get(len = size)

    def put(self, data, block = True, verbose = True):
        if self.v & verbose:
            print("uart: added data to queue:", data)
        if isinstance(data, list):
            for i in range(len(data)):
                if self.put(data[i], block, False):
                    return data[i:]
        else:
            try:
                self.txbuf.put(data, block)
            except:
                return data

    def get(self, block = True, len = 1, verbose = True):
        ret = []
        if len == 1:
            try:
                ret = self.rxbuf.get(block)
            except:
                return None
        elif len > 1:
            for _ in range(len):
                add = self.get()
                if add != None:
                    ret.append(add)
        if self.v & verbose:
            print("uart: got data from queue:", ret)
        return ret

    def get_test_processes(self):
        if self.sim == 'nmigen':
            return [self.txp, self.rxp]
        elif self.sim == 'cocotb':
            return [self.txc, self.rxc]

    def kill(self):
        self.go_on = False

    def close(self):
        self.kill()

    def txp(self):
        yield self.tx.eq(1)
        yield Delay(self.step*4)
        while self.go_on:
            d = None
            try:
                d = self.txbuf.get(block = False)
            except:
                pass
            if d != None:
                yield from self._tx(d)
            else:
                yield Delay(self.step)

    async def txc(self):
        if self.v:
            print("uart: cocotb write process started")
        s = self.cocotb_steps
        self.tx <= 1
        await Timer(s*4, 'step')
        while self.go_on:
            d = None
            try:
                d = self.txbuf.get(block = False)
            except:
                pass
                go_on = False
            if d != None:
                self.tx <= 0
                await Timer(s, 'step')
                if self.v:
                    print("sending", d)
                for i in range(8):
                    self.tx <= d % 2
                    d = d >> 1
                    await Timer(s, 'step')
                self.tx <= 1
            await Timer(s, 'step')
        if self.v:
            print("uart: cocotb write process closed")

    async def rxc(self):
        if self.v:
            print("uart: cocotb read process started")
        s = self.cocotb_steps
        while self.go_on:
            d = 0
            while self.rx.value.binstr != "1":
                print("test:", self.rx)
                if self.go_on == False:
                    if self.v:
                        print("uart: cocotb read process closed")
                    return
                await First(Timer(s, 'step'), Edge(self.rx))
            while self.rx.value.binstr != "0":
                if self.go_on == False:
                    if self.v:
                        print("uart: cocotb read process closed")
                    return
                await First(Timer(s, 'step'), Edge(self.rx))
            for i in range(8):
                await Timer(s, 'step')
                d |= (self.rx.value % 2) << i
            await Timer(s, 'step')
            if self.rx.value != 1:
                print("got break")
                while self.rx.value != 1:
                    if self.go_on == False:
                        d = None
                        if self.v:
                            print("uart: cocotb read process closed")
                        return
                    await First(Timer(s, 'step'), Edge(self.rx))

            if self.v:
                print("got", d)
            if d != None:
                self.rxbuf.put(d)
        if self.v:
            print("uart: cocotb read process closed")

    def rxp(self):
        while self.go_on:
            d = (yield from self._rx())
            if d != None:
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
            while (yield self.rx) != 1:
                if self.go_on == False:
                    return
                yield Delay(self.step)
        else:
            yield Delay(self.step)
            return d

