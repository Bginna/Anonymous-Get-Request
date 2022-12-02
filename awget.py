###############################################
# Group Name  : XXXXXX

# Member1 Name: XXXXXX
# Member1 SIS ID: XXXXXX
# Member1 Login ID: XXXXXX

# Member2 Name: XXXXXX
# Member2 SIS ID: XXXXXX
# Member2 Login ID: XXXXXX
###############################################

import sys
import getopt
import random
import socket

#Main Function
if __name__ == "__main__":
    
    argv = sys.argv[1:]
    if(len(argv) == 0):
        print("Error, no URL Specified")
        exit()

    #Set Chainfile
    if('-c' in argv):
        chainfile = argv[argv.index('-c') + 1]
        print(chainfile)
    else:
        chainfile = "chaingang.txt"

    #Set URL
    URL = argv[0]

    f = open(chainfile, "r")
    if(f.readable()):
        ipList = f.readlines()

        #Get rid of lists
        length = ipList.pop(0)

        #Get rid of newlines
        for index in range(len(ipList) - 1):
            ipList[index] = ipList[index][:-1]

        #Random IP first
        index = random.randint(1, int(length) - 1)
        firstStone = ipList[index]
        x = firstStone.split(" ")
        firstIP = x[0]
        firstPort = x[1]
        
        #Remove first IP from list to avoid loops
        ipList.pop(index)
    else:
        print("Error: File Unreadable")
        exit()

    #Make tuple to encode
    newipList = []
    for index in ipList:
        split = index.split()
        index = (split[0], int(split[1]))
        newipList.append(index)

    ipList = newipList
    listToEncode = [URL, ipList]

    #encodedTuple = tupleToEncode.toString().encode()
    #print(encodedTuple)
    encodedList = str(listToEncode).encode()
    print(encodedList)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(firstIP, firstPort)
    clientSocket.send(encodedList)

    


    f.close()
