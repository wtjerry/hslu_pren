import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.dirname(__file__))

from networking.CommandFactory import CommandFactory
from networking.IpProvider import get_wlan_ip_address
from networking.SocketServer import SocketServer


def _startSocketServer():
    CommandFactory.setup_start(lambda: print("yay it worked, here may be the method to start our SW"))
    ip = get_wlan_ip_address()
    print("starting socket server")
    SocketServer(address=ip).start()


def _startMasterModule():
    while True:
        print("master module is still here")
        time.sleep(3)


def blocking_count_down(text):
    for i in range(0, 5000000):
        print("{0}: {1}".format(text, i))


def start():
    executor = ThreadPoolExecutor(max_workers=2)
    executor.submit(_startSocketServer)
    executor.submit(blocking_count_down, "hello")


if __name__ == '__main__':
    start()
