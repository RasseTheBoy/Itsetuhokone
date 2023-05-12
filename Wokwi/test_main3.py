
from machine import Pin, Timer # type:ignore
from utime import sleep # type:ignore

onboard_led = Pin(25, Pin.OUT)
onboard_led_timer = Timer(-1)
onboard_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: onboard_led.toggle())

# ------------------------------

from ir_sensor import IRSensor

ir_a1 = IRSensor(6, 'Anturi a1')
ir_a2 = IRSensor(7, 'Anturi a2')
ir_b1 = IRSensor(8, 'Anturi b1')
ir_b2 = IRSensor(9, 'Anturi b2')

sensor_lst = [ir_a1, ir_a2, ir_b1, ir_b2]

def move_to_middle():
    print('Moving to middle')
    while not all([ir.read() for ir in [ir_a2, ir_b2]]):
        print('Moving...')
        sleep(0.5)

    print('Moved to middle')


move_to_middle()