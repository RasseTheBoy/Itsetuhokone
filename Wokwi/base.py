# Author: Rasmus Ohert

class Base:
    """Base class for other classes. Contains basic functions and variables."""
    def __init__(self, name:str, debug_print:bool=False, decimal_len:int=2, simple_read:bool=False, simple_max_val:int=100, analog_pin_max_val:int=65535) -> None:
        """Initialize class. Set name and debug_print.
        
        Parameters:
        - `name` (str): Name of class
        - `debug_print` (bool): If `True`, print debug info; if `False`, do not print. Default: `False`
        - `simple_max_val` (int): Max value for simple_read. Default: `100`
        - `analog_pin_max_val` (int): Max value for analog pin read. Default: `65535`"""

        # Setup class variables
        self.name = name
        self.debug_print = debug_print

        # Setup for analog pins
        self.decimal_len = decimal_len
        self.simple_read = simple_read
        self.simple_max_val = simple_max_val
        self.analog_pin_max_val = analog_pin_max_val


    def pprint(self, *texts, do_print:bool=True) -> None:
        """Print info.
        Mainly used for debugging.
        
        Parameters:
        - `texts`: Texts to print; can be multiple
        - `do_print`: If `True`, print; if `False`, do not print"""
        
        if not (do_print and self.debug_print):
            return

        # Print first item
        if len(texts) == 1:
            print(f'{self.name}: {texts[0]}')
            return
        
        print(f'{self.name}: {texts[0]}', end=' ')

        # Print other items without name; except last item
        for item in texts[1:-1]:
            print(item, end=' ')

        print(texts[-1]) # Print last item


    def praise(self, raise_as, text:str=''):
        """Prints texts and raises error.
        
        Parameters:
        - `raise_as`: Error to raise"""
        self.pprint(text)
        raise raise_as(text)


    def get_name(self) -> str:
        """Returns name of class.
        
        Returns:
        - `name` (str): Name of class"""
        return self.name


    def _format_analog_value(self, val):
        """Formats analog value to simplified value if `simple_read` is `True`.
        Else returns `val` unchanged.
        
        Parameters:
        - `val`: Value to format
        
        Returns:
        - `val` (int/float): Formatted value"""
        if self.simple_read:
            return round(val / self.analog_pin_max_val * self.simple_max_val, self.decimal_len)
        return val


    def config(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                self.pprint(f'Cannot set attribute: {key} - Attribute does not exist')