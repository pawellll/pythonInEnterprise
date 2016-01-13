from Tkinter import *


class SudokuUI(Frame):
    def __init__(self, parent, read_grid, solved_grid, message):
        Frame.__init__(self, parent)
        self.parent = parent
        self.readGrid = read_grid
        self.solvedGrid = solved_grid
        self.message = message
        self.row, self.col = -1, -1
        self.MARGIN = 60  # Pixels around the board
        self.SIDE = 60  # Width of every board cell.
        self.WIDTH = self.HEIGHT = self.MARGIN * 2 + self.SIDE * 9

        self.view = True
        self._init_ui()

    def callback(self):
        self.view = False

    def _init_ui(self):
        self.parent.title("Sudoku")
        self._set_menu()
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=self.WIDTH,
                             height=self.HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        b = Button(self, text="Przelacz widok", command=self.callback)
        b.pack()

        if self.view:
            self._draw_puzzle()
            self._draw_grid()

        self._draw_message()

    def _quit_function(self):
        self.parent.destroy()

    def _set_menu(self):
        menubar = Menu(self.parent)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self._quit_function)

        menubar.add_cascade(label="File", menu=file_menu)
        self.parent.config(menu=menubar)

    def _draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in xrange(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = self.MARGIN + i * self.SIDE
            y0 = self.MARGIN
            x1 = self.MARGIN + i * self.SIDE
            y1 = self.HEIGHT - self.MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = self.MARGIN
            y0 = self.MARGIN + i * self.SIDE
            x1 = self.WIDTH - self.MARGIN
            y1 = self.MARGIN + i * self.SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def _draw_puzzle(self):
        self.canvas.delete("numbers")

        for i in xrange(9):
            for j in xrange(9):
                if self.readGrid[i][j] == self.solvedGrid[i][j]:
                    text_color = 'green'
                else:
                    text_color = 'red'
                answer = self.solvedGrid[i][j]
                if answer != 0:
                    x = self.MARGIN + j * self.SIDE + self.SIDE / 2
                    y = self.MARGIN + i * self.SIDE + self.SIDE / 2

                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=text_color,
                        font=("Arial", 18)
                    )

    def _draw_message(self):
        x = self.WIDTH / 2
        y = 20
        self.canvas.create_text(
            x, y,
            text=self.message, tags="victory",
            fill="black", font=("Arial", 16)
        )


def run(read_grid, solved_grid, message):
    root = Tk()
    sudoku_ui = SudokuUI(root, read_grid, solved_grid, message)
    root.geometry("%dx%d" % (sudoku_ui.WIDTH, sudoku_ui.HEIGHT))
    root.mainloop()
