import socket
import os

class fileRecv():
    def __init__(self, host, port, uploadDirectory):
        self. host = host
        self.port = port
        self.uploadDirectory = uploadDirectory
        self.counter = 1

    def recvFile(self, conn):
        fileData = b''
        while True: 
            chunk = conn.recv(4096)
            if not chunk:
                break
            fileData += chunk

        filename = f'recvImage_{self.counter}.jpg'
        self.counter += 1

        with open(os.path.join(self.uploadDirectory, filename), 'wb') as f:
            f.write(fileData)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            print (f"serveren lytter efter på {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"connected by {addr}")
                    self.recvFile(conn)
                    print("fil modtaget {filename}")

def main():
    host = '0.0.0.0'
    port = 8000
    uploadDirectory = r'c:\Users\Mads\Desktop'

    receiver = fileRecv(host, port, uploadDirectory)
    receiver.start()

if __name__=="__main__":
    main()
