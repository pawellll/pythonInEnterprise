
class SudokuDetector:
    """
        Class for detecting sudoku on image
    """

    def __init__(self):
        self._original_image = None
        self._processed_image = None

    def detect_sudoku(self, image):
        """
            Detects sudoku on image
            Returns tuple (is_detected and sudoku_list)
        """
        self._original_image = image
        self._processed_image = image.copy()
        return False, list()

    def _preprocess(self):
        pass

    def _detect_biggest_rectangle(self):
        pass