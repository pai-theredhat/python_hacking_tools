#! /usr/bin/env python


import scapy.all as scapy
import optparse


def get_options():
    parser = optparse.OptionParser()
    parser.add_option("-t", dest="target", help="Enter target ip/range")
    return parser.parse_args()[0]


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def display_result(result_list):
    print("ip\t\t\tMAC\n...............................................")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_options()
scan_results = scan(options.target)
display_result(scan_results)