from machine import Pin, PWM # type:ignore
from utime import sleep # type:ignore

pwm = PWM(Pin(1))
pwm.freq(50)


def move_to(to_pos:int):
    """Move to a specified location."""
    print(f'Pos: {to_pos}')
    pwm.duty_u16(to_pos)
    sleep(0.5)

# for pos in range(7000, 9000, 50):
#     move_to(pos)

move_to(1200)
