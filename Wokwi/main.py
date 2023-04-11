from machine import Pin # type:ignore
from utime   import sleep # type:ignore

from capacitive_sens    import CapacitiveSensor
from csv_file_editor    import CSVFileEditor
from flip_flop_btn  import FlipFlopBtn
from class_copy     import Base
from motor  import Motor
from servo  import Servo


class Itsetuhokone(Base):
    def __init__(self, sleep_time:float=0.3, debug_print:bool=False):
        super().__init__('Itsetuhokone', debug_print=debug_print)

        self.pprint('Initializing')

        self.sleep_time = sleep_time # Sleep time between loops
        
        self.state = 0 # Set starting state (0 = Idle)

        self.on_board_led = Pin(25, Pin.OUT) # For debugging

        # Moottorit
        self.kuljetin = Motor(5, 6, 'Kuljetin', debug_print=debug_print) # Kuljetin moottori
        self.nostomotti = Servo(0, name='Nostomotti', min_pos_val=1500, max_pos_val=8150, debug_print=debug_print) # Nostomotti

        # Anturit
        self.anturi_a1 = CapacitiveSensor(10, 'Anturi a1', debug_print=debug_print)
        self.anturi_a2 = CapacitiveSensor(12, 'Anturi a2', debug_print=debug_print)
        self.anturi_b1 = CapacitiveSensor(14, 'Anturi b1', debug_print=debug_print)
        self.anturi_b2 = CapacitiveSensor(15, 'Anturi b2', debug_print=debug_print)

        self.anturi_lst = [self.anturi_a1, self.anturi_a2, self.anturi_b1, self.anturi_b2]

        # Start/Stop napit
        self.start_stop = FlipFlopBtn(2,3, name='Start/Stop napit', debug_print=debug_print)

        # CSV tiedosto
        _header_lst = [anturi.get_name() for anturi in self.anturi_lst]
        self.data_history_csv = CSVFileEditor('sensor_data.csv', _header_lst, debug_print=debug_print)

        self.pprint('Initialized')


    def stprint(self, text): # State print
        """Prints text with the state number included"""
        print(f'Itsetuhokone: [{self.state}] - {text}')

    
    def _update_csv_data(self):
        """Updates data to CSV file"""
        _data_lst = [anturi.read() for anturi in self.anturi_lst] # Reads values from sensors
        self.data_history_csv.append_data(_data_lst) # Appends data to CSV file


    def run(self):
        """Runs main code"""
        self.pprint('Running')

        while True:
            self.on_board_led.toggle()

            self._update_csv_data() # Updates data to CSV file

            if self.state == 0: # Idle
                self.stprint('Idle')
                if self.start_stop.check():
                    self.state = 10

            elif self.state == 10: # Start:
                self.stprint('Starting')
                self.state = 11

            elif self.state == 11: # Input options
                self.state = 20

            elif self.state == 20: # Tarkista tallennus
                self.state = 21

            elif self.state == 21: # Luo tallennustiedosto
                self.state = 22

            elif self.state == 22: # Aloita tallennus
                self.state = 23

            elif self.state == 23: # Aja alkuasemaan
                self.state = 24

            elif self.state == 24: # Tarkistaa anturidatan (optional)
                self.state = 30

            elif self.state == 30: # Aloita ajosekvenssi
                self.stprint('At 30!')
                self.state = 31

            elif self.state == 31: # Tuote keskelle (A->B)
                self.state = 32

            elif self.state == 32: # Vaaka ylös/Punnitse
                self.state = 33

            elif self.state == 33: # Vaaka alas
                self.state = 34

            elif self.state == 34: # Tuote päätyyns (A->B)
                self.state = 35

            elif self.state == 35: # Tuote keskelle (B->A)
                self.state = 36

            elif self.state == 36: # Punnitse
                self.state = 37

            elif self.state == 37: # Vaaka alas
                self.state = 38

            elif self.state == 38: # Tuote päätyyn (B->A)
                self.state = 39

            elif self.state == 39: # Sekvenssi valmis
                self.state = 30


            else: # Invalid state code
                self.stprint('[!] Invalid state code [!]')

            if self.state != 0 and not self.start_stop.check():
                self.state = 0
                self.stprint('Stopping')

            sleep(self.sleep_time)



Itsetuhokone(debug_print=True).run()