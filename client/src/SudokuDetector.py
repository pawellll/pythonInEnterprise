import cv2
import numpy as np

WINDOW_NAME = "picture_window"
RED_COLOR = (0, 0, 255)
DETECTION_LINE_THICKNESS = 3


class SudokuDetector:
    """
        Class for detecting sudoku on image
    """
    def __init__(self):
        self._original_image = None
        #  self._resized = None # rescaling not neeeded?
        self._gray = None
        self._thresh = None
        self._contours = None

    def detect_sudoku(self, image):
        """
            Detects sudoku on image
            Returns sudoku rectangle
        """
        cv2.namedWindow(WINDOW_NAME)  # create window for displaying image
        self._original_image = image
        self._preprocess()

        if self._find_biggest_square() is not None:
            return self._biggest, self._thresh
        else:
            return None

    def _preprocess(self):
        """performs preprocessing on image"""
        # rescale image
        self._resized = self._original_image  # cv2.resize(self._original_image, (600, 600))  # rescaling not needed?
        # gray scale conversion
        self._gray = cv2.cvtColor(self._resized, cv2.COLOR_BGR2GRAY)
        # Gaussian blur
        self._gray = cv2.GaussianBlur(self._gray, (5, 5), 0)
        # thresholding
        self._thresh = cv2.adaptiveThreshold(self._gray, 255, 1, 1, 11, 2)
        #  contours finding
        self._contours, hierarchy = cv2.findContours(self._thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def _find_biggest_square(self):
        """looks for the biggest square on the image"""
        self._biggest = None
        self.maxArea = 0
        for i in self._contours:
            area = cv2.contourArea(i)
            if area > 50000:  # 50000 is an estimated value for the kind of blob we want to evaluate
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                if area > self.maxArea and len(approx) == 4:
                    self._biggest = approx
                    self.maxArea = area
                    # best_cont = i # not used warning
        if self.maxArea > 0:
            is_closed = True
            cv2.polylines(self._original_image, [self._biggest], is_closed, RED_COLOR, DETECTION_LINE_THICKNESS)
            cv2.imshow(WINDOW_NAME, self._original_image)
            self._reorder()  # put vertices in order
            return self._biggest
        else:
            cv2.imshow(WINDOW_NAME, self._original_image)
            return None

    def _reorder(self):
        """
         puts vertices in order
        """
        # [top-left, top-right, bottom-right, bottom-left]
        a = self._biggest.reshape((4, 2))
        b = np.zeros((4,2), dtype=np.float32)

        add = a.sum(1)
        b[0] = a[np.argmin(add)]  # smallest sum
        b[2] = a[np.argmax(add)]  # largest sum

        diff = np.diff(a,axis = 1)  # y-x
        b[1] = a[np.argmin(diff)]  # min diff
        b[3] = a[np.argmax(diff)]  # max diff
        self._biggest = b
