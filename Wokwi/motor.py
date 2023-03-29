from machine import Pin


class Motor:
    """Simple controller for a single motor with two relays contorlling it's rotation."""
    def __init__(self, relayCw_pin_num:int, relayCCw_pin_num:int, motor_name:str='motor', debug_print:bool=False):
        self.relayCw    = Pin(relayCw_pin_num, Pin.OUT)
        self.relayCCw   = Pin(relayCCw_pin_num, Pin.OUT)
        self.motor_name = motor_name
        self.debug_print = debug_print


    def run_cw(self):
        """Run motor clockwise"""
        self.stop_all(False)
        self.relayCw.on()
        self._print('Running clockwise')
    

    def run_ccw(self):
        """Run motor counterclockwise"""
        self.stop_all(False)
        self.relayCCw.on()
        self._print('Running counterclockwise')
    

    def stop_all(self, do_print:bool=True):
        """Stops motor from spinning"""
        self.relayCw.off()
        self.relayCCw.off()
        self._print('Stopped', do_print)


    def config(self, **kwargs):
        """Configure class variables:
        `motor_name`, `debug_print`"""
        for arg_key, arg_item in kwargs.items():
            if arg_key == 'motor_name':
                self.motor_name = arg_item

            elif arg_key == 'debug_print':
                self.debug_print = arg_ite                   


    def _print(self, text, do_print:bool=True):
        """Print motor info.
        Used mainly for debugging."""
        if do_print and self.debug_print:
            print(f'{self.motor_name}: {text}')


# m = Motor(Pin(0, Pin.OUT), Pin(1, Pin.OUT)) # For debugging