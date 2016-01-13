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
