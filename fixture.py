import board
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from collections import namedtuple

def init():
    LED = namedtuple('LED', ('power', 'mac', 'ip'))
    led = LED( (DigitalInOut(board.D1),
                DigitalInOut(board.D4)),
               (DigitalInOut(board.D18),
                DigitalInOut(board.D19)),
               (DigitalInOut(board.D12),
                DigitalInOut(board.D11)))

    led.power[0].direction = Direction.OUTPUT
    led.power[1].direction = Direction.OUTPUT
    led.mac[0].direction = Direction.OUTPUT
    led.mac[1].direction = Direction.OUTPUT
    led.ip[0].direction = Direction.OUTPUT
    led.ip[1].direction = Direction.OUTPUT

    voltage = AnalogIn(board.A3)
    
    return (led, lambda: voltage.value * 2 * 3.27 / 65536)

