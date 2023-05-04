# Author: Rasmus Ohert

from class_copy import Base
from machine import ADC, Pin # type:ignore



class Accelerometer(Base):
    """Class for a three axis accelerometer"""

    def __init__(self, x_pin=None, y_pin=None, z_pin=None, name:str='Accelerometer', decimal_len:int=2, simple_read:bool=False, simple_max_val:int=100, analog_pin_max_val:int=65535, debug_print:bool=False) -> None:
        """Initializes accelerometer
        
        Parameters:
        - `x_pin` (int): Pin number for x axis
        - `y_pin` (int): Pin number for y axis
        - `z_pin` (int): Pin number for z axis
        - `name` (str): Name of the accelerometer. Default: 'Accelerometer'
        - `decimal_len` (int): Decimal length of returned values. Default: `2`
        - `simple_read` (bool): If `True`, returns values between `0` and `simple_max_val`. Else returns values between `0` and `analog_pin_max_val`. Default: `False`
        - `simple_max_val` (int): Maximum value of accelerometer. Default: `100`
        - `analog_pin_max_val` (int): Maximum value of analog pin. Default: `65535`
        - `debug_print` (bool): If `True`, prints debug messages. Default: `False`"""
        super().__init__(name, debug_print, decimal_len, simple_read, simple_max_val, analog_pin_max_val)

        pin_lst = [x_pin, y_pin, z_pin] # Setup list of given pins

        # Check if atleast one pin is given
        if pin_lst.count(None) == 3:
            raise ValueError('Atleast one pin must be given')
        
        # Setup pins
        setup_adc_pins = lambda pin_num: ADC(Pin(pin_num, mode=Pin.IN)) if pin_num is not None else None
        self._xyz_pins = [setup_adc_pins(pin) for pin in pin_lst]

        # Read initial values
        self.xyz_last_values = [self._read_pin_raw(pin) for pin in self._xyz_pins]
    

    def _format_output(self, xyz_vals:list[float|int]) -> str:
        """Formats output
        
        Parameters:
        - `xyz_vals` (list[float|int]): List of x, y and z values"""
        xyz = 'x y z'.split(' ')
        return ' '.join([f'{xyz[i]}: {xyz_vals[i]}' for i in range(3)])

    def update(self, ret_type:type=float, get_val:str='new') -> list:
        """Updates values of accelerometer
        
        Parameters:
        - `ret_type` (type): Type of returned values. Default: `float`
            - `float`: Returns value with decimal length of `decimal_len`
            - `int`: Returns values rounded to integers
            - `str`: Returns values as a string
        - `get_val` (str): Type of returned values. Default: `'new'`
            - `'new'`: Returns new values
            - `'diff'`: Returns difference between new and last values"""

        # Read new values
        xyz_new_values = [self._read_pin_raw(pin) for pin in self._xyz_pins]
            
        # Compare if values have changed, save the difference and update last state
        xyz_diff_values = [new - last for new, last in zip(xyz_new_values, self.xyz_last_values)]
        self.xyz_last_values = xyz_new_values

        # Print values and set return value
        if get_val == 'new':
            self.pprint(f'xyz_new_values: {self._format_output(xyz_new_values)}')
            ret_val_lst = xyz_new_values
        elif get_val == 'diff':
            self.pprint(f'xyz_diff_values: {self._format_output(xyz_diff_values)}')
            ret_val_lst = xyz_diff_values
        else:
            raise ValueError(f'Invalid value for get_val: {get_val}')

        # Return values
        if ret_type == float:
            return [round(val, self.decimal_len) for val in ret_val_lst]
        elif ret_type == int:
            return [int(val) for val in ret_val_lst]
        elif ret_type == str:
            return [f'{val:.{self.decimal_len}f}' for val in ret_val_lst]
        else:
            raise TypeError(f'Invalid return type: {ret_type}')
    

    def _read_pin_raw(self, pin):
        """Reads raw value from pin"""
        return pin.read_u16() if pin is not None else 0

    
    def config(self, **kwargs):
        """Configure class variables:
        `name`, `debug_print`"""
        self._base_config(**kwargs)