import math


class ahbuart:
    def __init__(
        self, 
        serial
    ):
        self.serial = serial
        self.serial.write([0x55])

    def get_test_processes(self):
        return  self.serial.get_test_processes()

    def kill(self):
        try:
            self.serial.kill()
        except:
            pass

    def write(self, addr: int, data: list) -> None:
        if len(data) > 64:
            self.write(addr, data[:64])
            self.write(addr + 256, data[64:])
        else:
            l = len(data)
            msg = [ 0xC0 | (l - 1), *self._words_to_bytes(addr), *self._words_to_bytes(data)]
            self.serial.write(msg)


    def read(self, addr: int, words_number: int = 1, return_array = False):
        if words_number > 64:
            return [*self.read(addr, 64), *self.read(addr, words_number - 64, return_array = True)]
        else:
            self.serial.write([ 0x80 | (words_number - 1), *self._words_to_bytes(addr)])
            ret = self._build_words(self.serial.read(size = words_number *  4))
            if (words_number == 1) and (return_array == False):
                return ret[0]
            return ret

    def _build_words(self, input_bytes):
        if len(input_bytes) > 4:
            return [*self._build_words(input_bytes[:4]), *self._build_words(input_bytes[4:])]
        else:
            ret = 0
            for i in range(len(input_bytes)):
                ret += input_bytes[i] << (len(input_bytes)-1-i) * 8
            return [ret]

    def _words_to_bytes(self, words):
        ret = []
        if not isinstance(words, list):
            words = [words]
        for word in words:
            ret.extend([
                ((word & 0xFF000000) >> 24),
                ((word & 0x00FF0000) >> 16),
                ((word & 0x0000FF00) >> 8),
                (word & 0x000000FF)
            ])
        return ret    

    def __del__(self):
        self.close()

    def close(self) -> None:
        self.serial.close()
