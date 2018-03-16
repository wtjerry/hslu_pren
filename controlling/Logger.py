class Logger(object):
    def __init__(self, socket_server):
        self._socket_server = socket_server

    def major_step(self, step):
        s = "----------------------------" + "\n" \
            + step + "\n" \
            + "----------------------------" + "\n" \
            + "                            " + "\n"
        self._enqueue(s)

    def info(self, s):
        self._enqueue(s)

    def _enqueue(self, s):
        try:
            self._socket_server.queue.append(s)
        except Exception as ex:
            self._socket_server.stop()
            print(ex)
