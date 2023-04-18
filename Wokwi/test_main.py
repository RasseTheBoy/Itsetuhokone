# THIS IS ONLY A TEST FILE
# DO NOT USE THIS FILE IN FINAL PRODUCT

from machine import Pin, ADC # type:ignore
from utime   import sleep # type:ignore

from three_axis_accelerometer import Accelerometer

onboard_led = Pin(25, Pin.OUT)

# Test ADC on one pin and print the output
def test_adc(pin_num:int):
    """Test ADC on one pin and print the output"""
    adc = ADC(pin_num)
    while True:
        onboard_led.toggle()
        print(adc.read_u16())
        sleep(0.1)


# Test Accelerometer
def test_accelerometer():
    """Test accelerometer"""
    acc = Accelerometer(28, debug_print=False)
    while True:
        onboard_led.toggle()
        val_lst = acc.update()
        print(val_lst)
        sleep(0.1)


# test_adc(28)

test_accelerometer()