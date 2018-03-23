class Logger(object):
    def __init__(self, connection_handler):
        self._connection_handler = connection_handler

    def major_step(self, step):
        s = "\n" \
            + "----------------------------" + "\n" \
            + step + "\n" \
            + "----------------------------" + "\n" \
            + "                            " + "\n"
        self._enqueue(s)

    def info(self, s):
        self._enqueue(s)

    def _enqueue(self, s):
        try:
            self._connection_handler.queue.append(s)
        except Exception as ex:
            self._connection_handler.stop()
            print(ex)
