import argparse

from Tkinter import *
import Image, ImageTk



class SudokuError(Exception):
    """
    An application specific error.
    """
    pass



class SudokuUI(Frame):

    def __init__(self, parent, readGrid, solvedGrid, message):
        Frame.__init__(self, parent)
        self.parent = parent
        self.readGrid = readGrid
        self.solvedGrid = solvedGrid
        self.message = message
        self.row, self.col = -1, -1
        self.MARGIN = 60  # Pixels around the board
        self.SIDE = 60  # Width of every board cell.
        self.WIDTH  = self.HEIGHT = self.MARGIN * 2 + self.SIDE * 9

        self.view = True
        self.__initUI()
	
    def callback(self):
        self.view = False

    def __initUI(self):
	
        self.parent.title("Sudoku")
        self.__setMenu()
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=self.WIDTH,
                             height=self.HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        
        self.img = ImageTk.PhotoImage(Image.open("img/virtual.jpg"))
        b = Button(self, text="Przelacz widok", command=self.callback)
        b.pack()
        try:
            if self.view:
                #self.canvas.create_image(350,350, image=self.img)
                self.__draw_puzzle()
                self.__draw_grid()
        except:
            pass
        self.__draw_message()

    def __quitFunction(self):
        self.parent.destroy()

    def __classicMode(self):
        photoMode = Toplevel(self.parent)
        photoMode.title("Photo mode")
        canvas = Canvas(photoMode, width=600, height=600)
        canvas.pack()
        self.img = ImageTk.PhotoImage(Image.open("img/virtual.jpg"))
        canvas.create_image(300,300, image=self.img)
        

    def __setMenu(self):
        menubar = Menu(self.parent)
        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Exit", command=self.__quitFunction)
        viewMenu = Menu(menubar, tearoff=0)
        viewMenu.add_command(label="Photo mode", command=self.__classicMode)

        menubar.add_cascade(label = "File", menu=fileMenu)
        menubar.add_cascade(label = "View", menu=viewMenu)
        self.parent.config(menu = menubar)
    
   
    def __draw_grid(self):
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

    def __draw_puzzle(self):
        self.canvas.delete("numbers")

        for i in xrange(9):
            for j in xrange(9):
		if (self.readGrid[i][j] == self.solvedGrid[i][j]):
			textColor = 'green'
		else:
			textColor = 'red'
                answer = self.solvedGrid[i][j]
                if answer != 0:
                    x = self.MARGIN + j * self.SIDE + self.SIDE / 2
                    y = self.MARGIN + i * self.SIDE + self.SIDE / 2

                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=textColor,
			font=("Arial", 18)
                    )


    def __draw_message(self):
        x = self.WIDTH /2
        y = 20
        self.canvas.create_text(
            x, y,
            text=self.message, tags="victory",
            fill="black", font=("Arial", 16)
        )





def run(readGrid, solvedGrid, message):
    root = Tk()
    sudokuUi = SudokuUI(root, readGrid, solvedGrid, message)
    root.geometry("%dx%d" % (sudokuUi.WIDTH,sudokuUi.HEIGHT))
    root.mainloop()
