# this code will write serial input to arduino to control the LED

import pyserial, time

arduino = serial.Serial('/dev/ttyACM0',115200,timeout=1)
time.sleep(1)
