import socket

class ImgFileSender:
    def __init__(self, serverIP, serverPort):
        self.serverAddress = (serverIP, serverPort)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.serverAddress = f"{serverIP}:{serverPort}"

    def send(self, filePath):
        try:
            filePath = filePath
            with open(filePath, 'rb') as f:
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
    filePath = '/images/potala-palace.jpg'
    serverIP = '172.20.10.2'
    serverPort = 8000

    connect_to_wifi = ConnectHandler("AP1830","qwert123")
    connect_to_wifi.activate()
    
    jpgSender = ImgFileSender(serverIP, serverPort)
    jpgSender.send(filePath)
