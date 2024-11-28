import serial
import time

try:
    ser = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=1)
    print(f"Serial port opened: {ser.name}")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

while True:
    try:
        data = ser.readline().decode('utf-8').strip()
        if data:
            print(f"Received: {data}")
    except Exception as e:
        print(f"Error reading data: {e}")
        time.sleep(1)
