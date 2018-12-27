from tkinter import *
import random
import time
import math

#Superclass for all moving objects on Canvas
class Hull():
    """Hull class used as a superclass for all moving elements in game
    
    It is created with 3 requiered arguments:
                                position on x-axis (int x),
                                position on y-axis (int y),
                                hull's image path (str image_path)
                                
                            And has 3 optional arguments
                                speed on x-axis (int sx)[defaults to 0]
                                speed on y-axis (int sy)[defaults to 0]
                                object size compared to original photosize x:100
                                    (int scale > 0)[defaults to 100]
                                """
    #Default constructor
    def __init__(self, x: int, y: int, image_path: str, 
                 sx: int = 0, sy: int = 0, scale: int = 100):
        #setting image to correct size
        self.image = PhotoImage(file = image_path)

        #TODO: add image scaling

        self._x = x - self.image.width() / 2
        self._y = y
        self._sx = sx
        self._sy = sy

        self.size = [self.image.width(), self.image.height()]
        
    def get_X(self) -> int:
        """Returns object's x-position"""
        return self._x

    def get_Y(self) -> int:
        """Returns object's y-position"""
        return self._y

    def get_middle(self) -> list:
        """Returns middle point [x, y] of the object"""
        if self.get_X() - self.size[0] < 0:
            self_x = 0
        elif self.get_X() - self.size[0] > canvas_size[0]:
            self_x = canvas_size[0]
        else:
            self_x = self.get_X() - self.size[0]

        if self.get_Y() - self.size[1] < 0:
            self_y = 0
        elif self.get_Y() - self.size[1] > canvas_size[1]:
            self_y = canvas_size[1]
        else:
            self_y = self.get_Y() - self.size[1]

        return [self_x, self_y]

    def get_radius(self) -> int:
        """Calculates objects radius"""
        
        n = min(self.size)
        n = n / 2
        return n

        #Older version
        #n = (self.size[0] / 2) ** 2 + (self.size[1] / 2) ** 2
        #n = math.sqrt(n)
        #n = int(n)
        #return n

    def get_image(self) -> PhotoImage:
        """Returns PhotoImage containing object's picture"""
        return self.image

    def draw(self, canvas: Canvas):
        """Draws object's picture on given canvas"""
        canvas.create_image(self._x, self._y, anchor = NW, image = self.image)

    def collision(self, other):
        """Checks collision with parameter object. If collision, returns true, else returns false"""

        print("Self ", self.get_middle()[0], self.get_middle()[1])
        print("Other ", other.get_middle()[0], other.get_middle()[1])

        distance = math.sqrt((abs(self.get_middle()[0] - other.get_middle()[0]) ** 2) \
           + (abs(self.get_middle()[1] - other.get_middle()[1])** 2))

        if distance < self.get_radius() + other.get_radius():
            return True
        else:
            return False

#Hero's spaceship (Hull with added features like acceleration)
class Hero(Hull):
    """Spaceship controlled by player with left and right movement
    
    It is created with 3 requiered arguments:
                                position on x-axis (int x),
                                position on y-axis (int y),
                                hull's image path (str image_path)
                                
                            And has 3 optional arguments
                                speed on x-axis (int sx)[defaults to 0]
                                speed on y-axis (int sy)[defaults to 0]
                                object size compared to original photosize (float > 0)[defaults to 1]
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

    def get_middle(self):
        y = self._y - self.size[1] /2
        return [super().get_middle()[0], y]

#Flying rocks class
class Rock(Hull):
    """Flying object with no speed modification
    
    It is created with 3 requiered arguments:
                                position on x-axis (int x),
                                position on y-axis (int y),
                                hull's image path (str image_path)
                                
                            And has 3 optional arguments
                                speed on x-axis (int sx)[defaults to 0]
                                speed on y-axis (int sy)[defaults to 0]
                                object size compared to original photosize (float > 0)[defaults to 1]
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

def game_over():
    master.destroy()

#Magic variables
canvas_size = [800, 600]
rock_image = "Art/Rock1.gif"
hero_image = "Art/ScarabSolo.gif"
hero_y_position = canvas_size[1] - 140
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
spacehero = Hero(canvas_size[0] / 2, hero_y_position, hero_image, sx = 5)

#Eventhandlers
def refresher():
    """Recursion loop to control canvas drawing"""
    draw(canvas, hulls, spacehero)
    master.after(5, refresher)

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

    #Check collision of Rocks and Spacehero
    for hull in hulls:
        if hull.collision(spacehero):
            game_over()

    master.after(50, handler)
    
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