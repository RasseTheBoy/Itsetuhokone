from machine import Pin
from utime   import sleep

from motor  import Motor
from servo  import Servo


class Itsetuhokone:
    def __init__(self):
        def_out_pin = lambda pin_num : Pin(pin_num, Pin.OUT)

        self.on_board_len = def_out_pin(25)

        self.kuljetin = Motor(5, 6, 'Kuljetin') # Kuljetin moottori
        self.nostomotti = Servo(0, servo_name='Nostomotti', min_pos_val=1500, max_pos_val=8150, debug_print=True)


    def run(self):
        pass



Itsetuhokone().run()