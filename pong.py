from tkinter import *
import random
import time
import winsound

def beep():
    frequency = 2500                                            # Set Frequency To 2500 Hertz
    duration = 50                                               # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

class Paddle:
    def __init__(self, canvas, color):          
        self.canvas=canvas                                      #all drawing functions will need that canvas
        self.id = canvas.create_rectangle(0, 0,100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.shiftInXPerGameLoop = 0                            
        self.canvasWidth=self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.shiftDirectionSetLeft)
        self.canvas.bind_all('<KeyPress-Right>', self.shiftDirectionSetRight)
    
    def shiftDirectionSetLeft(self, event):
        self.shiftInXPerGameLoop=-5
        
    def shiftDirectionSetRight(self, event):
        self.shiftInXPerGameLoop= 5
        
    def draw(self):
        leftUpperCorner_x,leftUpperCorner_y,rightLowerCorner_x,rightLowerCorner_y=self.canvas.coords(self.id)
        if leftUpperCorner_x <= 0:                                    #if left corner of the paddle already touching left edge of the screen
            if self.shiftInXPerGameLoop < 0:                          #if player wants to move further left
                self.shiftInXPerGameLoop=0                            #then prevent that move
        if rightLowerCorner_x >= self.canvasWidth:                    #if right corner of the paddle already touching right edge of the screen
            if self.shiftInXPerGameLoop > 0:                          #if player wants to move further right
                self.shiftInXPerGameLoop=0                            #then prevent that move
        self.canvas.move(self.id, self.shiftInXPerGameLoop, 0)        #do the actual move
        

class Ball:
    def __init__(self, canvas, color, startx, starty):
        self.canvas=canvas
        self.id=canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, startx, startx)
        possibleStartingShiftPerGameLoop=[-3, -1, -1, 1, 2, 3]
        random.shuffle(possibleStartingShiftPerGameLoop)
        self.x=possibleStartingShiftPerGameLoop[0]
        self.y=-3
        self.canvasHeight=self.canvas.winfo_height()
        self.canvasWidth=self.canvas.winfo_width()
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        leftTop_x,leftTop_y,rightBottom_x,rightBottom_y = self.canvas.coords(self.id)
        if leftTop_y <= 0:
            self.y=3
        if rightBottom_y >= self.canvasHeight:
            self.y=-3
        if leftTop_x <= 0:
            self.x=3    
        if rightBottom_x >= self.canvasWidth:
            self.x=-3



tk=Tk()
tk.title("Janka Gra")
tk.resizable(height=0,width=0)
tk.wm_attributes("-topmost", 1) #controls whether the window stays on top of normal windows
myCanvas=Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)#borderwidth, bd, 
myCanvas.pack()
tk.update()

myPaddle=Paddle(myCanvas, 'black')
myBall=Ball(myCanvas, 'red', 200, 100)


while 1:
    myBall.draw()
    myPaddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)