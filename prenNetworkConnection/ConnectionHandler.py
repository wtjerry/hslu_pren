class ConnectionHandler(object):
    def handle(self, connection, client_address):
        try:
            print("connection from {address}".format(address=client_address))

            data = connection.recv(1024)
            print("received {0}".format(data))
            if data:
                print("sending data back to the client")
                connection.sendall(data)
            else:
                print("no data from {address}".format(address=client_address))

        finally:
            connection.close()
