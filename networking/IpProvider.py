import socket
import fcntl
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    p = struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    ioctl = fcntl.ioctl(s.fileno(), 0x8915, p)
    ioctl_ = ioctl[20:24]
    return socket.inet_ntoa(ioctl_)


def get_wlan_ip_address():
    return get_ip_address("wlan0")
