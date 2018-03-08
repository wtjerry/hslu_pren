class StartCommand(object):
    def __init__(self, start_func):
        self._start_func = start_func

    def execute(self):
        self._start_func()
