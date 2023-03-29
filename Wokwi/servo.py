from machine    import Pin, PWM
from utime  import sleep



class Servo:
    def __init__(self, pin_out:int, freq:int=50, servo_name:str='servo', min_pos_val:int=1000, max_pos_val:int=9000, debug_print:bool=False):
        self.pwm = PWM(Pin(pin_out, Pin.OUT))
        self.pwm.freq(freq)

        self.min_pos_val    = min_pos_val
        self.max_pos_val    = max_pos_val
        self.servo_name     = servo_name
        self.debug_print    = debug_print


    def reset_pos(self, pos:str='min'):
        """Reset position to given `'min'` or `'max'` position"""
        if pos not in ('min', 'max'):
            self._print(f'Not a valid position: {pos}')
            return

        self._print(f'Reseting to position: {pos}')
        if pos == 'min':
            self.move_to(self.min_pos_val)
        elif pos == 'max':
            self.move_to(self.max_pos_val)


    def move_to(self, value:int):
        """Move to a specified location.
        `min_pos_value` <= `value` <= `max_pos_value`"""
        if value > 0:
            if value < self.min_pos_val:
                self._print(f'Cannot move to given value: {value} - Value too small (min: {self.min_pos_val})')
                return
            elif  value > self.max_pos_val:
                self._print(f'Cannot move to given value: {value} - Value too big (max: {self.min_pos_val})')
                return
            
            self.pwm.duty_u16(value)
            self._print(f'Moved to: {value}')
            return

    
    def _print(self, text, do_print:bool=True):
        """Print servo info.
        Used mainly for debugging."""
        if do_print and self.debug_print:
            print(f'{self.servo_name}: {text}')
