#! /ur/bin/env python

import netfilterqueue


def process_packet(packet):
    print(packet)
    packet.drop()

#check whether /proc/sys/net/ipv4/ip_forward file is set to 1

queue = netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
queue.run()
