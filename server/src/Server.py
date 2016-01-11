import socket
import sys
'''
 Logika servera: dostaje zdjecie, zapisuje je tymczasowo do pliku imageToProcess.jpg
 potem trzeba je przeprocesowac przez te wszystkie parsery sovery itd, a nastepnie zwrocic
 to co zwracaja te rzeczy
'''

class Server:
    def __init__(self, addr = 'localhost', port = 5004, datasize = 1024):
        self._data_size = int(datasize)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (addr, int(port))
        print >>sys.stderr, 'startuje server %s na porcie %s' % server_address
        self.sock.bind(server_address)


    def listen(self):
        self.sock.listen(5)
        while True:
            print >>sys.stderr, 'czekam na polaczenie od klienta'
            connection, client_address = self.sock.accept()
            try:
            	n = 0
                print >>sys.stderr, 'polaczenie z: ', client_address
                fname = 'imageToProcess.jpg'
                fp = open(fname,'w+')
                while True:
                    data = connection.recv(self._data_size)
                    n =  n + 1
                    print(str(n) + ': data')
                    if data is None:
                    	print('not data')
                    	fp.close()
                        solved_sudoku = self.ProcessImage(fname)
                        connection.send('msg: ' + solved_sudoku)
                        break
                    fp.write(data)
                fp.close()


                print('P')
            finally:
                connection.close()
                
    def ProcessImage(self,imageName):
    	print('Procesuje sudoku: ' + imageName)
    	return 'Przeprocesowano'
