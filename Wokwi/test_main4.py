
from utime import sleep # type:ignore
from machine import Pin, Timer # type:ignore
from base import Base

onboard_led = Pin(25, Pin.OUT)
onboard_led_timer = Timer(-1)
onboard_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: onboard_led.toggle())

# Test asyncio functionality

import uasyncio as asyncio # type:ignore

from running_and_error_leds     import RunningAndErrorLEDs
from start_stop_latch   import StartStopLatch
from servo  import Servo

RunErrLeds = RunningAndErrorLEDs(12,13)
RUNNING_LED, ERROR_LED = RunErrLeds.get_leds()


class StopPressed(Exception):
    """Raised when stop button is pressed"""
    def __init__(self, message='Stop button pressed') -> None:
        super().__init__(message)


def while_runner(func):
    async def wrapper(*args, **kwargs):
        while True:
            try:
                await func(*args, **kwargs)
            except StopPressed:
                print('Stop button pressed')

            await asyncio.sleep(0.5)

    return wrapper


class Itsetuhokone(Base):
    def __init__(self, debug_print = True) -> None:
        super().__init__('Itsetuhokone', debug_print=debug_print)
        self.start_stop = StartStopLatch(10, 11, debug_print=debug_print)
        self.servo = Servo(22, name='Vaaka moottori', min_pos_val=4500, max_pos_val=7150, debug_print=debug_print)

        self.state = 0 # Set starting state (0 = Idle)
        self.run = True


    @while_runner
    async def check_start_stop(self):
        print(f'Checking start/stop: ({self.start_stop.read_btn("start")}, {self.start_stop.read_btn("stop")})')
        
        if self.start_stop.check_both_pressed():
            self.praise(KeyboardInterrupt, 'Both buttons pressed')
        elif self.start_stop.read_btn('start'):
            self.state = 0
            self.run = True
        elif self.start_stop.read_btn('stop'):
            self.state = 0
            # self.run = False
            raise StopPressed
        await asyncio.sleep(0.5)

    @while_runner
    async def start(self):
        while self.run:
            if self.state == 0:
                RUNNING_LED.toggle()
                print('IDLE')
                if self.start_stop.check_state():
                    self.state = 10

            elif self.state == 10:
                print('Moving servo to max')
                self.servo.move_to_pos('max')
                await asyncio.sleep(0.5)
                self.state = 20

            elif self.state == 20:
                print('Moving servo to min')
                self.servo.move_to_pos('min')
                await asyncio.sleep(0.5)
                self.state = 30

            elif self.state == 30:
                print('Movig servo to mid')
                self.servo.move_to_pos('mid')
                await asyncio.sleep(0.5)
                self.state = 10

            else:
                raise ValueError(f'Invalid state: {self.state}')
            
            await asyncio.sleep(0.5)


    async def setup_async(self):
        await asyncio.gather(
            self.check_start_stop(),
            self.start()
        )

    
    def start_sync(self):
        try:
            asyncio.run(self.setup_async())
        except KeyboardInterrupt:
            print('Interrupted')
            RunErrLeds.error_blink()
        except Exception as err:
            print('Error:', err)
        finally:
            RunErrLeds.do_all('off')
            print('Done')


if __name__ == '__main__':
    itsetuhokone = Itsetuhokone()
    itsetuhokone.start_sync()
