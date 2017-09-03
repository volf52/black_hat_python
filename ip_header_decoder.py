#!/usr/bin/env python
"""

@author : 'Muhammad Arslan <rslnrkmt2552@gmail.com>'

"""

import os
import threading
import time
from netaddr import IPNetwork, IPAddress
import socket
import struct
from ctypes import *
from get_ip import get_lan_ip

host = get_lan_ip()
subnet = '.'.join(host.split('.')[:2]) + '.86.0/24'

magic_message = "VOLF"

def udp_sender(host, subnet, magic_message):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = filter(lambda x: x != host, IPNetwork(subnet))
    for ip in addr:
        print "Trying %s" % ip
        try:
            sender.sendto(magic_message, ("%s" % ip, 65212))
        except:
            pass

class IP(Structure):
    _fields_ = [
        ("ihl",             c_ubyte, 4),
        ("version",         c_ubyte, 4),
        ("tos",             c_ubyte),
        ("len",             c_ushort),
        ("id",              c_ushort),
        ("offset",          c_ushort),
        ("ttl",             c_ubyte),
        ("protocol_num",    c_ubyte),
        ("sum",             c_ushort),
        ("src",             c_uint32),
        ("dst",             c_uint32)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):

        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        self.src_addr = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_addr = socket.inet_ntoa(struct.pack("@I", self.dst))

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):
    _fields_ = [
        ("type",        c_ubyte),
        ("code",        c_ubyte),
        ("checksum",    c_ushort),
        ("unused",      c_ushort),
        ("next_hop_mtu",c_ushort)
    ]

    def __new__(cls, socket_buffer):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass


if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)


t = threading.Thread(target=udp_sender, args=(host, subnet, magic_message))
t.start()


try:
    while True:
        raw_buffer = sniffer.recvfrom(65565)[0]
        ip_header = IP(raw_buffer[:20])
        print "Protocol: %s\t%s -> %s" % (ip_header.protocol, ip_header.src_addr, ip_header.dst_addr)

        if ip_header.protocol == "ICMP":

            offset = ip_header.ihl * 4
            buf = raw_buffer[offset: offset + sizeof(ICMP)]
            icmp_header = ICMP(buf)
            print "ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code)

            if icmp_header.code == 3 and icmp_header.type == 3:
                if IPAddress(ip_header.src_addr) in IPNetwork(subnet):
                    if raw_buffer[len(raw_buffer) - len(magic_message):] == magic_message:
                        print "Host Up: %s" % ip_header.src_addr


except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


