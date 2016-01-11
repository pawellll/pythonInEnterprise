import socket
import sys

''' 
    Logika klienta:
        musi dostac sciezke do zrobionego zdjecia, wysyla na server cale zdjecie
        w odpowiedzi dostaje to, co zwraca solver w formie ciagu danych
        do dopiecia przez Pawla

        do ustawienia dynamicznie zmienna filepath w zaleznosci gdzie to zdjecie bedzie
'''

class Client:
    def __init__(self, addr = 'localhost', port = 5004, datasize = 1024):
        self._data_size = datasize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (addr, port)
        print >>sys.stderr, 'polaczenie z %s na porcie %s' % self.server_address
        self.sock.connect(self.server_address)
        self.sock.settimeout(10.0)
        try:
            filepath = '../resources/good2.jpg'
            img = open(filepath,'r')
            while True:
                strng = img.readline(512)
                if not strng:
                    break
                self.sock.send(strng)
            img.close()

            print('Otrzymano z servera odpowiedz: ')
            print( self.sock.recv(16))


        finally:
            print >>sys.stderr, 'zamykam gniazdo'
            self.sock.close()