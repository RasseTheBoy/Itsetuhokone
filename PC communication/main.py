from FastDebugger   import fd

import serial

from time import sleep


def setup_serial():
    """Setup serial communication with the micropython board.
    Not returning before the serial connection is established.
    """
    tries = 0
    while True:
        try:
            ser = serial.Serial('COM3', 115200, timeout=1)
            ser.flush()
            print('Serial connection established.')
            return ser
        
        except serial.SerialException:
            tries += 1
            print(f'Failed to connect to serial port. Try {tries}')
            sleep(1)


def read_serial(ser):
    """Read data from the serial connection."""
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if line == 'Done':
                break


if __name__ == '__main__':
    ser = setup_serial()
    read_serial(ser)