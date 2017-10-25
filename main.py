# pylint: disable=C0103,C0111,W0614,W0401
from Tkinter import *
import tkMessageBox


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def createWidgets(self):
		# TODO: make this a 2D array, so it can be indexed.
        cells = []
        sizeX = 4
        sizeY = 8
        px = 0
        py = 0
        w = 7
        h = 1

        for i in range(sizeY):
            tmp = Text(self, width=w, height=h)
            tmp.bind("<Tab>", self.focus_next_window)
            cells.append(tmp.grid(padx=px, pady=py))

            for j in range(sizeX):
                tmp = Text(self, width=w, height=h)
                tmp.bind("<Tab>", self.focus_next_window)
                cells.append(tmp.grid(padx=px, pady=py, row=i, column=j))


def hello():
    tkMessageBox.showinfo("", "Hello!")


root = Tk()
# create a toplevel menu
menubar = Menu(root)
menubar.add_command(label="Hello!", command=hello)
menubar.add_command(label="Quit!", command=root.quit)


app = Application()
app.master.title('CSV Editor')
app.master.config(menu=menubar)
app.mainloop()
