# Author: Rasmus Ohert

from machine import Pin, Timer # type:ignore
from utime   import sleep # type:ignore

from three_axis_accelerometer   import Accelerometer
from running_and_error_leds     import RunningAndErrorLEDs
from csv_file_editor    import CSVFileEditor
from flip_flop_btn  import FlipFlopBtn
from force_sensor   import ForceSensor
from ir_sensor  import IRSensor
from sdcard     import SDCardSetup
from motor  import Motor
from servo  import Servo
from base   import Base


RunErrLeds = RunningAndErrorLEDs()
RUNNING_LED, ERROR_LED = RunErrLeds.get_leds()


class Itsetuhokone(Base):
    """Main class for Itsetuhokone project."""
    def __init__(self, sleep_time:float=0.3, csv_add_timer:bool=True, debug_print:bool=False):
        """Initializes class.

        Parameters:
        - `sleep_time` (float): Sleep time between loops. Default: `0.3`
        - `debug_print` (bool): If `True`, prints debug messages. Default: `False`"""
        super().__init__('Itsetuhokone', debug_print=debug_print)

        self.pprint('Initializing')

        self.sleep_time = sleep_time # Sleep time between loops
        
        self.state = 0 # Set starting state (0 = Idle)

        # Onboard LED; toggles every second
        # Mainly for debugging purposes; can be removed/disabled if needed
        self.on_board_led = Pin(25, Pin.OUT)
        onboard_led_timer = Timer(-1)
        onboard_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.on_board_led.toggle())

        # Moottorit
        self.kuljetin = Motor(0, 1, 'Kuljetin', debug_print=debug_print) # Kuljetin moottori
        self.nostomotti = Servo(10, name='Vaaka moottori', min_pos_val=1500, max_pos_val=8150, debug_print=debug_print) # Vaaka moottori
        # Nosto moottori ei ole tällä hetkellä käytössä/kytketty

        # IR anturit
        self.ir_a1 = IRSensor(6, 'Anturi a1', debug_print=debug_print)
        self.ir_a2 = IRSensor(7, 'Anturi a2', debug_print=debug_print)
        self.ir_b1 = IRSensor(8, 'Anturi b1', debug_print=debug_print)
        self.ir_b2 = IRSensor(9, 'Anturi b2', debug_print=debug_print)

        # Vaaka anturi (voima-anturi)
        self.vaaka = ForceSensor(28, 'Vaaka', debug_print=debug_print)

        # Värinä anturi
        self.accelerometer = Accelerometer(x_pin=26, y_pin=27, name='Värinä anturi', debug_print=debug_print)

        # Listaa kaikki anturit
        self.sensor_lst = [self.ir_a1, self.ir_a2, self.ir_b1, self.ir_b2, self.vaaka, self.accelerometer]

        # Start/Stop napit
        self.start_stop = FlipFlopBtn(17, 16, name='Start/Stop napit', debug_print=debug_print)

        # SD kortti ja CSV tiedosto
        SDCardSetup(5, 2, 3, 4)
        _header_lst = [sensor.get_name() for sensor in self.sensor_lst]
        self.data_history_csv = CSVFileEditor('sd/sensor_data.csv', _header_lst, add_timer=csv_add_timer, debug_print=debug_print)

        self.pprint('Initialized')


    def stprint(self, text):
        """Prints text with the state number included
        
        Parameters:
        - `text` (Any): Text to print"""
        print(f'Itsetuhokone: [{self.state}] - {text}')

    
    def _update_csv_data(self):
        """Updates data to CSV file"""
        _data_lst = [sensor.update() for sensor in self.sensor_lst] # Reads values from sensors
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
        while not self.ir_a1.read():
            self.kuljetin.run_cw()

        self.kuljetin.stop_all()
        self.stprint('At start position')

    
    def _move_to_middle(self, from_pos:str):
        """Moves to middle position (from `A` or `B`)
        
        Parameters:
        - `from_pos` (str): Position to move from (`A` or `B`)"""
        self.stprint('Moving to middle position')
        while not self.ir_a2.read() and not self.ir_b2.read():
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
                    RUNNING_LED.toggle()
                    self.state = 10

            elif self.state == 10: # Start:
                self.stprint('Starting')
                RUNNING_LED.on()
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
                while not self.ir_b1.read():
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
                while not self.ir_a1.read():
                    self.kuljetin.run_cw()

                self.kuljetin.stop_all()
                self.stprint('At end position')
                self.state = 39

            elif self.state == 39: # Sekvenssi valmis
                self.stprint('Sequence done')
                self.state = 30


            else: # Invalid state code
                self.stprint('[!] Invalid state code [!]')

            if self.state != 0 and not self.start_stop.check():
                RUNNING_LED.off()
                self.state = 0
                self.stprint('Stopping')
                self.kuljetin.stop_all()

            sleep(self.sleep_time)


try:
    Itsetuhokone(debug_print=False).run()
except Exception as err:
    print(f'Error: {err}')
    RunErrLeds.error_blink()