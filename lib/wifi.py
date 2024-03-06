import network
import sys
import time

def connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        print("Already Connected with IP:", sta_if.ifconfig()[0])
        return sta_if.ifconfig()[0]
    sta_if.active(True)
    try:
        sta_if.config(dhcp_hostname="ESP32")
        sta_if.connect(ssid, password)
    except Exception as err:
        sta_if.active(False)
        print("Error:", err)
        sys.exit()
    print("Connecting", end="")
    n = 0
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(1)
        n += 1
        if n == 60:
            break
    if n == 60:
        sta_if.active(False)
        print("\nGiving up! Not connected!")
    else:
        print("\nNow connected with IP:", sta_if.ifconfig()[0])
        return sta_if.ifconfig()[0]

if __name__ == "__main__":
    esp_ip = connect("AP1830", "19QwertL")
    print(f"IP: {esp_ip}")
