import sys
import math


class Solver():
    def __init__(self, grid = None):
        self.sudoku_grid = [[0 for x in range(9)] for x in range(9)]
        if grid:
            self.sudoku_grid = grid

    def validate_row(self, r, c):
        value = self.sudoku_grid[r][c]
        for _c in range(9):
            if _c != c and self.sudoku_grid[r][_c] == value:
                return False
        return True

    def validate_column(self, r, c):
        value = self.sudoku_grid[r][c]
        for _r in range(9):
            if _r != r and self.sudoku_grid[_r][c] == value:
                return False
        return True

    def validate_box(self, r, c):
        value = self.sudoku_grid[r][c]
        box_r = int(math.floor(r / 3))
        box_c = int(math.floor(c / 3))
        for _r in range(box_r * 3, box_r * 3 + 3):
            for _c in range(box_c * 3, box_c * 3 + 3):
                if _c != c and _r != r and self.sudoku_grid[_r][_c] == value:
                    return False
        return True

    def backtrack(self, r, c):
        c += 1
        if c > 8:
            c = 0
            r += 1
            if r > 8:
                return True

        if self.sudoku_grid[r][c] != 0:
            if not (self.validate_row(r, c) and self.validate_column(r, c) and self.validate_box(r, c)):
                return False
            return self.backtrack(r, c)
        else:
            for x in range(1, 10):
                self.sudoku_grid[r][c] = x
                if self.validate_row(r, c) and self.validate_column(r, c) and self.validate_box(r, c):
                    if (self.backtrack(r, c)):
                        return True
            self.sudoku_grid[r][c] = 0
            return False

    def solve(self):
        for r in range(9):
            for c in range(9):
                if self.sudoku_grid[r][c] != 0 and not self.validate_row(r, c) and self.validate_column(r,c) and self.validate_box(r, c):
                    return False
        return self.backtrack(0, -1)

    def print_grid(self):
        for row in self.sudoku_grid:
            print(row)



if __name__ == "__main__":
    grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    sudoku = Solver(grid);
    if sudoku.solve():
        sudoku.print_grid()
    else:
        print("Brak rozwiazania")
