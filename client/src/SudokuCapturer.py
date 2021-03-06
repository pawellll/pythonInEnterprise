import cv2
import logging
import sys
from SudokuDetector import SudokuDetector


class SudokuCapturer:
    """
    Class which take capture photos from default camera
    and recognise if there's sudoku on photo
    """

    def __init__(self):
        """C-tor, opens camera"""
        camera_port = 0  # 0 is for default camera
        self._camera_capturer = cv2.VideoCapture(camera_port)
        self._dectector = SudokuDetector()
        logging.info("Camera opened")

    def __del__(self):
        """D-tor, responsible for releasing camera"""
        logging.info("Releasing camera")
        self._camera_capturer.release()

    def capture_sudoku(self):
        """
            takes photo from default camera of computer and checks if there's sudoku on it
            if no sudoku was found it returns None
            if sudoku was found returns image of sudoku
        """
        if self._camera_capturer.isOpened():
            logging.info("Capturing photo")
            _, image = self._camera_capturer.read()
            cv2.waitKey(100)  # used to slow down
            return self._dectector.detect_sudoku(image)
        else:
            logging.info("Couldn't open camera")
            sys.exit(0)

