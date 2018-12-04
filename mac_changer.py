#!/usr/bin/env python


import subprocess
import optparse
import re


def change_mac(interface, new_mac):
    print("[+] Changing MAC of " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Please enter the interface ")
    parser.add_option("-m", "--mac", dest="new_mac", help="Please enter the MAC ")
    options = parser.parse_args()[0]
    if not options.interface:
        print("[-] Please enter interface . For more info use --help")
        exit()
    if not options.new_mac:
        print("[-] Please enter interface . For more info use --help")
        exit()
    return options


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if not mac_address_search_result:
        print("[-] Couldn't retrieve mac address")
    else:
        return mac_address_search_result.group(0)


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] MAC address changed to " + current_mac)
else:
    print("[-] MAC address NOT changed ")









