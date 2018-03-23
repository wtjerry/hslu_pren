class PositionSender(object):
    def __init__(self, connection_handler):
        self._connection_handler = connection_handler

    def send(self, x, z):
        s = "new position x: '{x}' z: '{z}'\n".format(x=x, z=z)
        self._connection_handler.queue.append(s)
