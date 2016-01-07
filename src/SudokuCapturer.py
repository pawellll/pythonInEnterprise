import cv2
import numpy as np


class SudokuCapturer:
    def __init__(self):
        camera_port = 0  # 0 is for default camera
        self._camera_capturer = cv2.VideoCapture()

    def capture_sudoku(self):
        if self._camera_capturer.isOpened():
            pass

