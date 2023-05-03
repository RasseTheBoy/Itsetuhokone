# THIS IS ONLY A TEST FILE
# DO NOT USE THIS FILE IN FINAL PRODUCT

from machine import Pin, Timer # type:ignore

onboard_led = Pin(25, Pin.OUT)

timer = Timer(-1)
timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: onboard_led.toggle())

# ------------------------------

from machine import ADC # type:ignore
from utime import sleep # type:ignore

def read_adc(pin_num:int):
    """Read analog input from pin 28"""
    adc = ADC(pin_num)
    while True:
        print(adc.read_u16())
        sleep(0.5)

def read_digital(pin_num:int):
    """Read digital input from pin 28"""
    pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
    while True:
        print(pin.value())
        sleep(0.5)

def read_digital_and_analog(digital_pin_num:int, analog_pin_num:int):
    """Read digital and analog input from pin 28"""
    dig = Pin(digital_pin_num, Pin.IN, Pin.PULL_UP)
    adc = ADC(analog_pin_num)
    while True:
        print(f'{dig.value()} {adc.read_u16()}')
        sleep(0.5)

def read_digitals_and_analogs(dig_pin_num_lst:list[int]|int=[], ana_pin_num_lst:list[int]|int=[]):
    """Read digital and analog pins"""

    # Convert to list if only one pin is given
    if isinstance(dig_pin_num_lst, int):
        dig_pin_num_lst = [dig_pin_num_lst]
    if isinstance(ana_pin_num_lst, int):
        ana_pin_num_lst = [ana_pin_num_lst]

    # Setup digital and analog pins into lists
    dig_lst = [{'pin_num': pin_num, 'pin': Pin(pin_num, Pin.IN)} for pin_num in dig_pin_num_lst]
    ana_lst = [{'pin_num': pin_num, 'pin': ADC(pin_num)} for pin_num in ana_pin_num_lst]

    # Read digital and analog pins
    while True:
        # Format text to include pin name and value
        text = ''
        text_format =  lambda pin_num, pin_value :  f'[{pin_num}] - {pin_value}   ---   '
        for dig in dig_lst + ana_lst:
            try:
                text += 'Digi: ' + text_format(pin_num=dig['pin_num'], pin_value=dig['pin'].value())
            except AttributeError:
                text += 'Anal: ' + text_format(pin_num=dig['pin_num'], pin_value=dig['pin'].read_u16())
            
            except Exception as err:
                text += text_format.format(pin_name=dig['pin_num'], pin_value=err)

        # Remove last '---'
        text = text[:-7]

        print(text)
        sleep(0.5)


# read_digitals_and_analogs(dig_pin_num_lst=[6,7,8,9])
