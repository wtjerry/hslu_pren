from prenNetworkConnection.CommandData import CommandData


class NetworkStreamDecoder(object):
    def read(self, stream):
        with stream as s:
            length = int(s.read(5))
            command_id = int(s.read(1).decode("utf8"))
            parameter = s.read(length-1).decode("utf8")
            return CommandData(command_id, parameter)
