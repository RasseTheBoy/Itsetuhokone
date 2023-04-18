# Author: Rasmus Ohert

from class_copy import Base
from machine import ADC, Pin # type:ignore



class Accelerometer(Base):
    """Class for a three axis accelerometer"""

    def __init__(self, x_pin=None, y_pin=None, z_pin=None, name:str='Accelerometer', decimal_len:int=2, simple_read:bool=True, simple_max_val:int=100, debug_print:bool=False) -> None:
        """Initializes accelerometer
        
        Parameters:
            `x_pin` (int): Pin number for x axis
            `y_pin` (int): Pin number for y axis
            `z_pin` (int): Pin number for z axis
            `name` (str): Name of the accelerometer. Default: 'Accelerometer'
            `decimal_len` (int): Decimal length of returned values. Default: 2
            `simple_read` (bool): If True, returns values between 0 and `simple_max_val`. Else returns values between 0 and 65535. Default: True
            `simple_max_val` (int): Maximum value of accelerometer. Default: 100
            `debug_print` (bool): If True, prints debug messages. Default: False"""
        super().__init__(name, debug_print)

        # Setup class variables
        self.decimal_len = decimal_len
        self.simple_read = simple_read
        self.simple_max_val = simple_max_val

        pin_lst = [x_pin, y_pin, z_pin] # Setup list of given pins

        # Check if atleast one pin is given
        if pin_lst.count(None) == 3:
            raise ValueError('Atleast one pin must be given')
        
        # Setup pins
        setup_adc_pins = lambda pin_num: ADC(Pin(pin_num, mode=Pin.IN)) if pin_num is not None else None
        self._xyz_pins = [setup_adc_pins(pin) for pin in pin_lst]

        # Read initial values
        self.xyz_last_values = [self._read_pin_value(pin) for pin in self._xyz_pins]


    def _read_pin_value(self, pin:Pin):
        """Reads value from pin
        
        Parameters:
        - `pin` (machine.Pin): Pin to read from"""
        if pin is None:
            ret_val = 0
        else:
            ret_val = pin.read_u16()

        if self.simple_read:
            return ret_val / 65535 * self.simple_max_val
        return ret_val
    

    def update(self, ret_type:type=float, get_vals:str='diff') -> list:
        """Updates values of accelerometer
        
        Parameters:
        - `ret_type` (type): Type of returned values. Default: `float`
        - `get_vals` (str): 'diff' or 'new'. Default: 'diff'"""

        # Read new values
        xyz_new_values = [self._read_pin_value(pin) for pin in self._xyz_pins]

        if get_vals == 'new': 
            self.pprint(f'xyz_new_values: {xyz_new_values}')

        # Compare if values have changed, save the difference and update last state
        xyz_diff_values = [new - last for new, last in zip(xyz_new_values, self.xyz_last_values)]
        self.xyz_last_values = xyz_new_values

        if get_vals == 'diff':
            self.pprint(f'xyz_diff_values: {xyz_diff_values}')

        if get_vals == 'new':
            ret_val_lst = xyz_new_values
        elif get_vals == 'diff':
            ret_val_lst = xyz_diff_values
        else:
            raise ValueError(f'Invalid value for get_vals: {get_vals}')

        if ret_type == float:
            return [round(diff, self.decimal_len) for diff in ret_val_lst]
        elif ret_type == int:
            return [int(diff) for diff in ret_val_lst]
        elif ret_type == str:
            return [f'{diff:.{self.decimal_len}f}' for diff in ret_val_lst]
        else:
            raise TypeError(f'Invalid return type: {ret_type}')
    
    
    def config(self, **kwargs):
        """Configure class variables:
        `name`, `debug_print`, `tolerance`"""
        self._base_config(**kwargs)