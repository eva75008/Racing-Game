import pyxel
from math import sin, radians, sqrt
from random import randint


screen_width = 720
screen_height = 480
convergence = (screen_width // 2, 200)
sky_height = screen_height // 2


class Game:
    def __init__(self):
        pyxel.init(screen_width, screen_height, "Retro-racing Game", 60)
        pyxel.load("graphic.pyxres")
        self.road = Road()
        self.milestonel = Milestones(0)
        self.milestoner = Milestones(720)
        self.timeOfDay = TimeOfDay()
        self.player = Player()
        self.enemies = Enemies(self.player)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.timeOfDay.update()
        self.milestonel.update()
        self.milestoner.update()
        self.player.update()
        self.enemies.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_LIME)
        self.road.draw()
        self.enemies.draw()
        self.timeOfDay.draw()
        self.milestonel.draw()
        self.milestoner.draw()
        self.player.draw()


        
class Road:
    def __init__(self):
        self.Xo = screen_width // 2
        self.Yo = 200
        self.max_height = 64
        self.Xg = screen_width / 3
        self.Yg = screen_height
        self.Xd = (screen_width * 2) / 3
        self.Yd = screen_height
        self.l = self.Xd- self.Xg
        #self.sizes_coeff = self.min_width
        self.sizes_coeff = 18

        self.startx = self.Xo
        self.starty = self.Yo
         #self.Xf = self.Xg
        
        self.overflowX = 200
        self.line_thickness = 40
        
        self.endY = self.starty


    def update(self):
        pass

    
    def createRoad(self):
        pyxel.tri(
            -self.overflowX,
            screen_height,
            screen_width + self.overflowX,
            screen_height,
            self.Xo,
            self.Yo,
            pyxel.COLOR_GRAY,
        )
    
    
    def directions(self, Xf):
        self.Xf = Xf
        if self.starty >= self.Yg + 50:
            self.__init__()

        self.coeff = (self.Yg-self.Yo)/(self.Xf-self.Xo)

        self.size = self.sizes_coeff*(abs(self.startx - self.Xo) / (screen_width/2))

        self.starty += 7 * ((self.starty-199)/(screen_height-200))
        self.startx = (self.starty-200)/self.coeff + self.Xo
        
        self.endY = self.starty + self.size
        self.endX = (self.endY-200)/self.coeff + self.Xo


    def draw(self):
        self.createRoad()
        #self.directions()

        if self.starty < screen_height: 
            self.directions(self.Xg)
            for n in range(1, 3):
                for x in range(self.line_thickness):
                    pyxel.line(
                        self.startx
                        + ((self.line_thickness if n == 2 else -self.line_thickness)),
                        self.starty,
                         self.endX,
                         self.endY,
                        pyxel.COLOR_WHITE,
                    )
                self.directions(self.Xd)

        
        
        
        
        
        
class Roads:
    def __init__(self):
        self.overflowX = 200
        self.line_thickness = 40

    def createRoad(self):
        pyxel.tri(
            -self.overflowX,
            screen_height,
            screen_width + self.overflowX,
            screen_height,
            convergence[0],
            convergence[1],
            pyxel.COLOR_GRAY,
        )

    def outlineRoad(self):
        for n in range(2):
            for x in range(self.line_thickness):
                pyxel.line(
                    (-self.overflowX if n else screen_width + self.overflowX),
                    screen_height + x,
                    convergence[0],
                    convergence[1],
                    pyxel.COLOR_WHITE,
                )

    def createLanes(self):
        """for x in range(self.line_thickness):
            line(
                x1,
                y1,
                x2,
                y2,
                pyxel.COLOR_WHITE,
            )
"""





        for n in range(1, 3):
            for x in range(self.line_thickness):
                pyxel.line(
                    screen_width / 3 * n
                    + ((self.line_thickness if n == 2 else -self.line_thickness)),
                    screen_height + x,
                    convergence[0],
                    convergence[1],
                    pyxel.COLOR_WHITE,
                )

    def draw(self):
        self.createRoad()
        self.outlineRoad()
        self.createLanes()


class Enemies:
    def __init__(self, player, scaling_factor=0.05):
        self.player = player
        (self.x, self.y) = convergence
        self.scaling_factor = scaling_factor
        self.trajectory = randint(-1, 1)

    def calculateRadius(self, y, initial_size):
        y -= convergence[1]
        return self.scaling_factor * y + initial_size

    def increaseSpeed(self, y, initial_speed):
        y -= convergence[1] - 1
        return initial_speed * 2 ** (y / 60)

    def update(self):
        self.y += self.increaseSpeed(self.y, 1)
        self.x += self.trajectory * self.increaseSpeed(self.y, 1)
        if self.y > screen_height + self.calculateRadius(self.y, 8):
            self.y = convergence[1]
            self.x = convergence[0]
            self.trajectory = randint(-1, 1)

        # Check collision with player
        if self.checkCollision():
            self.player.onCollision()

    def checkCollision(self):
        # Calculate the radius of the ball used in the collision detection
        radius = self.calculateRadius(self.y, 8)

        # Calculate the dimensions of the player rectangle used in the collision detection
        x = self.player.x + self.player.width * 0.3
        y = self.player.y + self.player.height * 0.3
        width = self.player.width * 0.4
        height = self.player.height * 0.4

        # Check if the ball collides with the player
        return (
            self.x + radius >= x
            and self.x - radius <= x + width
            and self.y + radius >= y
            and self.y - radius <= y + height
        )

    def draw(self):
        pyxel.circ(self.x, self.y, self.calculateRadius(self.y, 8), pyxel.COLOR_WHITE)


