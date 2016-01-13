import cv2
import numpy as np

WINDOW_NAME = "picture_window"
RED_COLOR = (0, 0, 255)
DETECTION_LINE_THICKNESS = 3


class SudokuDetector:
    """
        Class for detecting sudoku on image
        Variable i used to count found squares. We need to give user some time to put image in front of camera
        Because of it we process 10th found square on image in order to avoid situation of detection just half of
        sudoku while user is putting it in front of camera
    """

    def __init__(self):
        self._original_image = None
        self._gray = None
        self._thresh = None
        self._contours = None
        self.mat = np.zeros((100, 2), np.float32)
        self._i = 0

    def detect_sudoku(self, image):
        """
            Detects sudoku on image
            Returns sudoku rectangle
        """
        cv2.namedWindow(WINDOW_NAME)  # create window for displaying image
        self._original_image = image
        cv2.imwrite("original.jpg", self._original_image)

        self._preprocess()

        if self._find_biggest_square() is not None:
            if self._i > 10:
                # continue processing and return image of found sudoku
                self._perspective()
                self._warp()
                self._i = 0
                return self._output
            else:
                self._i += 1
                return None
        else:
            return None

    def _preprocess(self):
        """performs preprocessing on image"""
        # rescale image
        self._resized = self._original_image  # cv2.resize(self._original_image, (600, 600))  # rescaling not needed?
        # gray scale conversion
        self._gray = cv2.cvtColor(self._resized, cv2.COLOR_BGR2GRAY)
        # Gaussian blur
        kernel_size = (5, 5)
        self._gray = cv2.GaussianBlur(self._gray, kernel_size, 0)
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
        """puts vertices in order"""

        # [top-left, top-right, bottom-right, bottom-left]
        a = self._biggest.reshape((4, 2))
        b = np.zeros((4, 2), dtype=np.float32)

        add = a.sum(1)
        b[0] = a[np.argmin(add)]  # smallest sum
        b[2] = a[np.argmax(add)]  # largest sum

        diff = np.diff(a, axis=1)  # y-x
        b[1] = a[np.argmin(diff)]  # min diff
        b[3] = a[np.argmax(diff)]  # max diff
        self._biggest = b

    def _perspective(self):
        """change image to proper perspective"""
        c_sqrt = 10
        if self._biggest is None:
            self._biggest = [[0, 0], [640, 0], [640, 480], [0, 480]]
        tl, tr, br, bl = self._biggest[0], self._biggest[1], self._biggest[2], self._biggest[3]
        for k in range(0, 100):
            i = k % c_sqrt
            j = k / c_sqrt
            ml = [tl[0] + (bl[0] - tl[0]) / 9 * j, tl[1] + (bl[1] - tl[1]) / 9 * j]
            mr = [tr[0] + (br[0] - tr[0]) / 9 * j, tr[1] + (br[1] - tr[1]) / 9 * j]
            # self.mat[k,0] = ml[0]+(mr[0]-ml[0])/9*i
            # self.mat[k,1] = ml[1]+(mr[1]-ml[1])/9*i
            self.mat.itemset((k, 0), ml[0] + (mr[0] - ml[0]) / 9 * i)
            self.mat.itemset((k, 1), ml[1] + (mr[1] - ml[1]) / 9 * i)
        self.reshape = self.mat.reshape((c_sqrt, c_sqrt, 2))

    def _warp(self):
        """image equalising"""
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        close = cv2.morphologyEx(self._gray, cv2.MORPH_CLOSE, kernel)
        division = np.float32(self._gray) / close
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
                output[ri * 450 / (c_sqrt - 1):(ri + 1) * 450 / (c_sqrt - 1),
                ci * 450 / (c_sqrt - 1):(ci + 1) * 450 / (c_sqrt - 1)] = warp[ri * 450 / (c_sqrt - 1):(ri + 1) * 450 / (
                c_sqrt - 1), ci * 450 / (c_sqrt - 1):(ci + 1) * 450 / (c_sqrt - 1)].copy()

        self._output = output
