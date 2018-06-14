#!/usr/bin/env python3
from os import path
from re import compile, findall
from subprocess import Popen, PIPE
from colorama import init, Fore, Back, Style
init(autoreset=True)


# http://www.macdrifter.com/2011/12/python-and-the-mac-clipboard.html
def get_clipboard_data():
    p = Popen(['pbpaste'], stdout=PIPE)
    p.wait()
    data = str(p.stdout.read())
    return data


def check(mac):
    file_content = open(current_path, "r", encoding='utf-8',
                        errors='ignore').readlines()

    for line in file_content:
        # Strip and split the line: <device_name>, <MAC_address>
        device_name, mac_address = line.strip().split(',')
        mac_address = mac_address.replace(' ', '')

        if mac_address.lower() == mac.lower():
            print('-', mac_address, ',', Fore.GREEN + device_name + Fore.RESET)
            # return True, if not returned then the MAC isn't trusted.
            return True


def main():
    while True:
        user_input = input("Check mac address: ")
        if not user_input: continue

        if user_input in 'eE': exit()
        if user_input in 'clipboard': clipboard()

        for address in user_input.strip().replace(' ', '').split(','):
            if not check(address):
                print('-', Fore.RED + address + Fore.RESET)


def clipboard():
    clip = get_clipboard_data()

    # Regex Compiler loaded with MAC Adresses pattern
    reCompiler = compile(u'(?:[0-9a-fA-F]:?){12}')
    reResults = findall(reCompiler, clip)

    # If there's any addresses check for them.
    if reResults:
        for i in reResults:
            if ':' not in i: continue

            # Check if the address is unknown
            if not check(i):
                print('-', Fore.RED + i + Fore.RESET)

try:
    current_path = path.dirname(path.realpath(__file__)) + "/maclist.txt"
    if not path.exists(current_path):
        open(current_path, "w").close()
    clipboard()
    main()

except KeyboardInterrupt:
    print()
    exit()
