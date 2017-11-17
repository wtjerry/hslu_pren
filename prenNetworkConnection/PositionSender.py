import socket

from prenNetworkConnection.Encoder import Encoder

address = "localhost"
port = 12346

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((address, port))

data = Encoder().position(55, 2)
sock.sendall(data)  # the other side will receive b"000042552"
