# Author: Rasmus Ohert

from base import Base
from utime  import ticks_ms, ticks_diff # type:ignore


class CSVFileEditor(Base):
    """Edits text files"""
    def __init__(self, file_path:str, headers:list, write_wait_time_s:int=1, add_timer:bool=True, timer_decimals:int=0, separator:str=';', encoding:str='utf-8', debug_print:bool=False):
        """Initializes CSVFileEditor
        
        Parameters:
        - `file_path` (str): Name of the file
        - `headers` (list[str]): List of headers
        - `write_wait_time_s` (int): Time between writing data to file (in seconds). Default: `1`
        - `add_timer` (bool): Add timer to data. Default: `True`
        - `timer_decimals` (int): Number of decimals in timer. Default: `0`
        - `separator` (str): Separator between values in file. Default: `';'`
        - `encoding` (str): Encoding of file. Default: `'utf-8'`
        - `debug_print` (bool): Print debug info. Default: `False`"""
        
        super().__init__(file_path, debug_print=debug_print)
        
        self._file_path = file_path
        self._headers = headers
        self._write_wait_time_s = write_wait_time_s
        self._add_timer = add_timer
        self._timer_decimals = timer_decimals
        self._separator = separator
        self.encoding = encoding

        self._last_write_time = ticks_ms()

        self._setup_file()

    
    def _setup_file(self) -> None:
        """Sets up file if it doesn't exist, is empty or has wrong headers"""
        self.pprint('Setting up file')

        if self._add_timer:
            self._headers.insert(0, 'Time')

        _headers = self._separator.join([str(header) for header in self._headers])
        self.write(f'sep={self._separator}\n{_headers}') # Write headers to file; and set separator (meant for excel)

        self.pprint('File setup done')
        

    def _read_as(self, ret_as:str='r') -> list | None:
        """Reads file, and returns it as a list of rows or as collumns
        
        Parameters:
        - `ret_as` (str): Return as
            - `'r'`: rows
            - `'c'`: collumns
            
        Returns:
        - `list` or `None`"""
        
        def read_file():
            """Reads file; returns None if file doesn't exist"""
            try:
                with open(self._file_path, 'r', encoding=self.encoding) as f:
                    return f.read()
            except FileNotFoundError:
                self.pprint('File not found')
                return None      

        _read = read_file()
        
        if not _read or ret_as not in ['r', 'c']:
            return

        _lines = _read.splitlines()
        if ret_as == 'r':
            return _lines
        elif ret_as == 'c':
            return list(zip(*_lines))[::-1]
        
    
    def write(self, text:str):
        """Writes text to file
        
        Parameters:
        - `text` (str): Text to write"""
        with open(self._file_path, 'w', encoding=self.encoding) as f:
            f.write(text)
        
        self.pprint('text written to file')


    def append_data(self, data:list):
        """Appends data to file if given time has passed
        
        Parameters:
        - `data` (list): Data to append to file"""

        if ticks_diff(ticks_ms(), self._last_write_time) < self._write_wait_time_s * 1000: # If time hasn't passed
            return
        
        if self._add_timer:
            time = f'{ticks_ms()/1000:.{self._timer_decimals}f}' # Format time to 1 decimal
            data.insert(0, time) # Insert time at start of data

        with open(self._file_path, 'a', encoding=self.encoding) as f:
            data = [str(d) for d in data] # Convert all data to strings
            f.write(f'\n{self._separator.join(data)}')

        self._last_write_time = ticks_ms()
        
        self.pprint(f'Data appended to file -> {data}')