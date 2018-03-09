import os
import sys
from concurrent.futures import ThreadPoolExecutor

from controlling.Dummies.DummyBalancer import DummyBalancer

sys.path.append(os.path.dirname(__file__))

from controlling.DummyController import DummyController
from networking.CommandFactory import CommandFactory
# from networking.IpProvider import get_wlan_ip_address
from networking.SocketServer import SocketServer


def _startSocketServer():
    #ip = get_wlan_ip_address()
    print("starting socket server")
    #SocketServer(address=ip).start()


def _blocking_count(text):
    for i in range(0, 5000000):
        print("{0}: {1}".format(text, i))


if __name__ == '__main__':
    # Dummy Start
    controller = DummyController()
    controller.listenForStart()

    # executor = ThreadPoolExecutor(max_workers=2)
    # CommandFactory.setup_start(controller.switch_to_start)
    # controller.switch_to_start()
    # executor.submit(_startSocketServer)
    # executor.submit(_blocking_count, "hello")
