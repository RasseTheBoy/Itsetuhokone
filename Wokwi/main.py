from machine import Pin
from utime   import sleep

from capacitive_sens    import CapacitiveSensor
from class_copy     import Base
from motor  import Motor
from servo  import Servo


class Itsetuhokone(Base):
    def __init__(self, debug_print:bool=False):
        super().__init__('Itsetuhokone', debug_print=debug_print)

        self.pprint('Initializing')

        # For debugging
        self.on_board_led = Pin(25, Pin.OUT)

        # Moottorit
        self.kuljetin = Motor(5, 6, 'Kuljetin', debug_print=debug_print) # Kuljetin moottori
        self.nostomotti = Servo(0, name='Nostomotti', min_pos_val=1500, max_pos_val=8150, debug_print=debug_print) # Nostomotti

        # Anturit
        self.anturi_a1 = CapacitiveSensor(10, 'Anturi a1', debug_print=debug_print)
        self.anturi_a2 = CapacitiveSensor(12, 'Anturi a2', debug_print=debug_print)
        self.anturi_b1 = CapacitiveSensor(14, 'Anturi b1', debug_print=debug_print)
        self.anturi_b2 = CapacitiveSensor(15, 'Anturi b2', debug_print=debug_print)


    def run(self):
        self.pprint('Running')
        while True:
            self.on_board_led.toggle()

            self.anturi_a1.check()
            self.anturi_a2.check()
            self.anturi_b1.check()
            self.anturi_b2.check()

            sleep(0.3)



Itsetuhokone(debug_print=True).run()