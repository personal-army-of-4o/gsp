import cocotb


def ahbuart_test(u):
    print("writing")
    u.write(0x80000004, [0xFFFFFFFF, 0])
    print("reading")
    d = u.read(0x80000000, 2)
    print(d)
    if d != [511, 1023]:
        cocotb.fail(msg = "mismatch")
    print("killing")
    u.kill()  

