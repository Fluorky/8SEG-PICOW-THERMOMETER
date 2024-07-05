import thermometer8seg
import config
import wificonnection

if __name__ == "__main__":
    wificonnection.connect_to_wifi(config.wifi_ssid, config.wifi_password)
    thermometer8seg.main()
