import thermometer8seg
import config
import wifconnection

if __name__ == "__main__":
    thermometer8seg.main()
    wifconnection.connect_to_wifi(config.wifi_ssid, config.wifi_password)
