class ConnectionHandler(object):
    def handle(self, connection, client_address):
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
