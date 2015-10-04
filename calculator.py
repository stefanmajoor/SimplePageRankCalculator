from Tkinter import *
import numpy as np

class App:
    def __init__(self, master):
        self.rows = 4
        self.master = master
        self.update()
        self.matrixlabels = []
 
    '''
    Display all items 
    '''
    def update(self):
        self.frame = Frame(self.master)

        ## How many values
        Label(self.master, text="Amount of nodes:").grid(row=0, column=0, columnspan=3)
        
        ## No idea why this works. But it does
        var = StringVar(root)
        var.set(str(self.rows))
        self.rowBox = Spinbox(self.master, from_=1, to=10, textvariable=str(var))
        self.rowBox.grid(row=0, column=3, columnspan=3)
        Button(self.master, text="Update", command=self.setRows).grid(row=0, column=6)


        ## From and to indications
        Label(self.master, text="To").grid(column=3, row=1)
        Label(self.master, text="From").grid(row=3, column=0)

        self.labels = []

        ## Letters at top
        for i in range(0, self.rows):
            label = Label(self.master, text=unichr(ord("A")+i))
            label.grid(row=2, column=i+2)
            self.labels.append(label)

        ## Letters at the left
        for i in range(0, self.rows):
            label = Label(self.master, text=unichr(ord("A")+i))
            label.grid(row=i+3, column=1)
            self.labels.append(label)

        ## Create all entry fields
        self.entries = [[0. for i in range(self.rows)] for j in range(self.rows)]
        for i in range(0,self.rows):
            for j in range(0,self.rows):
                self.entries[i][j] = Spinbox(self.master, from_=0, to=10, width=3)
                self.entries[i][j].grid(row=i+3, column = j+2)

        ## calculate the different values
        values = []
        for i in range(0, self.rows):
            values.append(unichr(ord("A")+i))

        Label(self.master, text="Start at").grid(row=14, column=0)
        self.begin = Spinbox(self.master, values=values)
        self.begin.grid(row=14, column=3, columnspan=3)

        Label(self.master, text="Teleport rate").grid(row=15, column=0)
        self.teleport = Spinbox(self.master, from_=0.01, to=1, increment=0.01)
        self.teleport.grid(row=15, column=3, columnspan=3)


        ## Run button
        Button(self.master, text="Run", command=self.calculate).grid(row=15, column=6)

    '''
    Set the amount of rows
    '''
    def setRows(self):
        self.rows = int(self.rowBox.get())
        self.frame.grid_remove()
        for i in range(0,len(self.entries)):
            for j in range(0, len(self.entries[i])):
                self.entries[i][j].destroy()

        for label in self.labels:
            label.destroy()
        self.update()

    '''
    Calculate the Pagerank
    '''
    def calculate(self):
        values = np.empty([self.rows, self.rows])
        for i in range(0,self.rows):
            for j in range(0,self.rows):
                values[i][j] = self.entries[i][j].get()

        matr = self.calculateMatrix(values)

        ## calculate the start vector
        vec = np.zeros([self.rows])
        startIndex = ord(self.begin.get()) - ord("A")
        vec[startIndex] = 1


        label = Label(self.master, text="Iteratie")
        label.grid(row=40, column=0)
        self.matrixlabels.append(label)

        ## Letters at top
        for i in range(0, self.rows):
            label = Label(self.master, text=unichr(ord("A")+i))
            label.grid(row=40, column=i+1)
            self.matrixlabels.append(label)

        for i in range(0, 20):
            ## print the values
            label = Label(self.master, text=str(i))
            label.grid(row=41+i, column=0)
            self.matrixlabels.append(label)
            for j in range(0, self.rows):
                label = Label(self.master, text=str(round(vec[j], 3)))
                label.grid(row=41+i, column=j+1)
                self.matrixlabels.append(label)

            ## calculate new vector
            vec = vec.dot(matr)

    '''
    Calculate and display the matrix from the values
    '''
    def calculateMatrix(self, values):

        teleport = float(self.teleport.get())
        
        ## calculate the actual matrix row by row
        mat = np.empty([self.rows, self.rows])
        for i in range(0, self.rows):
            ## first calculate the sum of every item in the row
            s = 0
            for j in range(0, self.rows):
                s += values[i][j]

            ## now calculate the values
            for j in range(0, self.rows):
                if s != 0:
                    mat[i][j] = teleport/self.rows + (1-teleport)/s * values[i][j]
                else:
                    mat[i][j] = float(1)    /self.rows


        ## destroy old result
        for label in self.matrixlabels:
            label.destroy()
        self.matrixlabels = []

        ## Display matrix
        label = Label(self.master, text="Resulting matrix")
        label.grid(row=20, column=0)
        self.matrixlabels.append(label)

        ## Letters at top
        for i in range(0, self.rows):
            label = Label(self.master, text=unichr(ord("A")+i))
            label.grid(row=21, column=i+2)
            self.matrixlabels.append(label)

        ## Letters at the left
        for i in range(0, self.rows):
            label = Label(self.master, text=unichr(ord("A")+i))
            label.grid(row=i+22, column=1)
            self.matrixlabels.append(label)

        ## Create all entry fields
        for i in range(0,self.rows):
            for j in range(0,self.rows):
                label = Label(self.master, text=str(mat[i][j]))
                label.grid(row=i+22, column = j+2)
                self.matrixlabels.append(label)

        ## return matrix
        return mat

root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below