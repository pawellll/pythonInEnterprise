import logging
import os
import SudokuGui
import SudokuOcr
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
            image = self._sudoku_capturer.capture_sudoku()
            if image is None:
                logging.info("Sudoku hasn't been found on image. Continuing")
            else:
                logging.info("Found sudoku on image")
                # ############################################
                # ################ TODO:send image with sudoku to server and wait for response
                reader = SudokuOcr.OCRmodelClass()
                read_grid = reader.orc(image).tolist()
                solved_grid = self._solve_sudoku(read_grid)
                # ################
                # ############################################
                if solved_grid is not None:
                    SudokuGui.run(reader.original.tolist(), solved_grid, "Succesfully solved sudoku")
                    break

    @staticmethod
    def _solve_sudoku(read_grid):
        solver = Solver(read_grid)
        if solver.solve():
            return solver.sudoku_grid
        else:
            return None

    @staticmethod
    def _setup_logging(log_path, logging_level, logging_format):
        # remove log file if exists
        try:
            os.remove(log_path)
        except OSError:
            pass

        logging.basicConfig(filename=log_path, level=logging_level, format=logging_format)
        logging.info("Logging has been initialised")
