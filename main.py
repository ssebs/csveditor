# pylint: disable=C0103,C0111,W0614,W0401,C0200
from Tkinter import *
import tkMessageBox
import tkFileDialog
import tkFont
import csv

##
# CSV GUI Editor written in python using tkinter
# - A lightweight csv editor
# - (c) 2017 Sebastian Safari ssebs@ymail.com
##


class Application(Frame):

    cellList = []
    currentCells = []

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createDefaultWidgets()

    def focus_next_window(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def selectall(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return "break"

    # TODO: Create bind for arrow keys

    def createDefaultWidgets(self):
        w, h = 7, 1
        self.sizeX = 4
        self.sizeY = 6
        self.defaultCells = []
        for i in range(self.sizeY):
            self.defaultCells.append([])
            for j in range(self.sizeX):
                self.defaultCells[i].append([])

        for i in range(self.sizeY):
            for j in range(self.sizeX):
                tmp = Text(self, width=w, height=h)
                tmp.bind("<Tab>", self.focus_next_window)
                tmp.bind("<Control-a>", self.selectall)
                tmp.insert(END, "")
                tmp.grid(padx=0, pady=0, column=j, row=i)

                self.defaultCells[i][j] = tmp
                self.cellList.append(tmp)

        self.defaultCells[0][0].focus_force()
        self.currentCells = self.defaultCells
        
        
        # TODO: Add buttons to create new rows/columns

    def newCells(self):
        self.removeCells()
        self.createDefaultWidgets()

    def removeCells(self):
        while(len(self.cellList) > 0):
            for cell in self.cellList:
                # print str(i) + str(j)
                cell.destroy()
                self.cellList.remove(cell)
        

    def loadCells(self, ary):

        self.removeCells()

        # get the max width of the cells
        mx = 0
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                if(len(ary[i][j]) >= mx):
                    mx = len(ary[i][j])
        w = mx

        sizeX = len(ary)
        sizeY = len(ary[0])
        loadCells = []
        for i in range(sizeY):
            loadCells.append([])
            for j in range(sizeX):
                loadCells[i].append([])

        # create the new cells
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                tmp = Text(self, width=w, height=1)
                tmp.bind("<Tab>", self.focus_next_window)
                tmp.bind("<Control-a>", self.selectall)
                tmp.insert(END, ary[i][j])

                if(i == 0):
                    tmp.config(font=("Helvetica", 10, tkFont.BOLD))
                    tmp.config(state=DISABLED, relief=FLAT,
                               bg=app.master.cget('bg'))
                
                loadCells[i][j] = tmp
                self.cellList.append(tmp)

                tmp.grid(padx=0, pady=0, column=j, row=i)
        
        self.currentCells = loadCells

    def saveCells(self):
        print "saving Cells"

        filename = tkFileDialog.asksaveasfilename(initialdir = ".",title = "Save File",filetypes = (("csv files","*.csv"),("all files","*.*")))
        var = ""
        with open(filename, "wb") as csvfile:
            wr = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
            for i in range(len(self.currentCells)):
                for j in range(len(self.currentCells[0])):
                    var = self.currentCells[i][j].get(1.0,END).strip()
                    if var is not "\n":
                        print var
                        wr.writerow(["var"] + [var])

        tkMessageBox.showinfo("", "Saved!")
        # First,Last,user
        # Bob,Johnson,bjohn
        # Mark,Phillips,mphil
        #



# End Application Class #


# Begin functions #

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

# End functions #


### CODE ENTRY ###
app = Application()
menubar = Menu(app)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=app.newCells)     # add save dialog
filemenu.add_command(label="Open", command=readFile)        # add save dialog
filemenu.add_command(label="Save as", command=app.saveCells)
filemenu.add_command(label="Exit", command=app.quit)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_command(label="Exit", command=app.quit)

app.master.title('CSV Editor')
app.master.config(menu=menubar)

default_font = tkFont.nametofont("TkTextFont")
default_font.configure(family="Helvetica")

app.option_add("*Font", default_font)
app.mainloop()
