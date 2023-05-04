# Author: Rasmus Ohert

from class_copy import Base
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

    
    def check(self) -> bool:
        """Checks if value has changed since last check.
        Returns `True` if it has changed, else `False`."""
        
        _current_state = self.read()

        # Check if value has changed since last udpate
        _changed = False
        if self._last_state != _current_state:
            self.pprint(f'Changed value {self._last_state} -> {_current_state}')
            _changed = True

        # Update last state
        self._last_state = _current_state

        return _changed


    def read(self) -> int:
        """Read current pin value."""
        if self.pin.value() == 1:
            return False
        return True


    def config(self, **kwargs):
        """Configure class variables:
        `name`, `debug_print`"""
        self._base_config(**kwargs)