import time

def write(value):    
    f = open("/dev/ttyACM0", "w")
    f.write(value + "\n")
    f.close()
