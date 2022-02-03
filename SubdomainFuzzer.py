# Python Subdomain Fuzzer
# 0x29a - 2/2/22

import io, requests, sys, threading
from queue import Queue

Domain = input('* [Enter Domain]: ')
WordList = input('* [Enter Wordlist Filename]: ')

WaitingRoom = Queue()

FoundSubdomains = []

def connect(url):
    try:
        requests.get(url)
        return True
    except requests.ConnectionError:
        return False

def getUrl():
    with open(WordList, 'r') as file:
        line = file.readline()
        cnt = 0
        while line:
            url = ("https://{}.{}".format(line.strip(),Domain))
            WaitingRoom.put(url)
            line = file.readline()
            cnt += 1

def daemon():
    while not WaitingRoom.empty():
        url = WaitingRoom.get()
        if connect(url):
            print("! [{}] Found".format(url))
            FoundSubdomains.append(url)
        else:
            pass

def scan(threads):
    getUrl()
    rThreads = []

    for x in range(threads):
        thread = threading.Thread(target=daemon)
        rThreads.append(thread)

    for thread in rThreads:
        thread.start()

    for thread in rThreads:
        thread.join()

    print('-> [Found Subdomains]: ', FoundSubdomains)

scan(100)
