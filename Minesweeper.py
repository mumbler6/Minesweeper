from tkinter import *
from tkinter import ttk
from tkinter import font
from random import randint

dirX = [-1, -1, 0, 1, 1, 1, 0, -1]
dirY = [0, 1, 1, 1, 0, -1, -1, -1]
colors = ["black", "green", "blue", "orange", "red", "purple", "purple", "purple", "purple"]

class MinesweeperButton: # button 

    def __init__(self, x, y, visited):
        self.button = Button(root, height = 1, width = 2, bg="lightblue")
        self.x = x
        self.y = y
        self.visited = visited

    def reveal(self, button):
        self.button.config(bg="white")
        self.visited = True
        if minefield[self.x][self.y] == 0:
            num = prox[self.x][self.y]
            if num == 0:
                self.button.config(text = " ")
                for dir in range(0, 8):
                    newX = self.x + dirX[dir]
                    newY = self.y + dirY[dir]
                    if inRange(newX, newY) and minefield[newX][newY] == 1:
                        continue
                    if inRange(newX, newY) and prox[newX][newY] >= 0 and buttons[newX][newY].visited == False:
                        buttons[newX][newY].reveal(buttons[newX][newY])
            else:
                self.button.config(text=num, fg=colors[num])
        else:
            self.button.config(text = "*", fg="black", bg="red")
            reveal_all()


    def flag(self, button):
        global bombsleft
        if self.visited == False:
            if self.button['text'] == "X":
                self.button.config(text=" ")
                bombsleft = bombsleft + 1
                BombsLeft.config(text="X: " + str(bombsleft))
            else:
                self.button.config(text="X")
                bombsleft = bombsleft - 1
                BombsLeft.config(text = "X: "+str(bombsleft))

def reset():
    generate()
    for x in range(0, 10):
        for y in range(0, 10):
            buttons[x][y].button.config(text = " ", bg = "lightblue", fg = "black")
            buttons[x][y].visited = False

    create()
    BombsLeft.config(text="X: " + str(bombsleft))

def inRange(x, y):
    return x >= 0 and x < 10 and y >= 0 and y < 10

def create():
    global minefield
    global prox
    for x in range(0, 10):
        for y in range(0, 10):
            if minefield[x][y] == 0:
                number = 0
                for dir in range(0, 8):
                    newX = x + dirX[dir]
                    newY = y + dirY[dir]
                    if inRange(newX, newY) and minefield[newX][newY]:
                        number += 1
                prox[x][y] = number

def generate():
    global maxbombs
    global minefield
    global prox
    global bombsleft
    minefield = []
    prox = []
    numbombs = 0
    for x in range(0, 10):
        subfield = []
        subprox = []
        for y in range(0, 10):
            rand = randint(0, 100)
            if rand > 82 and numbombs < maxbombs:
                subfield.append(1)
                numbombs += 1
            else:
                subfield.append(0)
            subprox.append(0)
        minefield.append(subfield)
        prox.append(subprox)
    bombsleft = numbombs

def reveal_all():
    for x in range(0, 10):
        for y in range(0, 10):
            if buttons[x][y].visited == False:
                buttons[x][y].reveal(buttons[x][y])

root = Tk()
root.title("Minesweeper")
root.geometry('240x285')

maxbombs = 18
bombsleft = 0
buttons = []
minefield = []
prox = []
Restart = Button(root, text = "Reset", width = 4, height = 1, command = reset)
Restart.place(x = 0, y = 260)
Reveal = Button(root, text = "Reveal All", width = 10, height = 1, command = reveal_all)
Reveal.place(x = 35, y = 260)
for x in range(0, 10):
    subbuttons = []
    for y in range(0, 10):
        b = MinesweeperButton(x, y, False)
        b.button.grid(row=x, column=y)
        b.button.bind("<Button-1>", b.reveal)
        b.button.bind("<Button-3>", b.flag)
        subbuttons.append(b)
    buttons.append(subbuttons)
generate()
BombsLeft = Label(root, text = "X: "+str(bombsleft))
BombsLeft.place(x = 200, y= 260)
create()
root.mainloop();
