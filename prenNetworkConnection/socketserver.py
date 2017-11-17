import socket


class SocketServer(object):
    def __init__(self, address="localhost", port=12345):
        self.address = address
        self.port = port

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.bind((self.address, self.port))
        sock.listen(1)
'''
        while True:
            print("waiting for a connection")
            connection, client_address = sock.accept()
        
            try:
                print("connection from {address}".format(address=client_address))

                while True:
                    data = connection.recv(16)
                    print(type(data))
                    print(len(data))
                    print("received {!r}".format(data))
                    if data:
                        print("sending data back to the client")
                        connection.sendall(data)
                    else:
                        print("no data from {address}".format(address=client_address))
                        break

            finally:
                connection.close()
            '''


if __name__ == '__main__':
    SocketServer().start()
