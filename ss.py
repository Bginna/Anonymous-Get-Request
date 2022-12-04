###############################################
# Group Name  : XXXXXX

# Member1 Name: Billy Ginna
# Member1 SIS ID: XXXXXX
# Member1 Login ID: XXXXXX

# Member2 Name: Greyson Sequino
# Member2 SIS ID: XXXXXX
# Member2 Login ID: XXXXXX
###############################################

import threading
import argparse
import sys
import socket
import random
import requests
import ast
import os

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
class ChildThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.url = None
        self.ss_list = None

    def select_next_ss(self):
        index = random.randint(0, len(self.ss_list) - 1)
        newIP = self.ss_list[index][0]
        newPort = self.ss_list[index][1]
        print(self.ss_list)
        self.ss_list.pop(index)
        return newIP, newPort

    def encode_config(self):
        return str([self.url, self.ss_list]).encode()

    def recv_file(self, sock):
        filename = 'TEMP_' + str(hash(sock))
        with open(filename, 'wb') as f:
            chunk = sock.recv(1024)
            while chunk:
                f.write(chunk)
                chunk = sock.recv(1024)
        return filename

    def send_file(self, file):
        with open(file, 'rb') as f:
            chunk = f.read(1024)
            while chunk:
                self.conn.sendall(chunk)
                chunk = f.read(1024)
    
    def download_file(self, url):
        url = url if url.startswith('http') else ('http://' + url)
        print(url)
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'w+b') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    '''
    select random SS from list
    remove current SS from list
    send URL and SS list to the next SS
    wait until file is recieved from next SS
    transmit file to prev SS
    tear down connection
    erase local copy
    '''
    def intermediate(self):
        print('Intermediate SS')
        next_ip, next_port = self.select_next_ss()
        filename = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((next_ip,  int(next_port)))
            s.send(self.encode_config())
            print("Config Sent")
            filename = self.recv_file(s)
            print("File Received")
        self.send_file(filename)
        os.remove(filename)
        self.conn.close()

    '''
    use wget to retrieve file from URL
    transmit the file back to the previous SS
    shut down connection
    erase the local copy of the file
    '''
    def end(self):
        print('End SS')
        filename = self.download_file(self.url)
        print("File Downloaded")
        self.send_file(filename)
        os.remove(filename)
        self.conn.close()

    def resolve_request(self):
        print("resolving")
        self.data = self.conn.recv(4096).decode()
        self.data = ast.literal_eval(self.data)
        print(self.data)
        self.url = self.data[0]
        self.ss_list = self.data[1]

    def run(self):
        print('--Running child thread--')
        self.resolve_request()
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
            try:

                conn, addr = s.accept()
                print(f'Recieved connection from {addr}')
                child = ChildThread(conn)
                child.start()
            except KeyboardInterrupt:
                print("\nGoodbye")
                s.close()
                break

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