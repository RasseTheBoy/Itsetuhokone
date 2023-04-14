
from class_copy import Base
from machine import ADC # type:ignore



class Accelerometer(Base):
    def __init__(self, x_pin=None, y_pin=None, z_pin=None, tolerance:int=100, min_val:int=0, max_val:int=1024, name:str='Accelerometer', debug_print:bool=False) -> None:
        super().__init__(name, debug_print)

        # Check if only one pin is `None`
        if [x_pin, y_pin, z_pin].count(None) > 1:
            raise ValueError('Only one pin can be `None`')
        
        # Setup class variables
        self._tolerance = tolerance
        self._min_val = min_val
        self._max_val = max_val
        
        # Setup pins
        setup_adc_pins = lambda pin: ADC(pin) if pin is not None else None
        self._xyz_pins = [setup_adc_pins(pin) for pin in [x_pin, y_pin, z_pin]]

        # Read initial values
        self.xyz_last_values = [self._read_pin_value(pin) for pin in self._xyz_pins]


    def _read_pin_value(self, pin):
        """Reads given pin value, and retuns `True` if button if pin is high; Else `False`"""
        if pin is None:
            return 0
        return pin.read()
    

    def update(self):
        """Updates values of accelerometer"""

        # Read new values
        xyz_new_values = [self._read_pin_value(pin) for pin in self._xyz_pins]

        # Compare if values have changed, save the difference and update last state
        xyz_diff_values = [new - last for new, last in zip(xyz_new_values, self.xyz_last_values)]
        self.xyz_last_values = xyz_new_values

        # Return difference values
        return xyz_diff_values
    
    
    def config(self, **kwargs):
        """Configure class variables:
        `name`, `debug_print`, `tolerance`"""
        self._base_config(**kwargs)

        for key, value in kwargs.items():
            if key == 'tolerance':
                self._tolerance = value