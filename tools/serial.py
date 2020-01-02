import time

count = 0
value = "1"
while True:
    if count % 2 == 0:
        value = "1"
    else:
        value = "2"

    f = open("/dev/ttyACM0", "w")
    f.write(value + "\n")
    f.close()
    time.sleep(1)
    count = count + 1
