###############################################
# Group Name  : XXXXXX

# Member1 Name: XXXXXX
# Member1 SIS ID: XXXXXX
# Member1 Login ID: XXXXXX

# Member2 Name: XXXXXX
# Member2 SIS ID: XXXXXX
# Member2 Login ID: XXXXXX
###############################################

import threading
from threading import Thread
import getopt
import sys

'''
--Child Thread--
read URL and chain info
if chain list is empty:
    use wget to retrieve file from URL
    transmit the file back to the previous SS
    shut down connection
    erase the local copy of the file
else:
    select random SS from list
    remove current SS from list
    send URL and SS list to the next SS
    wait until file is recieved from next SS
    transmit file to prev SS
    tear down connection
    erase local copy
'''
class ChildThread(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn
        self.url = None # recv url
        self.ss_list = None # recv ss_list

    def intermediate(self):
        print('Intermediate SS')

    def end(self):
        print('End SS')

    def run(self):
        print('--Running child thread--')
        print('URL: ', self.url)
        print('SS List: ', self.ss_list)
        if not self.ss_list:
            self.end()
        else:
            self.intermediate()

'''
--Main Thread--
get listen port from optional arg
print hostname and port that we are listening on
create server_socket and bind
loop and listen for incoming connections
accept connections and spawn thread for each new connection
'''
def main():
    args = sys.argv[1:]
    optlist, args = getopt.getopt(args, 'c:')
    print(optlist)

if __name__ == "__main__":
    main()