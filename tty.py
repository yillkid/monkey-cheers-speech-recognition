import serial, time

port = "/dev/ttyACM0"
baud = 115200

def write(value):
    s = serial.Serial(port)
    s.baudrate = baud
    s.write((value + '\n').encode())
    s.close()

def read():
    s = serial.Serial(port)
    s.baudrate = baud
    content = s.read(1).decode()
    s.close()

    return content
