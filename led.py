import os
import time

green_led = "/sys/class/leds/led0"
red_led = "/sys/class/leds/led1"
green_led_reset_trigger = "mmc0"
red_led_reset_trigger = "input"

def control(led_colour, state):
    # Check platform
    if not os.path.isdir(green_led):
        return

    if led_colour == "green":
        device = green_led

    elif led_colour == "red":
        device = red_led

    else:
        return

    if  state == "on":
        os.system("echo none | tee " + device + "/trigger >> /dev/null")
        os.system("echo 1 | tee " + device + "/brightness >> /dev/null") 

    elif state == "off":
        os.system("echo none | tee " + device + "/trigger >> /dev/null")
        os.system("echo 0 | tee " + device + "/brightness >> /dev/null") 

    elif state == "flash":
        os.system("echo timer | tee " + device + "/trigger >> /dev/null")
        os.system("echo 1 | tee " + device + "/brightness >> /dev/null")

    elif state == "reset":
        if device == green_led:
            trigger = green_led_reset_trigger
        elif device == red_led:
            trigger = red_led_reset_trigger

        os.system("echo " + trigger + " | tee " + device + "/trigger >> /dev/null")
        os.system("echo 1 | tee " + device + "/brightness >> /dev/null") 

    else:
        return

def led_reset_all():
    control("green", "reset")
    control("red", "reset")
    control("green", "off")
    control("red", "off")

def led_win():
    control("red", "off")
    for index in range(6):
        control("green", "flash")
        time.sleep(0.5)

def led_lose():
    control("green", "off")
    for index in range(6):
        control("red", "flash")
        time.sleep(0.5)

def led_listen():
    control("red", "off")
    time.sleep(0.5)
    control("green", "on")
    time.sleep(0.5)
