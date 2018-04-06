import time
from concurrent.futures import ThreadPoolExecutor


def blocking_count_down(text):
    for i in range(0, 5):
        print("{0}: {1}".format(text, i))
        time.sleep(0.25)


class ABC(object):
    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=3)

    def submit(self, text):
        self._executor.submit(blocking_count_down, text)
        return text

    def stop(self):
        self._executor.shutdown()


a = ABC()
print(a.submit("a"))
print(a.submit("b"))
print(a.submit("c"))
blocking_count_down("d")
