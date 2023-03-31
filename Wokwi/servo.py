from machine    import Pin, PWM
from utime  import sleep

from class_copy     import Base

class Servo(Base):
    def __init__(self, pin_out:int, freq:int=50, name:str='servo', min_pos_val:int=1000, max_pos_val:int=9000, debug_print:bool=False):
        super().__init__(name, debug_print)
        
        self.pwm = PWM(Pin(pin_out, Pin.OUT))
        self.pwm.freq(freq)

        self.min_pos_val    = min_pos_val
        self.max_pos_val    = max_pos_val
        self.debug_print    = debug_print


    def reset_pos(self, pos:str='min'):
        """Reset position to `'min'` or `'max'` position"""
        if pos not in ('min', 'max'):
            self.pprint(f'Not a valid position: {pos}')
            return

        self.pprint(f'Reseting to position: {pos}')
        if pos == 'min':
            self.move_to(self.min_pos_val)
        elif pos == 'max':
            self.move_to(self.max_pos_val)


    def move_to(self, value:int):
        """Move to a specified location.
        `min_pos_value` <= `value` <= `max_pos_value`"""
        if value > 0:
            if value < self.min_pos_val:
                self.pprint(f'Cannot move to given value: {value} - Value too small (min: {self.min_pos_val})')
                return
            elif  value > self.max_pos_val:
                self.pprint(f'Cannot move to given value: {value} - Value too big (max: {self.min_pos_val})')
                return
            
            self.pwm.duty_u16(value)
            self.pprint(f'Moved to: {value}')
            return


    def config(self, **kwargs):
        """Configure class variables:
        `name`, `debug_print`"""
        self._base_config(**kwargs)
