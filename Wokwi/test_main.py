# THIS IS ONLY A TEST FILE
# DO NOT USE THIS FILE IN FINAL PRODUCT

from machine import Pin, Timer # type:ignore

onboard_led = Pin(25, Pin.OUT)

timer = Timer(-1)
timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: onboard_led.toggle())

# ------------------------------

