# Author: Rasmus Ohert

class Base:
    """Base class for other classes. Contains basic functions and variables."""
    def __init__(self, name:str, debug_print:bool=False) -> None:
        """Initialize class. Set name and debug_print.
        
        Parameters:
        - `name` (str): Name of class
        - `debug_print` (bool): If `True`, print debug info; if `False`, do not print"""
        self.name = name
        self.debug_print = debug_print


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


    def _base_config(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'debug_print':
                self.debug_print = value
            elif key == 'name':
                self.name = value


    def get_name(self) -> str:
        """Returns name of class.
        
        Returns:
        - `name` (str): Name of class"""
        return self.name