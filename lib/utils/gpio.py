'''
Generic GPIO drivers for the Raspberry Pi
'''
try:
    import RPi.GPIO as gpio
except ImportError as ie:
    print("Could not import RPi GPIO... Quitting")
    import sys
    sys.exit(1)


gpio.setmode(gpio.BOARD)
PIN_IN = gpio.IN
PIN_OUT = gpio.OUT

class GPIOController():

    def __init__(self, pinBindings):
        self.pins = {}
        for pinNumber, pinMode in pinBindings:
            self.pins[pinNumber] = GPIO(pinNumber, pinMode)

class GPIO():

    def __init__(self, pinNum, pinMode):
        self._pinHandle = None
        self._pinNum = pinNum
        self._pinMode = pinMode
        gpio.setup(pinNum, pinMode)

    def set(self, mode=gpio.HIGH):
        ''' Set this GPIO HIGH'''
        gpio.output(self._pinNum, mode)

    def clear(self):
        ''' Set this GPIO low'''
        self.set(mode=gpio.LOW)

    def read(self):
        ''' Read the value on this pin.'''
        if self._pinMode == GPIO.IN:
            return gpio.input(self._pinNum)
        else:
            return RuntimeError("GPIO not configured for reading")

    @property
    def pinNum(self):
        return self._pinNum
