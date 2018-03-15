import os
import socket
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    p = struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    import fcntl
    ioctl = fcntl.ioctl(s.fileno(), 0x8915, p)
    ioctl_ = ioctl[20:24]
    return socket.inet_ntoa(ioctl_)


def get_wlan_ip_address():
    if os.name == "nt":
        return "127.0.0.1"
    return get_ip_address("wlan0")
