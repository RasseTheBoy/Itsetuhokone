# THIS IS ONLY A TEST FILE
# DO NOT USE THIS FILE IN FINAL PRODUCT

from machine import Pin, Timer # type:ignore

onboard_led = Pin(25, Pin.OUT)

timer = Timer(-1)
timer.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: onboard_led.toggle())

# ------------------------------

from utime import sleep # type:ignore

# Control motor from given pin

def toggle_motor(motor_pin_num:int):
    """Toggle motor on/off.
    
    Parameters:
    - `motor_pin_num`: Pin number of motor"""
    
    motor_pin = Pin(motor_pin_num, Pin.OUT)
    while True:
        sleep(1)
        motor_pin.toggle()
        print(f'Toggled motor {motor_pin_num}: {motor_pin.value()}')


def keep_motor_on(motor_pin_num:int):
    """Keep motor on.
    
    Parameters:
    - `motor_pin_num`: Pin number of motor"""
    
    motor_pin = Pin(motor_pin_num, Pin.OUT)
    motor_pin.value(1)
    print(f'Keeping motor {motor_pin_num} on: {motor_pin.value()}')


def hold_motor_on(motor_pin_num:int, time_s:int):
    """Hold motor on for given time.
    
    Parameters:
    - `motor_pin_num`: Pin number of motor
    - `time_s`: Time in seconds"""
    
    motor_pin = Pin(motor_pin_num, Pin.OUT)
    motor_pin.value(1)
    print(f'Keeping motor {motor_pin_num} on: {motor_pin.value()}')
    sleep(time_s)
    motor_pin.value(0)
    print(f'Turned motor {motor_pin_num} off: {motor_pin.value()}')



# hold_motor_on(15, 5)
keep_motor_on(15)