# Author: Rasmus Ohert

from machine import Pin, Timer # type:ignore
from utime   import sleep # type:ignore

from capacitive_sens    import CapacitiveSensor
from csv_file_editor    import CSVFileEditor
from flip_flop_btn  import FlipFlopBtn
from class_copy     import Base
from motor  import Motor
from servo  import Servo


class Itsetuhokone(Base):
    """Main class for Itsetuhokone project."""
    def __init__(self, sleep_time:float=0.3, debug_print:bool=False):
        """Initializes class.

        Parameters:
        - `sleep_time` (float): Sleep time between loops. Default: `0.3`
        - `debug_print` (bool): If `True`, prints debug messages. Default: `False`"""
        super().__init__('Itsetuhokone', debug_print=debug_print)

        self.pprint('Initializing')

        self.sleep_time = sleep_time # Sleep time between loops
        
        self.state = 0 # Set starting state (0 = Idle)

        # Onboard LED; toggles every second
        # Mainly for debugging purposes; can be removed
        self.on_board_led = Pin(25, Pin.OUT)
        onboard_led_timer = Timer(-1)
        onboard_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.on_board_led.toggle())

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


    def stprint(self, text):
        """Prints text with the state number included
        
        Parameters:
        - `text` (Any): Text to print"""
        print(f'Itsetuhokone: [{self.state}] - {text}')

    
    def _update_csv_data(self):
        """Updates data to CSV file"""
        _data_lst = [anturi.read() for anturi in self.anturi_lst] # Reads values from sensors
        self.data_history_csv.append_data(_data_lst) # Appends data to CSV file

    
    def _lift_and_weigh(self):
            sleep(1)
            self.nostomotti.move_to_pos('max')

            # Add code for vaaka here
            self.stprint('Punnitse...')
            sleep(1)

            self.nostomotti.move_to_pos('min')
            sleep(1)

    
    def _move_to_start(self):
        """Moves to start position (A1)"""
        self.stprint('Moving to start position')
        while not self.anturi_a1.read():
            self.kuljetin.run_cw()

        self.kuljetin.stop_all()
        self.stprint('At start position')

    
    def _move_to_middle(self, from_pos:str):
        """Moves to middle position (from `A` or `B`)
        
        Parameters:
        - `from_pos` (str): Position to move from (`A` or `B`)"""
        self.stprint('Moving to middle position')
        while not self.anturi_a2.read() and not self.anturi_b2.read():
            if from_pos == 'A':
                self.kuljetin.run_ccw()
            elif from_pos == 'B':
                self.kuljetin.run_cw()
            else:
                self.kuljetin.stop_all()
                self.stprint(f'[!] Invalid from_pos: {from_pos} [!]')
                return

        self.kuljetin.stop_all()
        self.stprint('At middle position')


    def run(self):
        """Runs main code"""
        self.pprint('Running...')

        while True:
            self._update_csv_data() # Updates data to CSV file

            if self.state == 0: # Idle
                self.stprint('Idle')
                if self.start_stop.check():
                    self.state = 10

            elif self.state == 10: # Start:
                self.stprint('Starting')
                self.state = 23

            elif self.state == 23: # Aja alkuasemaan
                self._move_to_start()
                self.state = 31

            elif self.state == 31: # Tuote keskelle (A->B)
                self._move_to_middle('A')

                self.state = 32

            elif self.state == 32: # Vaaka ylös/Punnitse
                self._lift_and_weigh()

                self.state = 34

            elif self.state == 34: # Tuote päätyyn (A->B)
                while not self.anturi_b1.read():
                    self.kuljetin.run_ccw()

                self.kuljetin.stop_all()
                self.stprint('At end position')

                sleep(1) # Wait a second before going back to middle

                self.state = 35

            elif self.state == 35: # Tuote keskelle (B->A)
                self._move_to_middle('B')

                self.state = 36

            elif self.state == 36: # Punnitse
                self._lift_and_weigh()

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