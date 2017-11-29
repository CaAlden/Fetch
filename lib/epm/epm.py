'''
Driver for the Electro Permanent Magnet (EPM)
'''
from ..utils.gpio import GPIOController, PIN_OUT

class EPMController():

    def __init__(self, addr0Pin, addr1Pin, valPin):
        pinMapping = [(addr0Pin, PIN_OUT),
                      (addr1Pin, PIN_OUT),
                      (valPin, PIN_OUT)]
        self._addr0 = addr0Pin
        self._addr1 = addr1Pin
        self._val = valPin
        self._gpio = GPIOController(pinMapping)


    def setMagnetState(self, addr, state):
        ''' Set the magnet at the given address to the given state.'''
        assert addr >= 0 and addr <= 3, "Invalid address {}".format(addr)
        assert state == 0 or state == 1, "State should be 1 or 0"

        if addr & 0b01:
            self._gpio[self._addr0].set()
        else:
            self._gpio[self._addr0].clear()

        if addr & 0b10:
            self._gpio[self._addr1].set()
        else:
            self._gpio[self._addr1].clear()

        if state:
            self._gpio.pins[self._val].set()
        else:
            self._gpio.pins[self._val].clear()
