from machine    import Pin, PWM # type:ignore
from utime  import sleep # type:ignore
from base   import Base

class Servo(Base):
    def __init__(self, pin_out:int, freq:int=50, name:str='servo', min_pos_val:int=1200, max_pos_val:int=8650, default_pos:str='mid', debug_print:bool=False):
        """Initialize servo class.
        
        Parameters:
        - `pin_out` (int): Pin to output to servo motor (PWM).
        - `freq` (int): Frequency of PWM. Default: `50`
        - `name` (str): Name of class. Default: `'servo'`
        - `min_pos_val` (int): Minimum position value. Default: `1200`
        - `max_pos_val` (int): Maximum position value. Default: `8650`
        - `default_pos` (str): Default position to move to. Default: `'mid'`
        - `debug_print` (bool): If `True`, print debug info; if `False`, do not print. Default: `False`"""
        super().__init__(name, debug_print)
        
        self.pwm = PWM(Pin(pin_out, Pin.OUT))
        self.pwm.freq(freq)

        self.freq = freq

        self.min_pos_val    = min_pos_val
        self.max_pos_val    = max_pos_val
        self.mid_pos_val    = (max_pos_val - min_pos_val) // 2 + min_pos_val

        self.pos_vals = {   
                            'min': self.min_pos_val,
                            'mid': self.mid_pos_val,
                            'max': self.max_pos_val
                        }
        

        self.force_move(self.mid_pos_val)


    def move_to_pos(self, pos:str):
        """Reset position to a position.
        
        Parameters:
        - `pos` (str): Position to move to.
            - `'min'`: Minimum position
            - `'mid'`: Middle position
            - `'max'`: Maximum position"""
        if pos not in self.pos_vals:
            self.pprint(f'Not a valid position: {pos}')
            return
        
        if self.current_post == self.pos_vals[pos]:
            self.pprint(f'Already at pos: {pos}')
            return
        elif self.current_post < self.pos_vals[pos]:
            freq_amnt = self.freq
        elif self.current_post > self.pos_vals[pos]:
            freq_amnt = -self.freq
        else:
            self.pprint(f'Error: {self.current_post} - {self.pos_vals[pos]}')
            return

        self.pprint(f'Moving to pos: {pos} from {self.current_post} to {self.pos_vals[pos]}')
        for pos_val in range(self.current_post, self.pos_vals[pos], freq_amnt):
            self.move_to_int(pos_val)


    def move_to_int(self, value:int):
        """Move to a specified location.

        Parameters:
        - `value` (int): Value to move to. Must be within `min_pos_value` <= `value` <= `max_pos_value`"""
        if value < self.min_pos_val:
            self.pprint(f'Cannot move to given value: {value} - Value too small (min: {self.min_pos_val})')
            return
        elif  value > self.max_pos_val:
            self.pprint(f'Cannot move to given value: {value} - Value too big (max: {self.min_pos_val})')
            return
        
        self.pwm.duty_u16(value)
        self.current_post = value
        sleep(0.01)


    def force_move(self, value:int):
        """Force move to a specified location.
        
        Parameters:
        - `value` (int): Can be any value. No limits."""
        self.pwm.duty_u16(value)
        self.current_post = value
