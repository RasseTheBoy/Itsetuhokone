
from utime import sleep # type:ignore
from start_stop_latch  import StartStopLatch


start_stop = StartStopLatch(10, 11, debug_print=True)

while True:
    if start_stop.check_both_pressed():
        print('Both buttons pressed')
        raise KeyboardInterrupt('Both buttons pressed')
    if start_stop.read_btn('start'):
        print('Start button pressed')
    elif start_stop.read_btn('stop'):
        print('Stop button pressed')
        break
    else:
        print('No button pressed')
    sleep(0.5)