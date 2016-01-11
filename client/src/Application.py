import logging
import os
from SudokuCapturer import SudokuCapturer
from Solver import Solver

LOGGING_PATH = "solver.log"
LOGGING_FORMAT = "%(asctime)s %(levelname)s %(message)s "
LOGGING_LEVEL = logging.DEBUG


class Application:
    def __init__(self):
        self._setup_logging(LOGGING_PATH, LOGGING_LEVEL, LOGGING_FORMAT)
        self._sudoku_capturer = SudokuCapturer()

    def run(self):
        logging.info("Stat appliction")
        while True:
            if self._sudoku_capturer.capture_sudoku() is None:
                pass
            else:
                pass
                # send image with sudoku to server and wait for response

                read_grid = None

                if Solver(read_grid).solve():
                    message = "Sudoku completed"
                else:
                    message = "Uabled to solve sudoku"

    @staticmethod
    def _setup_logging(log_path, logging_level, logging_format):
        # remove log file if exists
        try:
            os.remove(log_path)
        except OSError:
            pass

        logging.basicConfig(filename=log_path, level=logging_level, format=logging_format)
        logging.info("Logging has been initialised")
