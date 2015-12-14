import math


class Solver(object):
    def __init__(self, grid=None):
        self.sudoku_grid = [[0 for x in range(9)] for x in range(9)]
        self.size = len(grid) if grid else 9
        self.box_size = int(math.sqrt(self.size))
        if grid:
            self.sudoku_grid = grid

    def _validate_row(self, r, c):
        value = self.sudoku_grid[r][c]
        for _c in range(self.size):
            if _c != c and self.sudoku_grid[r][_c] == value:
                return False
        return True

    def _validate_column(self, r, c):
        value = self.sudoku_grid[r][c]
        for _r in range(self.size):
            if _r != r and self.sudoku_grid[_r][c] == value:
                return False
        return True

    def _validate_box(self, r, c):
        value = self.sudoku_grid[r][c]
        box_r = int(math.floor(r / self.box_size))
        box_c = int(math.floor(c / self.box_size))
        for _r in range(box_r * self.box_size, box_r * self.box_size + self.box_size):
            for _c in range(box_c * self.box_size, box_c * self.box_size + self.box_size):
                if _c != c and _r != r and self.sudoku_grid[_r][_c] == value:
                    return False
        return True

    def _backtrack(self, r, c):
        c += 1
        if c > self.size - 1:
            c = 0
            r += 1
            if r > self.size -1:
                return True

        if self.sudoku_grid[r][c] != 0:
            if not (self._validate_row(r, c) and self._validate_column(r, c) and self._validate_box(r, c)):
                return False
            return self._backtrack(r, c)
        else:
            for x in range(1, self.size + 1):
                self.sudoku_grid[r][c] = x
                if self._validate_row(r, c) and self._validate_column(r, c) and self._validate_box(r, c):
                    if (self._backtrack(r, c)):
                        return True
            self.sudoku_grid[r][c] = 0
            return False

    def solve(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.sudoku_grid[r][c] != 0 and not self._validate_row(r, c) and self._validate_column(r,
                                                                                                        c) and self._validate_box(
                        r, c):
                    return False
        return self._backtrack(0, -1)

    def print_grid(self):
        for row in self.sudoku_grid:
            print(row)



