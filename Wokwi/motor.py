from machine import Pin

from class_copy     import Base

class Motor(Base):
    """Simple controller for a single motor with two relays contorlling it's rotation."""
    def __init__(self, relayCw_pin_num:int, relayCCw_pin_num:int, name:str='motor', debug_print:bool=False):
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
    

    def stop_all(self, dopprint:bool=True):
        """Stops motor from spinning"""
        self.relayCw.off()
        self.relayCCw.off()
        self.pprint('Stopped', dopprint)


    def config(self, **kwargs):
        """Configure class variables:
        `name`, `debug_print`"""
        self._base_config(**kwargs)