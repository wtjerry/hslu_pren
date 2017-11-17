import time
from concurrent.futures import ThreadPoolExecutor


def blocking_count_down(text):
    for i in range(0, 5):
        print("{0}: {1}".format(text, i))
        time.sleep(0.25)


class ABC(object):
    def __init__(self):
        self.__executor = ThreadPoolExecutor(max_workers=1)

    def submit(self, text):
        self.__executor.submit(blocking_count_down, text)
        return text

    def stop(self):
        self.__executor.stop()


a = ABC()
print(a.submit("a"))
print(a.submit("b"))
print(a.submit("c"))
blocking_count_down("d")