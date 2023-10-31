import serial

PORT = "COM7"

ser = serial.Serial(port=PORT, baudrate=1000000, bytesize=8, parity="N", stopbits=1)
