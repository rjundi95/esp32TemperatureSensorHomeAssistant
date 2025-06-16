import network
import time

# Connect to Wi-Fi
ssid = ''             # name of the wifi network
password = ''         # password of the wifi network

def do_connect():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    # Wait for connection
    while not station.isconnected():
        print("Connecting...")
        time.sleep(3)

    print('Connection successful!')
    print(station.ifconfig())  # Displays IP address
    print(station.ifconfig()[0])
    esp32_IP = station.ifconfig()[0]
    
#do_connect()

