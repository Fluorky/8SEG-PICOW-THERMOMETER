import network
import time


# Connect to your Wi-Fi network
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    timeout = 10  # Timeout in seconds
    start_time = time.time()
    while not wlan.isconnected() and time.time() - start_time < timeout:
        print("Connecting to WiFi...")
        time.sleep(1)

    if wlan.isconnected():
        print("Connected to WiFi")
        print("IP Address:", wlan.ifconfig()[0])
    else:
        print("Failed to connect to WiFi")
