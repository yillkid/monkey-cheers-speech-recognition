import netifaces as ni
import socket
import time

REMOTE_SERVER = "google.com"

def get_ip_address():
    ni.ifaddresses('wlan0')
    ip = ni.ifaddresses('wlan0')[2][0]['addr']
    return ip

def connect_time():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    before = time.perf_counter()
    s = socket.create_connection((host, 80), 2)
    after = time.perf_counter()
    
    return after - before
  except Exception as e:
    print(e)
    return -1
