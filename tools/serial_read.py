import serial, time

port = "/dev/ttyACM0"
baud = 115200
s = serial.Serial(port)
s.baudrate = baud

while True:
    time.sleep(0.5)      # debouncing
    data = s.read(1)
    data = str(data.decode())
    print("get data = " + str(data))

s.close()
