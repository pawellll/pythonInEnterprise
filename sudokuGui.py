import argparse

from Tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

BOARDS = ['debug', 'n00b', 'l33t', 'error']  # Available sudoku boards
MARGIN = 40  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH  = HEIGHT = MARGIN * 2 + SIDE * 9 # Width and height of the whole board


class SudokuError(Exception):
    """
    An application specific error.
    """
    pass




class SudokuUI(Frame):

    def __init__(self, parent, grid, message):

        Frame.__init__(self, parent)
        self.parent = parent
        self.grid = grid
        self.message = message
        self.row, self.col = -1, -1

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)


        try:
            self.__draw_puzzle()
            self.__draw_grid()

        except:
            pass
        self.__draw_message()


    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in xrange(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in xrange(9):
            for j in xrange(9):
                answer = self.grid[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2

                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill="black"
                    )


    def __draw_message(self):

        x = WIDTH /2
        y = 20
        self.canvas.create_text(
            x, y,
            text=self.message, tags="victory",
            fill="black", font=("Arial", 16)
        )





def run(grid, message):
    root = Tk()
    SudokuUI(root, grid, message)
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.mainloop()
