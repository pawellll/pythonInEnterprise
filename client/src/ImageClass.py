import cv2
import numpy as np
import math
import copy
import sys


class ImageClass:
    def __init__(self):
        # przeechwycony obraz
        self.captured = []
        # w skali szarosci
        self.gray = []
        # po progowaniu
        self.thresh = []
        # informacje na temat konturow
        self.contours = []
        # zawiera cztery punkty krawedzi najwiekszyego kwadratu
        self.biggest = None;
        # powierzchnia najwiekszego kwadratu
        self.maxArea = 0
        # .output is an image resulting from the warp() method
        self.output = []
        self.outputBackup = []
        self.outputGray = []
        # .mat is a matrix of 100 points found using a simple gridding algorithm
        # based on the four corner points from .biggest
        self.mat = np.zeros((100, 2), np.float32)
        # .reshape is a reshaping of .mat
        self.reshape = np.zeros((100, 2), np.float32)

    def imagePreprocessing(self):
        self.__initialPreprocessing()
        self.__findBiggestSquare()
        self.__perspective()
        self.__warp()

    def __initialPreprocessing(self):
        # konwersja do skali szarosci
        self.gray = cv2.cvtColor(self.captured, cv2.COLOR_BGR2GRAY)
        # rozmycie Gaussa
        self.gray = cv2.GaussianBlur(self.gray, (5, 5), 0)
        # progoowanie
        self.thresh = cv2.adaptiveThreshold(self.gray, 255, 1, 1, 11, 2)
        # szukanie konturow
        self.contours, hierarchy = cv2.findContours(self.thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def __findBiggestSquare(self):
        # wyszukiwanie najwiekszego kwadratu
        self.biggest = None
        self.maxArea = 0
        for i in self.contours:
            area = cv2.contourArea(i)
            if area > 50000:
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                if area > self.maxArea and len(approx) == 4:
                    self.biggest = approx
                    self.maxArea = area
                    best_cont = i
        if self.maxArea > 0:
            cv2.polylines(self.captured, [self.biggest], True, (0, 0, 255), 3)
            self.__reorder()  # uloz wierzcholki w kolejnosci
        else:
            print "No sudoku puzzle detected!"

        cv2.imwrite('img/capturer.jpg', self.captured)

    def __reorder(self):
        # segreguj wierzcholki
        # [top-left, top-right, bottom-right, bottom-left]
        a = self.biggest.reshape((4, 2))
        b = np.zeros((4, 2), dtype=np.float32)

        add = a.sum(1)
        b[0] = a[np.argmin(add)]  # smallest sum
        b[2] = a[np.argmax(add)]  # largest sum

        diff = np.diff(a, axis=1)  # y-x
        b[1] = a[np.argmin(diff)]  # min diff
        b[3] = a[np.argmax(diff)]  # max diff
        self.biggest = b

    def __perspective(self):
        # stworz siatke 100 punktow uzywajac algorytmu
        # topLeft-topRight-bottomRight-bottomLeft = "biggest"
        b = np.zeros((100, 2), dtype=np.float32)
        c_sqrt = 10
        if self.biggest == None:
            self.biggest = [[0, 0], [640, 0], [640, 480], [0, 480]]
        tl, tr, br, bl = self.biggest[0], self.biggest[1], self.biggest[2], self.biggest[3]
        for k in range(0, 100):
            i = k % c_sqrt
            j = k / c_sqrt
            ml = [tl[0] + (bl[0] - tl[0]) / 9 * j, tl[1] + (bl[1] - tl[1]) / 9 * j]
            mr = [tr[0] + (br[0] - tr[0]) / 9 * j, tr[1] + (br[1] - tr[1]) / 9 * j]
            ##            self.mat[k,0] = ml[0]+(mr[0]-ml[0])/9*i
            ##            self.mat[k,1] = ml[1]+(mr[1]-ml[1])/9*i
            self.mat.itemset((k, 0), ml[0] + (mr[0] - ml[0]) / 9 * i)
            self.mat.itemset((k, 1), ml[1] + (mr[1] - ml[1]) / 9 * i)
        self.reshape = self.mat.reshape((c_sqrt, c_sqrt, 2))

    def __warp(self):
        # wyrownywanie obraz
        mask = np.zeros((self.gray.shape), np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        close = cv2.morphologyEx(self.gray, cv2.MORPH_CLOSE, kernel)
        division = np.float32(self.gray) / (close)
        result = np.uint8(cv2.normalize(division, division, 0, 255, cv2.NORM_MINMAX))
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        output = np.zeros((450, 450, 3), np.uint8)
        c_sqrt = 10
        for i, j in enumerate(self.mat):
            ri = i / c_sqrt
            ci = i % c_sqrt
            if ci != c_sqrt - 1 and ri != c_sqrt - 1:
                source = self.reshape[ri:ri + 2, ci:ci + 2, :].reshape((4, 2))
                dest = np.array([[ci * 450 / (c_sqrt - 1), ri * 450 / (c_sqrt - 1)], [(ci + 1) * 450 / (c_sqrt - 1),
                                                                                      ri * 450 / (c_sqrt - 1)],
                                 [ci * 450 / (c_sqrt - 1), (ri + 1) * 450 / (c_sqrt - 1)],
                                 [(ci + 1) * 450 / (c_sqrt - 1), (ri + 1) * 450 / (c_sqrt - 1)]], np.float32)
                trans = cv2.getPerspectiveTransform(source, dest)
                warp = cv2.warpPerspective(result, trans, (450, 450))
                output[ri * 450 / (c_sqrt - 1):(ri + 1) * 450 / (c_sqrt - 1), ci * 450 / (c_sqrt - 1):(ci + 1) * 450 /
                                                                                                      (
                                                                                                      c_sqrt - 1)] = warp[
                                                                                                                     ri * 450 / (
                                                                                                                     c_sqrt - 1):(
                                                                                                                                 ri + 1) * 450 / (
                                                                                                                                 c_sqrt - 1),
                                                                                                                     ci * 450 / (
                                                                                                                     c_sqrt - 1):(
                                                                                                                                 ci + 1) * 450 / (
                                                                                                                                 c_sqrt - 1)].copy()
        output_backup = np.copy(output)
        # cv2.imshow('output',output)
        cv2.imwrite('img/original.jpg', output)
        key = cv2.waitKey(1)
        self.output = output
        self.outputBackup = output_backup

    def virtualImage(self, readGrid, solvedGrid):
        current = np.asarray(solvedGrid)
        # output known sudoku values to the real image
        j = 0
        tsize = (math.sqrt(self.maxArea)) / 400
        w = int(20 * tsize)
        h = int(25 * tsize)
        for i in range(100):
            ##            x = int(self.mat[i][0]+8*tsize)
            ##            y = int(self.mat[i][1]+8*tsize)
            x = int(self.mat.item(i, 0) + 8 * tsize)
            y = int(self.mat.item(i, 1) + 8 * tsize)
            if i % 10 != 9 and i / 10 != 9:
                yc = j % 9
                xc = j / 9
                j += 1
                # if puzzle.original[xc,yc]==0 and puzzle.current[xc,yc]!=0:
                if (current[xc, yc] != readGrid[xc, yc]):
                    string = str(current[xc, yc])
                    cv2.putText(self.captured, string, (x + w / 4, y + h), 0, tsize, (0, 0, 255), 2)
        small = cv2.resize(self.captured, (600, 600))
        cv2.imwrite('img/virtual.jpg', small)
        # cv2.imshow('sudoku',self.captured)
        key = cv2.waitKey(10)
        if key == 27:
            sys.exit()
