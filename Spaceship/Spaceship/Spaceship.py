from tkinter import *
import random
import time

#Superclass for all moving objects on Canvas
class Hull():
    """Hull class used as a superclass for all moving elements in game
    
    It is created with 3 requiered arguments:
                                position on x-axis (int x),
                                position on y-axis (int y),
                                hull's image path (str image_path)
                                
                            And has 2 optional arguments
                                speed on x-axis (int sx)[defaults to 0]
                                speed on y-axis (int sy)[defaults to 0]
                                """
    #Default constructor
    def __init__(self, x: int, y: int, image_path: str, 
                 sx: int = 0, sy: int = 0):
        self._x = x
        self._y = y
        self._sx = sx
        self._sy = sy
        self.image = PhotoImage(file = image_path)
        
    def get_X(self) -> int:
        """Returns object's x-position"""
        return self._x

    def get_Y(self) -> int:
        """Returns object's y-position"""
        return self._y

    def get_image(self) -> PhotoImage:
        """Returns PhotoImage containing object's picture"""
        return self.image

    def draw(self, canvas: Canvas):
        """Draws object's picture on given canvas"""
        canvas.create_image(self._x, self._y, anchor = NW, image = self.image)

#Hero's spaceship (Hull with added features like acceleration)
class Hero(Hull):
    """Spaceship controlled by player with left and right movement
    
    It is created with 3 requiered arguments:
                                position on x-axis (int x),
                                position on y-axis (int y),
                                hull's image path (str image_path)
                                
                            And has 2 optional arguments
                                speed on x-axis (int sx)[defaults to 0]
                                speed on y-axis (int sy)[defaults to 0]
                                """
    #Acceleration to left(amount of change given in argument)
    def move_left(self):
        """Move spaceship to left

        Movement speed determined by speed on x-axis (int sx)
        """
        self._x = ((self._x + (self.image.width() / 2) - self._sx) % canvas_size[0]) - self.image.width() / 2

    #Acceleration to right
    def move_right(self):
        """Move spaceship to right

        Movement speed determined by speed on x-axis (int sx)
        """
        self._x = ((self._x + (self.image.width() / 2) + self._sx) % canvas_size[0]) - self.image.width() / 2

#Flying rocks class
class Rock(Hull):
    """Flying object with no speed modification
    
    It is created with 3 requiered arguments:
                                position on x-axis (int x),
                                position on y-axis (int y),
                                hull's image path (str image_path)
                                
                            And has 2 optional arguments
                                speed on x-axis (int sx)[defaults to 0]
                                speed on y-axis (int sy)[defaults to 0]
                                """
    def move_down(self):
        """Move rock down

        Movement speed determined by speed on y-axis (int sy)
        Returns itself when it is outside canvas, otherwise None is returned.
        """
        self._y = self._y + self._sy

        if self._y > canvas_size[1]:
            return self
        else:
            return None

#DRAW images on the canvas
def draw(canvas: Canvas, hulls: list, spacehero: Hero):
    """Handles all drawing that happens on canvas

    Parameters:
        canvas (Canvas) to draw on
        hulls (list) containing all non-spacehero moving objects
        spacehero (Hero) player-controlled unit
    """
    #clear old drawings
    canvas.delete("all")

    #create black background
    canvas.create_rectangle(0, 0, canvas_size[0], canvas_size[1], fill = "black")

    #draw spacehero
    spacehero.draw(canvas)

    #draw other items
    for hull in hulls:
        hull.draw(canvas)

def spawn_enemy(hulls: list):
    """Adds new enemies to hulls-list

    Parameters:
        hulls (list) containing all non-hero moving objects
    """
    hulls.append(Rock(random.randint(0, canvas_size[0]), 0, rock_image, sy = 10))

#Magic variables
canvas_size = [800, 600]
rock_image = "Art/Rock1.gif"
hero_image = "Art/ScarabSolo.gif"
time.clock()

#STARTING INTERFACE ITEMS

#master
master = Tk()
master.title("Space Wars") #name
master.resizable(0, 0) #not resizeable

#canvas
canvas = Canvas(master, width = canvas_size[0], height = canvas_size[1])
canvas.pack()

#GAME part

#hulls list to contain all non-hero moving objects
hulls = list()

#Player-controlled Hero object created on the bottom of canvas
spacehero = Hero(canvas_size[0] / 2, canvas_size[1] - 140, hero_image, sx = 5)

#Eventhandlers
def refresher():
    """Recursion loop to control canvas drawing"""
    draw(canvas, hulls, spacehero)
    master.after(50, refresher)

def handler():
    """Recursion loop to control game objects refreshing"""

    #Create new enemies somewhat randomly
    rnd = random.random()
    if(time.clock() % 3*rnd > 2.9*rnd):
        spawn_enemy(hulls)
    
    #Move and refresh all non-hero items
    for hull in hulls:
        if type(hull) == Rock:
            remove_checker = hull.move_down()
            if(remove_checker == hull):
                hulls.remove(hull)
            else:
                print(len(hulls))

    master.after(100, handler)
    
def move_right(event):
    """Throw away method to fix spacehero movement problems"""
    spacehero.move_right()

def move_left(event):
    """Throw away method to fix spacehero movement problems"""
    spacehero.move_left()

master.after(10, handler)
master.after(50, refresher)
master.bind('<Right>', move_right)
master.bind('<Left>', move_left)

#mainloop
master.mainloop()