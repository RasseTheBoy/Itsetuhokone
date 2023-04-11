class Base:
    def __init__(self, name:str, debug_print:bool=False) -> None:
        self.name = name
        self.debug_print = debug_print

    def pprint(self, text, do_print:bool=True) -> None:
        """Print info.
        Mainly used for debugging."""
        if do_print and self.debug_print:
            print(f'{self.name}: {text}')

    def _base_config(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'debug_print':
                self.debug_print = value
            elif key == 'name':
                self.name = value

    def get_name(self) -> str:
        return self.name