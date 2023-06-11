#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac_address", dest="mac_address", help="MAC address")
    (options, arguments) = parser.parse_args()

    # Check for empty fields
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.mac_address:
        parser.error("[-] Please specify a mac address, use --help for more info")

    return options


def change_mac_address(interface, mac_address):
    print(f"[+] Changing MAC address for {interface} to {mac_address}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac_address(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode("utf-8"))
        if mac_address_search_result:
            return mac_address_search_result.group(0)
    except subprocess.CalledProcessError:
        print("[-] Could not read MAC address")


# Run code
options = get_arguments()

change_mac_address(options.interface, options.mac_address)
current_mac_address = get_current_mac_address(options.interface)
if current_mac_address == options.mac_address:
    print(f"[+] MAC address was successfully changed to {current_mac_address}")
else:
    print("[-] MAC address did not get changed.")
