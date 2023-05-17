# Author: Rasmus Ohert

from machine    import Pin # type:ignore
from base import Base


class Button(Base):
    def __init__(self, pin_num:int, name:str='Button') -> None:
        """Initializes Button class.

        Parameters
        ----------
        pin_num : int
            Pin number for button.

        pin_name : str
            Name of button. Default: 'Button'"""
        super().__init__(name)
        self.pin = Pin(pin_num, Pin.IN)

    
    def read_raw_pin(self):
        """Reads raw pin.

        Return
        ------
        int
            Raw data read value of pin."""
        return self.pin.value()
    

    def read_pin(self):
        """Reads pin.
        
        Return
        ------
        bool
            `True` if pin is high, else `False`.
            
        Note
        ----
        `True` means that button is pressed."""
        return self.pin.value() == 1


class StartStopLatch(Base):
    """Simple start-stop latch class."""
    def __init__(self, start_pin_num:int, stop_pin_num:int, name:str='Flip flop button', debug_print:bool=False):
        """Initializes class.
        
        Parameters
        ----------
        start_pin_num : int
            Pin number for start button.
            
        stop_pin_num : int
            Pin number for stop button.
            
        name : str
            Name of class. Default: 'Flip flop button'
            
        debug_print : bool
            If `True`, print debug info; if `False`, do not print. Default: `False`"""
        super().__init__(name, debug_print)

        self.start_button = Button(start_pin_num, 'Start button')
        self.stop_button = Button(stop_pin_num, 'Stop button')
        self.state = False

    
    def __call__(self):
        """Returns state of start-stop-latch.

        Return
        ------
        bool
            `True` if "latch" is set, else `False`."""
        return self.check_state()
    

    def read_btn(self, btn:str):
        """Reads given button.
        
        Parameters
        ----------
        btn : str
            Name of button to read. Valid names are 'start' and 'stop'.
            
        Return
        ------
        bool
            `True` if button is pressed, else `False`.
            
        Raises
        ------
        ValueError
            If given button name is invalid."""
        if btn == 'start':
            return self.start_button.read_pin()
        elif btn == 'stop':
            return self.stop_button.read_pin()
        else:
            self.praise(ValueError, f'Invalid button name: {btn}')


    def check_both_pressed(self):
        """Checks if both buttons are pressed.
        
        Return
        ------
        bool
            `True` if both buttons are pressed, else `False`."""
        return self.start_button.read_pin() and self.stop_button.read_pin()


    def check_state(self) -> bool:
        """Checks state of start-stop-latch.
        
        Return
        ------
        bool
            `True` if "latch" is set, else `False`."""
        if not self.state:
            if self.start_button.read_pin() and not self.stop_button.read_pin():
                self.state = True
                self.pprint('Set to True')
        
        else:
            if self.stop_button.read_pin():
                self.state = False
                self.pprint('Set to False')

        return self.state