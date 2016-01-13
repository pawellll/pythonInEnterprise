import socket
import sys
import SudokuOcr
from Solver import Solver
import cv2
import pickle


class Server:
    def __init__(self, addr='localhost', port=5008, datasize=1024):
        self._data_size = int(datasize)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (addr, int(port))
        print >> sys.stderr, 'Starting server at %s:%s' % server_address
        self.sock.bind(server_address)

    def listen(self):
        self.sock.listen(5)
        while True:
            print >> sys.stderr, 'Waiting for connection ... '
            connection, client_address = self.sock.accept()
            try:
                print >> sys.stderr, 'Connection from ', client_address
                fname = 'imageToProcess.jpg'
                fp = open(fname, 'wb+')
                while True:
                    data = connection.recv(self._data_size)
                    data = str(data)
                    if data == 'EOF':
                        fp.close()
                        break
                    else:
                        fp.write(data)
                image = cv2.imread("imageToProcess.jpg")
                result = self._process(image)
                connection.send(pickle.dumps(result))
                connection.close()
            finally:
                print('Closed via server')

    def _process(self, image):
        reader = SudokuOcr.OCRmodelClass()
        read_grid = reader.orc(image).tolist()
        solved_grid = self._solve_sudoku(read_grid)
        return reader.original.tolist(), solved_grid

    @staticmethod
    def _solve_sudoku(read_grid):
        solver = Solver(read_grid)
        if solver.solve():
            return solver.sudoku_grid
        else:
            return None
