import time
import serial
import sys

PORT = '/dev/ttyACM1'
BAUDRATE = 9600
TIMEOUT = None

con = serial.Serial("/dev/ttyACM0", 9600, timeout=None)
time.sleep(2)

print(con.write("t".encode()))

print(con.readline().decode())
print(con.readline().decode())
con.close()

