import serial, time

port = "/dev/ttyACM0"
baud = 115200

def a():
    s = serial.Serial(port)
    s.baudrate = baud

    while True:
        time.sleep(0.5)      # debouncing
        s.write('1\n'.encode())

    s.close()

a()
