import socket
import os

class file_recv():
    def __init__(self, host, port, upload_directory):
        self.host = host
        self.port = port
        self.upload_directory = upload_directory
        self.counter = 1

    def recv_file(self, conn):
        conn.recv(75) # For at undgå at HTTP headers bliver en del af billedet, skipper vi de første 75 recieved bits
        file_data = b''
        while True: 
            chunk = conn.recv(4096)

            if not chunk:
                break
            file_data += chunk
            print(len(file_data))

        filename = f'recv_image_{self.counter}.jpg'
        self.counter += 1

        with open(os.path.join(self.upload_directory, filename), 'wb') as f:
            f.write(file_data)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()

            print (f"serveren lytter efter på {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"connected by {addr}")
                    self.recv_file(conn)
                    print("fil modtaget {filename}")

def main():
    host = '172.20.10.2'
    port = 8000
    upload_directory = r'C:\script\images'

    receiver = file_recv(host, port, upload_directory)
    receiver.start()

if __name__=="__main__":
    main()
