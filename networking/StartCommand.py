class StartCommand(object):
    def __init__(self, start_func):
        self._start_func = start_func

    def execute(self):
        print("lets start")
        self._start_func()
