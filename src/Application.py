import logging
import os
from SudokuCapturer import SudokuCapturer

LOGGING_PATH = "solver.log"
LOGGING_FORMAT = "%(asctime)s %(levelname)s %(message)s "
LOGGING_LEVEL = logging.DEBUG


class Application:
    def __init__(self):
        self._setup_logging(LOGGING_PATH, LOGGING_LEVEL, LOGGING_FORMAT)
        self._sudoku_capturer = SudokuCapturer()

    def run(self):
        while True:
            if self._sudoku_capturer.capture_sudoku():
                # solve
                pass
            else:
                # capture again
                pass

    @staticmethod
    def _setup_logging(log_path, logging_level, logging_format):
        # remove log file if exists
        try:
            os.remove(log_path)
        except OSError:
            pass

        logging.basicConfig(filename=log_path, level=logging_level, format=logging_format)
        logging.info("Logging has been initialised")
