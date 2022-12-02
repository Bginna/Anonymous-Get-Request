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
import argparse
import sys
import socket
import random
import requests

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
        self.url = None
        self.ss_list = None

    def intermediate(self):
        print('Intermediate SS')
        index = random.randint(0, len(self.ss_list) - 1)
        newIP = ss_list[index][0]
        newPort = ss_list[index][1]
        ss_list.pop(index)
        SSSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SSSocket.connect((newIP, int(newPort)))
        SSSocket.send(encodedList)
        
    def download_file(url):
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    def send(file):
        with open(file, 'rb') as f:
            chunk = f.read(1024)
            while chunk:
                self.conn.sendall(chunk)
                chunk = f.read(1024)

    '''
    use wget to retrieve file from URL
    transmit the file back to the previous SS
    shut down connection
    erase the local copy of the file
    '''
    def end(self):
        print('End SS')
        filename = download_file(self.url)
        self.send(filename)

    def run(self):
        print('--Running child thread--')
        print('URL: ', self.url)
        print('SS List: ', self.ss_list)
        if not self.ss_list:
            self.end()
        else:
            self.intermediate()

def listen(port):
    host = socket.gethostname()
    print(f'stepping stone listening on {host}:{port}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host,int(port)))
        s.listen()
        while True:

            conn, addr = s.accept()
            with conn:
                print(f'Recieved connection from {addr}')
                child = ChildThread(conn)
                child.start()

'''
--Main Thread--
get listen port from optional arg
print hostname and port that we are listening on
create server_socket and bind
loop and listen for incoming connections
accept connections and spawn thread for each new connection
'''
def main():
    parser = argparse.ArgumentParser(
        prog = 'ss.py',
        description = 'Intermediate stepping stone for anonymous web get'
    )
    parser.add_argument('-p', '--port', default=2100)
    args = parser.parse_args()
    listen(args.port)

if __name__ == "__main__":
    main()