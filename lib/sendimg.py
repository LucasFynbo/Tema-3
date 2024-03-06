import network
import socket
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

class ImgFileSender:
    def __init__(self, serverIP, serverPort):
        self.serverAddress = (serverIP, serverPort)
        # self.serverAddress = f"{serverIP}:{serverPort}"

    def send(self, filePath):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            image = filePath
            with open(image, 'rb') as f:
                jpgData = f.read()
                
            print(len(jpgData))
                
            request = (
                b"POST /upload HTTP/1.1\r\n"
                b"Content-Type: image/jpeg\r\n"
                b"Content-Length: " + str(len(jpgData)).encode('utf-8') + b"\r\n" + 
                b"\r\n"
            )
            print("Request length:",len(request))
            self.s.connect(self.serverAddress)

            # Send the HTTP POST request
            self.s.sendall(request)
            self.s.send(jpgData)

            # Close the socket
            self.s.close()
            print("Image sent successfully!")
        except Exception as e:
            print("Error sending image:", e)


if __name__ == "__main__":
    filePath = '/images/image1.jpg'
    serverIP = '79.171.148.163'
    serverPort = 8000

    connect("AP1830","19QwertL")

    jpgSender = ImgFileSender(serverIP, serverPort)
    jpgSender.send(filePath)
