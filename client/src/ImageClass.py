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

    def virtualImage(self, readGrid, solvedGrid):
        self.captured = cv2.imread("original.jpg")
        current = np.asarray(solvedGrid)
        # output known sudoku values to the real image
        j = 0
        tsize = (math.sqrt(self.maxArea)) / 400
        w = int(20 * tsize)
        h = int(25 * tsize)
        for i in range(100):
            # x = int(self.mat[i][0]+8*tsize)
            # y = int(self.mat[i][1]+8*tsize)
            x = int(self.mat.item(i, 0) + 8 * tsize)
            y = int(self.mat.item(i, 1) + 8 * tsize)
            if i % 10 != 9 and i / 10 != 9:
                yc = j % 9
                xc = j / 9
                j += 1
                # if puzzle.original[xc,yc]==0 and puzzle.current[xc,yc]!=0:
                if current[xc, yc] != readGrid[xc, yc]:
                    string = str(current[xc, yc])
                    cv2.putText(self.captured, string, (x + w / 4, y + h), 0, tsize, (0, 0, 255), 2)
        small = cv2.resize(self.captured, (600, 600))
        cv2.imwrite('virtual.jpg', small)
        # cv2.imshow('sudoku',self.captured)
