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
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog = 'awget.py',
        description= 'Aanonymous web get'
    )
    parser.add_argument('URL')
    parser.add_argument('-c', '--chainfile', default='chaingang.txt')
    args = parser.parse_args()
    return args.URL, args.chainfile

def parse_filename(url):
    split = url.split('/')
    if len(split) == 1:
        return 'index.html'
    return split[-1]

def parse_chainfile(chainfile):
    ss_list = []
    with open(chainfile, 'r') as f:
        for line in f:
            line = line.strip().split(' ')
            if len(line) == 1:
                continue
            ss_list.append((line[0], line[1]))
    return ss_list

'''
get args from cmd
parse filename from URL
check that chainfile exists
find random ss
start connection to ss
send URL and ss_list to connection
wait to recieve file from connection
close connection
'''
def main():
    url, chainfile = parse_args()
    filename = parse_filename(url)
    if not os.path.isfile(chainfile):
        print("ERROR: chainfile not found")
        return
    ss_list = parse_chainfile(chainfile)
    first_ss = ss_list[random.randint(0, len(ss_list)-1)]
    
    

if __name__ == "__main__":
    main()