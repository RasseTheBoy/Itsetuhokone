# Author: Rasmus Ohert

from base import Base
from machine    import Pin # type:ignore

class StartStopLatch(Base):
    """Simple start-stop latch class."""
    def __init__(self, set_pin_num:int, reset_pin_num:int, name:str='Flip flop button', debug_print:bool=False):
        """Initializes class.

        Parameters:
        - `set_pin_num` (int): Pin number to use for setting flip-flop.
        - `reset_pin_num` (int): Pin number to use for resetting flip-flop.
        - `name` (str): Name of class instance. Default: 'Flip flop button'
        - `debug_print` (bool): If `True`, prints debug messages. Default: `False`"""
        super().__init__(name, debug_print)

        self._set_pin = Pin(set_pin_num, Pin.IN, Pin.PULL_UP)
        self._reset_pin = Pin(reset_pin_num, Pin.IN, Pin.PULL_UP)
        self.state = False

    
    def __call__(self):
        return self.check()
    

    def read_btn(self, btn:str):
        if btn == 'set':
            return self._read_pin(self._set_pin)
        elif btn == 'reset':
            return self._read_pin(self._reset_pin)
        else:
            self.pprint(f'Invalid button name: {btn}')
            raise ValueError(f'Invalid button name: {btn}')


    def check_both_pressed(self):
        """Checks if both buttons are pressed.

        Returns:
        - `bool`: `True` if both buttons are pressed, else `False`"""
        return self._read_pin(self._set_pin) and self._read_pin(self._reset_pin)


    def _read_pin(self, pin:Pin):
        """Reads given pin value, and retuns `True` if button if pin is high; Else `False`"""
        if pin.value() == 1:
            return True
        return False


    def check(self) -> bool:
        """Checks state of flip_flop.

        Returns:
        - `bool`: `True` if flip-flop is set, else `False`"""
        if not self.state:
            if self._read_pin(self._set_pin) and not self._read_pin(self._reset_pin):
                self.state = True
                self.pprint('Set to True')
        
        else:
            if self._read_pin(self._reset_pin):
                self.state = False
                self.pprint('Set to False')

        return self.state