from machine import Pin, SPI
import time
import machine

MOSI = 11
SCK = 10
RCLK = 9

KILOBIT = 0xFE
HUNDREDS = 0xFD
TENS = 0xFB
UNITS = 0xF7
Dot = 0x80

SEG8Code = [
    0x3F,  # 0
    0x06,  # 1
    0x5B,  # 2
    0x4F,  # 3
    0x66,  # 4
    0x6D,  # 5
    0x7D,  # 6
    0x07,  # 7
    0x7F,  # 8
    0x6F,  # 9
    0x77,  # A
    0x7C,  # b
    0x39,  # C
    0x5E,  # d
    0x79,  # E
    0x71,  # F
    0xFF,  # 8.
    0x40,  # -
    0x79,  # E
    0x33  # R
]


class LED_8SEG:
    def __init__(self):
        self.rclk = Pin(RCLK, Pin.OUT)
        self.rclk(1)  # type: ignore
        self.spi = SPI(1)
        self.spi = SPI(1, 1000_000)
        self.spi = SPI(1, 10000_000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=None)
        self.SEG8 = SEG8Code

    def write_cmd(self, num, seg):
        self.rclk(1)  # type: ignore
        self.spi.write(bytearray([num]))
        self.spi.write(bytearray([seg]))
        self.rclk(0)  # type: ignore
        time.sleep(0.002)
        self.rclk(1)  # type: ignore

    def write_to_registers(self, num, seg, num2, seg2, num3, seg3):
        self.write_cmd(num, seg)
        self.write_cmd(num2, seg2)
        self.write_cmd(num3, seg3)


class Temp_read:
    def __init__(self):
        self.temperature = None
        self.reading = None
        self.sensor_temp = machine.ADC(4)
        self.conversion_factor = 3.3 / 65535

    def read_temp(self):
        self.reading = self.sensor_temp.read_u16() * self.conversion_factor
        self.temperature = 27 - (self.reading - 0.706) / 0.001721
        return self.temperature


def truncate(number: float, digits: int) -> float:
    pow10 = 10 ** digits
    return number * pow10 // 1 / pow10


def main():

    led = LED_8SEG()
    temper = Temp_read()
    start = time.time()
    led_on_board = machine.Pin("LED", machine.Pin.OUT)
    led_on_board.on()
    temperature = temper.read_temp()

    while 1:

        stop = time.time()

        if stop - start == 1:
            start = time.time()
            temperature = temper.read_temp()
            print(temperature)
            print(str(int(round(temperature, 1) * 10)) + " *C")

        rounded_temperature = int(round(temperature, 1) * 10)
        time.sleep(0.0005)

        if rounded_temperature > 100:
            led.write_to_registers(UNITS, led.SEG8[abs(rounded_temperature) % 10], TENS,
                                   led.SEG8[(abs(rounded_temperature) % 100) // 10] | Dot, HUNDREDS,
                                   led.SEG8[(abs(rounded_temperature) % 1000) // 100])
        elif rounded_temperature < 0:
            led.write_cmd(KILOBIT, led.SEG8[17])
        else:
            led.write_to_registers(UNITS, led.SEG8[19], TENS, led.SEG8[19], HUNDREDS,
                                   led.SEG8[18])  # Message "ERR" displayed on display
