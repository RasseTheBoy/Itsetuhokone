
from machine import Pin, Timer # type:ignore

onboard_led = Pin(25, Pin.OUT)
onboard_led_timer = Timer(-1)
onboard_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: onboard_led.toggle())

# ------------------------------

from sdcard import SDCardSetup
from utime import sleep # type:ignore

# Test SD card by writing and reading a file

SDCardSetup(5, 2, 3, 4)

for _ in range(3):
    with open('sd/test.txt', 'w') as f:
        print('Writing to file...')
        f.write('Hello world!')

    sleep(8)

    with open('sd/test.txt', 'r') as f:
        print('Reading from file...')
        print(f.read())