from tkinter import *
import random
import time
import math

#All immutable global functions and variables
class Globals():
    #Canvas size
    canvas_size = [800, 600]
    starting_points = 0
    game_refresh_rate = 1
    graphics_refresh_rate = 1

    #Hero specific
    position_hero_y = canvas_size[1] - 140
    speed_hero = 5

    #Rock specific
    speed_rock = 10

    #Art work paths
    image_rock = "Art/meteorB4.png"
    image_hero = "Art/ship.png"

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
        self.size = [self.image.width(), self.image.height()]

        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy

        self.size = [self.image.width(), self.image.height()]

    def get_radius(self) -> int:
        """Calculates objects radius"""
        
        n = min(self.size)
        n = n / 2
        n = int(n)
        return n

    def get_image(self) -> PhotoImage:
        """Returns PhotoImage containing object's picture"""
        return self.image

    def draw(self, canvas: Canvas):
        """Draws object's picture on given canvas"""
        canvas.create_image(self.x - (self.size[0] / 2), \
            self.y - (self.size[1] / 2), anchor = NW, image = self.image)

    def collision(self, other):
        """Checks collision with parameter object. If collision, returns true, else returns false"""

        distance = math.sqrt((abs(self.x - other.x) ** 2) \
           + (abs(self.y - other.y)** 2))

        print("Player: ", other.x)
        print("Rock: ", self.x)

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
    def move_left(self, event):
        """Move spaceship to left

        Movement speed determined by speed on x-axis (int sx)
        """
        self.x = ((self.x - self.sx) % Globals.canvas_size[0])

    #Acceleration to right
    def move_right(self, event):
        """Move spaceship to right

        Movement speed determined by speed on x-axis (int sx)
        """
        self.x = ((self.x + self.sx) % Globals.canvas_size[0])

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
        self.y = self.y + self.sy

        if self.y > Globals.canvas_size[1]:
            return self
        else:
            return None

#DRAW images on the canvas
def graphics_operator(canvas: Canvas, hulls: list, spacehero: Hero, points: int):
    """Handles all drawing that happens on canvas

    Parameters:
        canvas (Canvas) to draw on
        hulls (list) containing all non-spacehero moving objects
        spacehero (Hero) player-controlled unit
    """

    points_text = "Points: " + str(points)

    #clear old drawings
    canvas.delete("all")

    #create black background
    canvas.create_rectangle(0, 0, Globals.canvas_size[0], Globals.canvas_size[1], fill = "black")

    #show points on canvas 
    canvas.create_text(Globals.canvas_size[0] - 60, 10, anchor = NW, text=points_text, fill="white")

    #draw spacehero
    spacehero.draw(canvas)

    #draw other items
    for hull in hulls:
        hull.draw(canvas)

###
#STARTING INTERFACE ITEMS

#master
master = Tk()
master.title("Space Mission") #name
master.resizable(0, 0) #not resizeable

#canvas
canvas = Canvas(master, width = Globals.canvas_size[0], height = Globals.canvas_size[1])
canvas.pack()

#time
time.clock()

###
#GAME part

def spawn_enemy(hulls: list):
    """Adds new enemies to hulls-list

    Parameters:
        hulls (list) containing all non-hero moving objects
    """
    hulls.append(Rock(random.randint(0, Globals.canvas_size[0]), 0, Globals.image_rock, sy = Globals.speed_rock))

def game_over():
    """Actions taken at end of the game"""
    master.destroy()
    print("Game over\nYour points: ", points)

#hulls list to contain all non-hero moving objects
hulls = list()

#Player-controlled Hero object created on the bottom of canvas
spacehero = Hero(Globals.canvas_size[0] / 2, Globals.position_hero_y, Globals.image_hero, sx = Globals.speed_hero)

#points calculator /points added when rocks reach bottom of the screen
points = Globals.starting_points

#Eventhandlers
def graphics_refresher():
    """Recursion loop to control canvas drawing"""
    graphics_operator(canvas, hulls, spacehero, points)
    master.after(Globals.graphics_refresh_rate, graphics_refresher)

def game_manager():
    """Recursion loop to control game objects refreshing"""

    global points

    #Create new enemies somewhat randomly #TODO: organize and improve
    rnd = random.random()
    if(time.clock() % 3*rnd > 2.9*rnd):
        spawn_enemy(hulls)
    
    #Move and refresh all non-hero items
    for hull in hulls:
        if type(hull) == Rock:
            #hull.move_down returns object itself if it reaches bottom of screen
            remove_checker = hull.move_down()
            if(remove_checker == hull):
                #remove hull referance from list
                hulls.remove(hull)
                #add points
                points += 1

    #Check collision of Rocks and Spacehero
    for hull in hulls:
        if hull.collision(spacehero):
            game_over()

    master.after(Globals.game_refresh_rate, game_manager)

master.after(10, game_manager)
master.after(50, graphics_refresher)
master.bind('<Right>', spacehero.move_right)
master.bind('<Left>', spacehero.move_left)

#mainloop
master.mainloop()