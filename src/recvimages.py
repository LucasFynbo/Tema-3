import socket
import os
import errno

class MySocket:
    def __init__(self):
        HOST = "0.0.0.0"
        PORT = 8000
        backlog = 5

        directory = r'C:\Users\Administrator\Desktop\images'

        
        self.data_handler = DataHandler(upload_directory = directory)

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.tcp_socket.bind((HOST, PORT)) # Binder socket sammen med porten.
            print('[i] Waiting for connection... \n\n')
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                print('[!] Address Already in use, rebinding...') 
                # TCP socket rebinding
                self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.tcp_socket.bind((HOST, PORT))

                print('[i] Rebinding succeded.')
            else:
                print('[!] Socket error: %s' % e)

            print (f"serveren lytter efter på {HOST}:{PORT}")

        self.tcp_socket.listen(backlog)

    def accept_tcp_connections(self):
        while True:
            conn, addr = self.tcp_socket.accept()
            with conn:
                print(f"connected by {addr}")
                self.data_handler.recv_file(conn)
                print("fil modtaget {filename}")

    def close_socket(self):
        self.tcp_socket.close()

class DataHandler():
    def __init__(self, upload_directory):
        self.counter = 1
        self.upload_directory = upload_directory

    def recv_file(self, conn):
        file_data = b''
        while True: 
            try:
                chunk = conn.recv(4096)
            except Exception as e:
                print(f"Connection reset by peer: {e}")
                break

            if not chunk:
                break

            file_data += chunk
            print(len(file_data))

        filename = f'recv_image_{self.counter}.jpg'
        self.counter += 1
	
        try:
            with open(os.path.join(self.upload_directory, filename), 'wb') as f:
                f.write(file_data.split(b'\r\n')[4].strip())
        except:
            print("Error writing. Skipping...")

        conn.close()
    

if __name__=="__main__":
    
    socket = MySocket()
    try:
        socket.accept_tcp_connections()
    finally:
        socket.close_socket()
