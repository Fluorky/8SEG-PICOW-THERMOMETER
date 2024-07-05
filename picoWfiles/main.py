import thermometer8seg
import config
import wifconnection

if __name__ == "__main__":
    wifconnection.connect_to_wifi(config.wifi_ssid, config.wifi_password)
    thermometer8seg.main()
