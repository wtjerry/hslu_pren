import os
import sys
from multiprocessing import Process
from time import sleep

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from networking.IpProvider import get_wlan_ip_address
from networking.SocketServer import SocketServer


def _startSocketServer():
    ip = get_wlan_ip_address()
    print("starting socket server")
    SocketServer(address=ip).start()


def _startMasterModule():
    while True:
        print("master module is still here")
        sleep(3)


def start():
    masterModuleProcess = Process(target=_startMasterModule, args=())
    socketServerProcess = Process(target=_startSocketServer, args=())
    masterModuleProcess.start()
    socketServerProcess.start()
    masterModuleProcess.join()
    socketServerProcess.join()


if __name__ == '__main__':
    start()
