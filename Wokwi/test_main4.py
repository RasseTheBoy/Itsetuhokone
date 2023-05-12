
from utime import sleep # type:ignore
from machine import Pin, Timer # type:ignore

onboard_led = Pin(25, Pin.OUT)
onboard_led_timer = Timer(-1)
onboard_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: onboard_led.toggle())

from running_and_error_leds import RunningAndErrorLEDs

run_err_leds = RunningAndErrorLEDs()
RUN_LED, ERR_LED = run_err_leds.get_leds()

while True:
    RUN_LED.on()
    ERR_LED.off()
    sleep(0.5)
    RUN_LED.off()
    ERR_LED.on()
    sleep(0.5)