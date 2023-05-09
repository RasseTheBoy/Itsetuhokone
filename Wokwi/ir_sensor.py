# Author: Rasmus Ohert

from base import Base
from machine    import Pin # type:ignore


class IRSensor(Base):
    """Simple IR-sensor class."""
    def __init__(self, pin_num:int, name:str='IR sensor', debug_print:bool=False):
        """Initializes class.
        
        Parameters:
        - `pin_num` (int): Pin number to use.
        - `name` (str): Name of class instance. Default: 'IR sensor'
        - `debug_print` (bool): If `True`, prints debug messages. Default: `False`"""
        super().__init__(name, debug_print)

        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)

        self._last_state = self.read()

    
    def update(self, get_val:str='raw') -> int|bool:
        """Updates sensor read value. 

        Parameters:
        - `get_val` (str): What to return. Default: `'raw'`
            - `'raw'`: Returns raw (`int`) value from pin
            - `'changed'`: Returns `True` if value has changed, else `False`"""
        
        _current_state = self.read()

        # Check if value has changed since last udpate
        _changed = False
        if self._last_state != _current_state:
            self.pprint(f'Changed value {self._last_state} -> {_current_state}')
            _changed = True

        # Update last state
        self._last_state = _current_state

        # Return value
        if get_val == 'raw':
            return self.pin.value()
        elif get_val == 'changed':
            return _changed
        else:
            raise ValueError(f'Invalid return value given: {get_val}')


    def read(self) -> bool:
        """Read current pin value.
        
        Returns `True` if value is `0`, else `False`."""
        if self.pin.value() == 1:
            return False
        return True