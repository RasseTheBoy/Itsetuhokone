
from utime import sleep # type:ignore
from machine import Pin, Timer # type:ignore

onboard_led = Pin(25, Pin.OUT)
onboard_led_timer = Timer(-1)
onboard_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: onboard_led.toggle())

error_led = Pin(14, Pin.OUT)

def error_blink():
    while True:
        error_led.toggle()
        sleep(0.5)


def main():
    print('In main')
    raise Exception('Error in main')

try:
    main()
except Exception as err:
    print(f'Error: {err}')
    error_blink()