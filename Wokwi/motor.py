# Author: Rasmus Ohert

from class_copy import Base
from machine    import Pin # type:ignore


class Motor(Base):
    """Simple controller for a single motor with two relays contorlling it's rotation."""
    def __init__(self, relayCw_pin_num:int, relayCCw_pin_num:int, name:str='motor', debug_print:bool=False):
        """Initializes class.

        Parameters:
        - `relayCw_pin_num` (int): Pin number to use for clockwise rotation.
        - `relayCCw_pin_num` (int): Pin number to use for counterclockwise rotation.
        - `name` (str): Name of class instance. Default: 'motor'
        - `debug_print` (bool): If `True`, prints debug messages. Default: `False`"""
        super().__init__(name, debug_print)
        
        self.relayCw    = Pin(relayCw_pin_num, Pin.OUT)
        self.relayCCw   = Pin(relayCCw_pin_num, Pin.OUT)


    def run_cw(self):
        """Run motor clockwise"""
        self.stop_all(False)
        self.relayCw.on()
        self.pprint('Running clockwise')
    

    def run_ccw(self):
        """Run motor counterclockwise"""
        self.stop_all(False)
        self.relayCCw.on()
        self.pprint('Running counterclockwise')
    

    def stop_all(self, do_print:bool=True):
        """Stops motor from spinning
        
        Parameters:
        - `do_print` (bool): If `True`, prints debug message. Default: `True`"""
        self.relayCw.off()
        self.relayCCw.off()
        self.pprint('Stopped', do_print)


    def config(self, **kwargs):
        """Configure class variables:
        `name`, `debug_print`"""
        self._base_config(**kwargs)