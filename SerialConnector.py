import serial
import time

arduino = serial.Serial(port='COM12', baudrate=115200, timeout=0.1)

x = 1

while True:
    print(x)
    arduino.write(bytes([x]))  # Convert integer to byte and send it
    time.sleep(0.5)
    x += 1  # Increment x so that the value changes each time
