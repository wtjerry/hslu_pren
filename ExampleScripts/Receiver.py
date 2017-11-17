import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("localhost", 12346))
sock.listen(1)


print("waiting for a connection")
try:
    connection, client_address = sock.accept()
    print(connection.recv(1024))
except KeyboardInterrupt:
    sock.close()
