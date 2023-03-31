from machine    import Pin

from class_copy     import Base

class FlipFlopBtn(Base):
    def __init__(self, set_pin_num:int, reset_pin_num:int, name:str='Flip flop button', debug_print:bool=False):
        super().__init__(name, debug_print)

        self._set_pin = Pin(set_pin_num, Pin.IN, Pin.PULL_UP)
        self._reset_pin = Pin(reset_pin_num, Pin.IN, Pin.PULL_UP)
        self.state = False

    
    def read_pin(self, pin:Pin):
        """Reads given pin value, and retuns `True` if button if pin is high; Else `False`"""
        if pin.value() == 0:
            return True
        return False


    def check(self):
        """Checks state of flip_flop.
        Returns `True` if flip-flop is set; Else `False`"""
        if not self.state:
            if self.read_pin(self._set_pin) and not self.read_pin(self._reset_pin):
                self.state = True
                self.pprint('Set to True')
        
        else:
            if self.read_pin(self._reset_pin):
                self.state = False
                self.pprint('Set to False')

        return self.state