import serial, time

arduino = serial.Serial('/dev/ttyACM0', 115200);

for i in range(5):
    arduino.write(b'H')
    time.sleep(1)
    arduino.write(b'L')
    time.sleep(1)
