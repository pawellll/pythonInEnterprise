import socket
import sys
'''
 Logika servera: dostaje zdjecie, zapisuje je tymczasowo do pliku imageToProcess.jpg
 potem trzeba je przeprocesowac przez te wszystkie parsery sovery itd, a nastepnie zwrocic
 to co zwracaja te rzeczy (zedytowac metode ProcessImage)
'''

class Server:
    def __init__(self, addr = 'localhost', port = 5004, datasize = 1024):
        self._data_size = int(datasize)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (addr, int(port))
        print >>sys.stderr, 'Starting server at %s:%s' % server_address
        self.sock.bind(server_address)


    def listen(self):
        self.sock.listen(5)
        while True:
            print >>sys.stderr, 'Waiting for connection ... '
            connection, client_address = self.sock.accept()
            try:
                print >>sys.stderr, 'Connection from ', client_address
                fname = 'imageToProcess.jpg'
                fp = open(fname,'wb+')
                while True:
                    data = connection.recv(self._data_size)
                    data = str(data)
                    if data == 'EOF':
                        fp.close()
                        break
                    else:
                        fp.write(data)

                solved_sudoku = self.ProcessImage(fname)
                print('Processed image and received result: ' + solved_sudoku)
                connection.send('msg: ' + solved_sudoku)
                connection.close()
            finally:
                print('Closed via server')

                
    def ProcessImage(self,imageName):
        print('Procesuje sudoku: ' + imageName)
        return 'Przeprocesowano'
