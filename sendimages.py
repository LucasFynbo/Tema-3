import socket

class JpgfileSender:
    def __init__(self, filePath, serverAddress, serverPort):
        self.filePath = filePath
        self.serverAddress = serverAddress
        self.serverPort = serverPort
        
    def send (self):
            
        with open(self.filePath, 'rb') as f:
            jpgData = f.read()
            
        request = (
            b"POST /upload HTTP/1.1\r\n"
            b"Host: " + self.serverAddress.encode() + b":" + str(self.serverPort).encode() + b"\r\n"
            b"Content-Type: image/jpeg\r\n"
            b"Content-Length: " + str(len(jpgData)).encode() + b"\r\n"
            b"\r\n" +
            jpgData
        )
            
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            s.connect((self.serverAddress, self.serverPort))
            s.sendall(request)
            response = s.recv(4096)
            print(response.decode())
            
        finally:
            s.close

filePath = '/images/image1.jpg'
serverAddress = '192.168.99.145'
serverPort = 8000

jpgSender = JpgfileSender (filePath, serverAddress, serverPort)
jpgSender.send()