import socket
import sys
import time
import pickle


class Client:
    def __init__(self, addr='localhost', port=5008, datasize=1024):
        self._data_size = datasize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (addr, port)
        print >> sys.stderr, 'Connecting to %s:%s' % self.server_address
        self.sock.connect(self.server_address)
        self.sock.settimeout(10.0)
        try:
            filepath = "prepared.jpg"
            img = open(filepath, 'r+b')
            while True:
                strng = img.readline(self._data_size)
                if not strng:
                    break
                self.sock.send(str(strng))
            img.close()
            time.sleep(2)
            self.sock.send('EOF')
            print('Waiting for response: ')
            self.result = pickle.loads(self.sock.recv(self._data_size))
            print(self.result)

        finally:
            print >> sys.stderr, 'Closing socket'
            self.sock.close()
