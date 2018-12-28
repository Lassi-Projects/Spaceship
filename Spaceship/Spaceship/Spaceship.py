from tkinter import *
import random
import time
import math

#All immutable global functions and variables
class Globals():
    #Canvas size
    canvas_size = [800, 600]
    starting_points = 0
    game_refresh_rate = 10
    graphics_refresh_rate = 10

    #Hero specific
    position_hero_y = canvas_size[1] - 140
    speed_hero = 6 #pixel/10ms

    #Rock specific
    speed_rock = 2 #pixels/10ms
    rock_acceleration = 0.1 #(pixels/10ms)/points_to_acc
    points_to_acc = 5
    #spawn rate
    rate_range = 100
    rate_limit = 95
    spawn_interval = 1


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
                                speed is pixels/10ms
                                object size compared to original photosize x:100
                                    (int scale > 0)[defaults to 100]
                                """
    #Default constructor
    def __init__(self, x: float, y: float, image_path: str, 
                 sx: float = 0, sy: float = 0, scale: int = 100):
        #setting image to correct size
        self.image = PhotoImage(file = image_path)

        #TODO: add image scaling
        self.size = [self.image.width(), self.image.height()]

        self.x = x
        self.y = y
        #speed is in pixels/10ms
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
                                speed is pixels/10ms
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
                                speed is pixels/10ms
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
last_time = time.time()

###
#GAME part

def spawn_meteor(hulls: list, points):
    """Adds new enemies to hulls-list

    Parameters:
        hulls (list) containing all non-hero moving objects
    """
    point_level = int(points / Globals.points_to_acc)
    rock_speed = Globals.speed_rock + Globals.rock_acceleration * (point_level)

    hulls.append(Rock(random.randint(0, Globals.canvas_size[0]), 0, Globals.image_rock, sy = rock_speed))

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
#Controls meteor spawning
spawn_control = False

#Eventhandlers
def graphics_refresher():
    """Recursion loop to control canvas drawing"""
    graphics_operator(canvas, hulls, spacehero, points)
    master.after(Globals.graphics_refresh_rate, graphics_refresher)

def game_manager():
    """Recursion loop to control game objects refreshing"""

    #control points
    global points
    #Control interval of spawns
    global last_time
    global spawn_control
    #create random integer
    rnd = random.randrange(Globals.rate_range)

    #Create new enemies
    if(spawn_control):
        spawn_meteor(hulls, points)
        last_time = time.time()
        spawn_control = False
    #spawn enemies after spawn_interval time and if rnd exceeds rate_limit
    elif(time.time() - last_time > Globals.spawn_interval and rnd > Globals.rate_limit):
        spawn_control = True

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