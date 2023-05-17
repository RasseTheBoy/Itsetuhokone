
from machine import Pin, Timer # type:ignore
from utime import sleep # type:ignore

onboard_led = Pin(25, Pin.OUT)
onboard_led_timer = Timer(-1)
onboard_led_timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: onboard_led.toggle())

# ------------------------------

import uasyncio as asyncio # type:ignore

led = Pin(13, Pin.OUT)
led2 = Pin(12, Pin.OUT)

class Led:
    def __init__(self, pin_num:int, name:str='Led', value:int=0) -> None:
        self.pin = Pin(pin_num, Pin.OUT, value=value)

        self.name = name
        self.toggles = 0
        self.run = True


    def pprint(self, *args, **kwargs):
        print(f'{self.name}:', *args, **kwargs)


    async def do_toggles(self, toggle_amnt:int=10, delay:float=0.5):
        while self.toggles < toggle_amnt and self.run:
            self.pin.toggle()
            self.toggles += 1
            self.pprint('Toggled')
            await asyncio.sleep(delay)

    async def start(self, toggle_amnt:int=10, delay:float=0.5):
        await self.do_toggles(toggle_amnt, delay)

    
async def main():
    await asyncio.gather(led1.start(), led2.start(delay=1.5))


led1 = Led(13, 'Led 1')
led2 = Led(12, 'Led 2')

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Interrupted')
    led1.run = False
    led2.run = False
except Exception as err:
    print('Error:', err)

finally:
    led1.pin.value(0)
    led2.pin.value(0)
    print('Done')
