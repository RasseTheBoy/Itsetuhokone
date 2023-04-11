from class_copy     import Base
from utime  import ticks_ms, ticks_diff


class CSVFileEditor(Base):
    """Edits text files"""
    def __init__(self, filename:str, headers:list, write_wait_time_s:int=1, add_timer:bool=True, separator:str=';', debug_print:bool=False):
        """Initializes CSVFileEditor
        
        Parameters:
            `filename` (str): Name of the file
            `headers` (list[str]): List of headers
            `write_wait_time_s` (int): Time between writing data to file (in seconds)
            `add_timer` (bool): Add timer to data
            `separator` (str): Separator between values
            `debug_print` (bool): Print debug info"""
        
        super().__init__(filename, debug_print=debug_print)
        
        self._filename = filename
        self._headers = headers
        self._write_wait_time_s = write_wait_time_s
        self._add_timer = add_timer
        self._separator = separator

        self._last_write_time = ticks_ms()

        self._setup_file()

    
    def _setup_file(self):
        """Sets up file if it doesn't exist, is empty or has wrong headers"""
        self.pprint('Setting up file')

        if self._add_timer:
            self._headers.insert(0, 'time')

        _headers = self._separator.join([str(header) for header in self._headers])
        self.write(_headers)

        self.pprint('File setup done')
        

    def _read_as(self, ret_as:str='r'):
        """Reads file, and returns it as a list of rows or as collumns
        
        Parameters:
            `ret_as` (str): Row (`r`) or collumn (`c`)
            
        Returns:
            `list` or `None`"""
        
        def read_file():
            """Reads file; returns None if file doesn't exist"""
            try:
                with open(self._filename, 'r', encoding='utf-8') as f:
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
        """Writes text to file"""
        with open(self._filename, 'w', encoding='utf-8') as f:
            f.write(text)
        
        self.pprint('text written to file')


    def append_data(self, data:list):
        """Appends data to file if given time has passed"""

        if ticks_diff(ticks_ms(), self._last_write_time) < self._write_wait_time_s * 1000: # If time hasn't passed
            return
        
        if self._add_timer:
            data.insert(0, ticks_ms() / 1000)

        with open(self._filename, 'a', encoding='utf-8') as f:
            data = [str(d) for d in data] # Convert all data to strings
            f.write(self._separator.join(data))

        self._last_write_time = ticks_ms()
        
        self.pprint(f'Data appended to file -> {data}')



if __name__ == '__main__':
    from time import sleep

    c = CSVFileEditor('test.csv', ['sensor1', 'sensor2'])
    
    for _ in range(10):
        c.append_data([1, 2])
        sleep(1)