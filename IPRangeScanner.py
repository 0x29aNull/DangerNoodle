# IP Range Scanner
# It's Magically Delicious
#1/26/2022

import io, os, threading, socket
from queue import Queue

# Port 135 is a default Micro$oft Windows port
# Adding or changing the port could give different results.
# I used a port scan technique rather than an IMCP ping
# as it is faster.
port = 135
host = input("IP Range (Ex. 10.1.5.): ")

# Here we see the list array in its natural habitat.
list = Queue()
upHosts = []
downHosts = []

# Outfile prints the results to a file within the same
# directory as this script. Complicated, I know.
outFile = open('results.txt', 'w')


def connect(address):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, port))
        return True
    except:
        return False

# Function to iterate over a range of numbers, Add the user input
# to the string then feed the resulting string in to the list.
# Yummy.
def getHosts():
    for i in range(1, 255):
        address = host + str(i)
        list.put(address)

# Function to take addresses from the list and give them to the
# Connect function, Then takes the results (True or False) and
# formats them to look purdy. Them purdy results are then logged.
def daemon():
    while not list.empty():
        address = list.get()
        if connect(address):
            print("{} is up".format(socket.gethostbyaddr(address)))
            upHosts.append(address)
            for i in address:
                outFile.write("{} is up".format(socket.gethostbyaddr(address)) + '\n')
        else:
            print("{} is down".format(address))
            downHosts.append(address)
            for j in address:
                outFile.write("{} is down".format(address) + '\n')

# Threading, Welcome to Flavor Country.
# The getHosts function is called to start iterating addresses
# then threads are created, 200 by default. Those threads are
# started, then joined before printing the results.
def scan(threads):
    getHosts()
    rThreads = []

    for x in range(threads):
        thread = threading.Thread(target=daemon)
        rThreads.append(thread)

    for thread in rThreads:
        thread.start()

    for thread in rThreads:
        thread.join()

    print("Online Hosts: ", upHosts)
    print("Offline Hosts: ", downHosts)
    outFile.close()


scan(200)
