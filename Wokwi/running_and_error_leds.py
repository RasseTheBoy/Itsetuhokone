# Author: Rasmus Ohert

from machine import Pin # type:ignore
from utime   import sleep # type:ignore

class RunningAndErrorLEDs:
    def __init__(self, running_led_pin_num:int=12, error_led_pin_num:int=13) -> None:
        """Initializes class.

        Parameters:
        - `running_led_pin_num` (int): Pin number for running LED. Default: `12`
        - `error_led_pin_num` (int): Pin number for error LED. Default: `13`"""
        self.running_led = Pin(running_led_pin_num, Pin.OUT)
        self.error_led = Pin(error_led_pin_num, Pin.OUT)

        self.leds_lst = [self.running_led, self.error_led]

    
    def get_leds(self):
        """Returns list of LEDs."""
        return self.leds_lst

    
    def do_all(self, to_do:str='toggle') -> None:
        """Does given action to all LEDs.

        Parameters:
        - `to_do` (str): Action to do. Default: `toggle`
            - `on`: Turns all LEDs on.
            - `off`: Turns all LEDs off.
            - `toggle`: Toggles all LEDs."""
        if to_do == 'on':
            [led.on() for led in self.leds_lst]
        elif to_do == 'off':
            [led.off() for led in self.leds_lst]
        elif to_do == 'toggle':
            [led.toggle() for led in self.leds_lst]
        else:
            raise ValueError(f'Invalid value for `to_do`: {to_do}')
        
    
    def error_blink(self, blink_times:int=5) -> None:
        """Blinks error LED.
        
        Parameters:
        - `blink_times` (int): Number of times to blink. Default: `5`
            - `0`: Blinks infinitely.
            - `>0`: Blinks given number of times."""
        def blink_finite(blink_times:int):
            print(f'Blinking {blink_times} times')
            for _ in range(blink_times):
                self.error_led.toggle()
                sleep(0.5)
            self.error_led.off()

        def blink_infinite():
            print('Blinking infinitely')
            while True:
                self.error_led.toggle()
                sleep(0.5)

        self.running_led.off()
        if blink_times == 0:
            blink_infinite()
        else:
            blink_finite(blink_times)