class TimeOfDay:
    def __init__(self, speed=0.5, day=True):
        self.speed = speed
        self.day = day
        self.pos = [1, 100]
        self.graphicsPositionY = 16
        self.sky = sky_height - 50

    def update(self):
        self.pos[0] += self.speed
        self.pos[1] = (
            self.sky * sin(radians(-180 * self.pos[0] / screen_width)) + self.sky
        )
        if self.pos[0] > screen_width:
            self.day = not self.day
            self.pos[0] = 1
            if self.day:
                self.graphicsPositionY = 16
            else:
                self.graphicsPositionY = 80

    def draw(self):
        pyxel.rect(
            0,
            0,
            screen_width,
            sky_height,
            pyxel.COLOR_CYAN if self.day else pyxel.COLOR_NAVY,
        )
        pyxel.blt(
            self.pos[0],
            self.pos[1],
            0,
            0,
            self.graphicsPositionY,
            60,
            60,
            pyxel.COLOR_BLACK,
        )

        

class Milestones:
    def __init__(self, Xf):
        self.Xo = screen_width // 2
        self.Yo = 200
        self.max_height = 64
        self.Xg = 0
        self.Yg = screen_height - 150
        self.Xd = 720
        self.Yd = screen_height - 150
        self.l = self.Xd- self.Xg
        #self.sizes_coeff = self.min_width
        self.sizes_coeff = 18

        self.startx = self.Xo
        self.starty = self.Yo
        self.Xf = Xf


    def update(self):
        pass

    def directions(self):
        if self.starty >= screen_height-100:
            self.__init__(self.Xf)

        self.coeff = (self.Yg-self.Yo)/(self.Xf-self.Xo)

        self.size = self.sizes_coeff*(abs(self.startx - self.Xo) / (screen_width/2))

        self.starty += 7 * ((self.starty-199)/(screen_height-200))
        self.startx = (self.starty-200)/self.coeff + self.Xo - (30)


    def draw(self):
        self.directions()

        if self.starty > 220:
            pyxel.rect(
                    self.startx,
                    self.starty,
                    self.size,
                    self.size*4,
                    pyxel.COLOR_RED,
                )

            pyxel.rect(
                self.startx,
                self.starty + self.size * 0.45,  #.45 ==> size delta Y / size
                self.size,
                self.size * 0.6,
                pyxel.COLOR_WHITE,
            )


            
            

class Player:
    def __init__(self):
        self.width = 95
        self.height = 150
        self.player_speed = 10
        self.wheel_size = (32, 15)
        self.wheel_speed = 18  # the lower the faster and wheel_speed <= 18
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 5:
            self.x -= self.player_speed
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < screen_width - self.width - 5:
            self.x += self.player_speed

    def onCollision(self):
        None
        #pyxel.quit()   #animation de fin de jeu

    def draw(self):
        # motorcycle
        pyxel.blt(
            self.x,
            self.y,
            2,
            16,
            10,
            self.width,
            self.height,
            pyxel.COLOR_PINK,
        )
        # first tire tread (top)
        pyxel.blt(
            self.x + self.wheel_size[0],
            self.y
            + 86
            + 18
            - 17 * (pyxel.frame_count % self.wheel_speed) / (self.wheel_speed - 1),
            2,
            48,
            160,
            self.wheel_size[0],
            self.wheel_size[1],
        )
        # second tire tread (middle)
        pyxel.blt(
            self.x + self.wheel_size[0],
            self.y
            + 86
            + 2 * 18
            - 17 * (pyxel.frame_count % self.wheel_speed) / (self.wheel_speed - 1),
            2,
            48,
            160,
            self.wheel_size[0],
            self.wheel_size[1],
        )
        # third tire tread (bottom)
        if 17 * (pyxel.frame_count % self.wheel_speed) / (self.wheel_speed - 1) > 9:
            pyxel.blt(
                self.x + self.wheel_size[0],
                self.y
                + 86
                + 3 * 18
                - 17 * (pyxel.frame_count % self.wheel_speed) / (self.wheel_speed - 1),
                2,
                48,
                160,
                self.wheel_size[0],
                self.wheel_size[1],
            )


Game()
