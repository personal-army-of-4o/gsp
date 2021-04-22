from nyanMigen import nyanify


@nyanify()
def loopback():
    rx = Signal()
    tx = rx
