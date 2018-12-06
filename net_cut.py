#! /ur/bin/env python

import netfilterqueue


def process_packet(packet):
    print("inside process_packet")
    print(packet)
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(1, process_packet)
print("queue is " + str(queue))
queue.run()
