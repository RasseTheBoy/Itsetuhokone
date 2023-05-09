from machine    import Pin, PWM # type:ignore
from utime  import sleep # type:ignore
from base   import Base

class Servo(Base):
    def __init__(self, pin_out:int, freq:int=50, name:str='servo', min_pos_val:int=1200, max_pos_val:int=8650, debug_print:bool=False):
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
        
        self.current_post = min_pos_val


    def move_to_pos(self, pos:str='min'):
        """Reset position to `'min'` or `'max'` position"""
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
        `min_pos_value` <= `value` <= `max_pos_value`"""
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
        """Force move to a specified location."""
        self.pwm.duty_u16(value)
        self.current_post = value
