# Author: Rasmus Ohert

from base import Base
from machine    import ADC # type:ignore


class ForceSensor(Base):
    def __init__(self, pin_num:int, name:str='Force sensor', decimal_len:int=2, simple_read:bool=False, simple_max_val:int=100, analog_pin_max_val:int=65535, debug_print:bool=False) -> None:
        """Force sensor class

        Parameters:
        - `pin_num` (int): Pin number to use.
        - `name` (str): Name of class instance. Default: 'Force sensor'
        - `debug_print` (bool): If `True`, prints debug messages. Default: `False`"""
        super().__init__(name, debug_print, decimal_len, simple_read, simple_max_val, analog_pin_max_val)

        # Setup class variables
        self.decimal_len = decimal_len

        # Setup pin
        self.pin = ADC(pin_num)

        # Read initial value
        self.update()


    def update(self) -> float:
        """Update class variables
        
        Returns:
        - `float`: Raw value of pin"""
        self._last_state = self._read_raw()

        # Return value
        return self._format_analog_value(self._last_state)

    
    def _read_raw(self):
        """Read raw value from sensor and round it to `decimal_len` decimal places"""
        raw_val = round(self.pin.read_u16(), self.decimal_len)
        self.pprint(f'Raw value: {raw_val}')
        return raw_val