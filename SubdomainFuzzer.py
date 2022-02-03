# Subdomain Fuzzer
#
# 0x29a

import io, requests, sys, threading
from queue import Queue

domain = input('Enter Domain: ')
wordlist = input('Enter Wordlist Filename: ')

WaitingRoom = Queue()

def connect(url):
    try:
        requests.get(url)
        return True
    except requests.ConnectionError:
        return False

def getUrl():
    with open(wordlist, 'r') as file:
        line = file.readline()
        cnt = 0
        while line:
            url = ("https://{}.{}".format(line.strip(),domain))
            WaitingRoom.put(url)
            line = file.readline()
            cnt += 1

def daemon():
    while not WaitingRoom.empty():
        url = WaitingRoom.get()
        if connect(url):
            print("{} Exists".format(url))
        else:
            print("{} Does Not Exist".format(url))

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

scan(100)
