import network
import sys
import time

class WifiConnector:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.hostname = "ESP32"
        self.sta_if = network.WLAN(network.STA_IF)
    
    def connect(self):
        if self.sta_if.isconnected():
            print("Already Connected")
            return
        self.sta_if.active(True)
        try:
            if self.hostname:
                self.sta_if.config(dhcp_hostname=self.hostname)
            self.sta_if.connect(self.ssid, self.password)
        except Exception as err:
            self.sta_if.active(False)
            print("Error:", err)
            sys.exit()
        print("Connecting", end="")
        n = 0
        while not self.sta_if.isconnected():
            print(".", end="")
            time.sleep(1)
            n += 1
            if n == 60:
                break
        if n == 60:
            self.sta_if.active(False)
            print("\nGiving up! Not connected!")
        else:
            print("\nNow connected with IP:", self.sta_if.ifconfig()[0])
            return self.sta_if.ifconfig()[0]

if __name__ == "__main__":
     wifi = WifiConnector("ITLab", "MaaGodt*7913")
     wifi.connect()