import socket
import sys
import time

''' 
    Logika klienta:
        musi dostac sciezke do zrobionego zdjecia, wysyla na server cale zdjecie
        w odpowiedzi dostaje to, co zwraca solver w formie ciagu danych
        do dopiecia przez Pawla

        do ustawienia dynamicznie zmienna filepath w zaleznosci gdzie to zdjecie bedzie
'''


class Client:
    def __init__(self, addr='localhost', port=5004, datasize=1024):
        self._data_size = datasize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (addr, port)
        print >> sys.stderr, 'Connecting to %s:%s' % self.server_address
        self.sock.connect(self.server_address)
        self.sock.settimeout(10.0)
        try:
            filepath = '../resources/good2.jpg'
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
            _result = self.sock.recv(self._data_size)
            print(_result)

        finally:
            print >> sys.stderr, 'Closing socket'
            self.sock.close()
