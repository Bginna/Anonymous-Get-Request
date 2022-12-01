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

#Main Function
if __name__ == "__main__":
    
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "c:")
    except:
        print("Error")

    #Set URL
    URL = argv[0]

    #Set Chain File
    for opt, arg in opts:
        if opt in ['-c']:
            chainfile = "chaingang.txt"
        else:
            chainfile = "chaingang.txt"

    f = open("chaingang.txt", "r")
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
        return
    print(URL)
    print(ipList)
    print(firstIP)
    print(firstPort)
        
    f.close()
