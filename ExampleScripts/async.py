import time
from concurrent.futures import ThreadPoolExecutor


def blocking_count_down(text):
    for i in range(0, 5):
        print("{0}: {1}".format(text, i))
        time.sleep(1)


class ABC(object):
    def __init__(self):
        self.__executor = ThreadPoolExecutor(max_workers=1)

    def submit(self, text):
        self.__executor.submit(blocking_count_down(text))

    def stop(self):
        self.__executor.stop()


a = ABC()
a.submit("a")
a.submit("b")
a.submit("c")
