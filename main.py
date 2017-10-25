# pylint: disable=C0103,C0111,W0614,W0401,C0200
from Tkinter import *
import tkMessageBox
import tkFileDialog
import csv


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createDefaultWidgets()

    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def selectall(self, event):
        event.widget.tag_add("sel","1.0","end")
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return "break"

    #TODO: Create bind for arrow keys

    def createDefaultWidgets(self):
        w, h = 7, 1
        self.sizeX = 4
        self.sizeY = 6
        self.cells = []
        for i in range(self.sizeY):
            self.cells.append([])
            for j in range(self.sizeX):
                self.cells[i].append([])

        for i in range(self.sizeY):
            self.cells.append([])
            for j in range(self.sizeX):
                tmp = Text(self, width=w, height=h)
                tmp.bind("<Tab>", self.focus_next_window)
                tmp.bind("<Control-a>", self.selectall)
                tmp.grid(padx=0, pady=0, column=j, row=i)
                self.cells[i][j] = tmp
        self.cells[0][0].focus_force()

        #TODO: Add buttons to create new rows/columns

    def loadCells(self, ary):
        # remove default cells
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                #print str(i) + str(j)
                self.cells[i][j].destroy()
        
        # get the max width of the cells
        mx = 0
        for i in range(len(ary)):
            for j in range(len(ary[0])):
              if( len(ary[i][j]) >= mx ):
                mx = len(ary[i][j])
        w = mx

        # create the new cells
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                # print ary[i][j]
                tmp = Text(self, width=w, height=1)
                tmp.bind("<Tab>", self.focus_next_window)
                tmp.bind("<Control-a>", self.selectall)
                tmp.insert(END, ary[i][j])
                tmp.grid(padx=0, pady=0, column=j, row=i)
                tmp.grid(padx=0, pady=0)

        #TODO: Make headers bold, non-editable?


def hello():
    tkMessageBox.showinfo("", "Hello!")


def readFile():
    filename = tkFileDialog.askopenfilename(initialdir=".", title="Select file",
                                            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    ary = []
    col = -1
    rows = []
    # get array size & get contents of rows
    with open(filename, "rb") as csvfile:
        rd = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in rd:
            ary.append([])
            col = len(row)
            rows.append(row)

    # create the array
    for i in range(len(ary)):
        for j in range(col):
            ary[i].append([])

    # fill the array
    for i in range(len(ary)):
        for j in range(col):
            # print rows[i][j]
            ary[i][j] = rows[i][j]

    app.loadCells(ary)


app = Application()
menubar = Menu(app)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=hello)
filemenu.add_command(label="Open", command=readFile)
filemenu.add_command(label="Save as", command=hello)
filemenu.add_command(label="Exit", command=app.quit)

menubar.add_cascade(label="File", menu=filemenu)

app.master.title('CSV Editor')
app.master.config(menu=menubar)
app.mainloop()
