import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.dirname(__file__))

from controlling.Controller import Controller
from networking.CommandFactory import CommandFactory
from networking.IpProvider import get_wlan_ip_address
from networking.SocketServer import SocketServer


def _startSocketServer():
    ip = get_wlan_ip_address()
    print("starting socket server")
    SocketServer(address=ip).start()


def _blocking_count(text):
    for i in range(0, 5000000):
        print("{0}: {1}".format(text, i))


if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=2)
    controller = Controller(executor)
    CommandFactory.setup_start(controller.switchToStart)
    executor.submit(_startSocketServer)
    executor.submit(_blocking_count, "hello")
