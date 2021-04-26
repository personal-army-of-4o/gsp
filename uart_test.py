class uart_test:
    def __init__(self, uart):
        self.uart = uart

    def test(self):
        u = self.uart
        u.put(0x55)
        d = u.get()
        if d != 0x55:
            print(d)
        else:
            print("ok")
        u.kill()  

