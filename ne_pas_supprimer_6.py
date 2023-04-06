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
        pyxel.load("graphics.pyxres")
        self.road = Road()
        self.milestone = Milestones()
        self.timeOfDay = TimeOfDay()
        self.player = Player()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.road.update()
        self.timeOfDay.update()
        self.milestone.update()
        self.player.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_LIME)
        self.road.draw()
        self.timeOfDay.draw()
        self.milestone.draw()
        self.player.draw()


class Road:
    def __init__(self):
        self.overflowX = 200
        self.line_thickness = 40
        self.enemies = Enemies()

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

    def update(self):
        self.enemies.update()

    def draw(self):
        self.createRoad()
        self.outlineRoad()
        self.createLanes()
        self.enemies.draw()


class Enemies:
    def __init__(self, scaling_factor=0.05):
        (self.x, self.y) = convergence
        self.scaling_factor = scaling_factor
        self.trajectory = randint(-1, 1)
        self.player = Player()

    def calculateRadius(self, y, initial_size):
        y -= convergence[1]
        return self.scaling_factor * y + initial_size

    def increaseSpeed(self, y, initial_speed):
        y -= convergence[1] - 1
        return initial_speed * 2 ** (y / 60)

    def update(self):
        self.y += self.increaseSpeed(self.y, 1)
        self.x += self.trajectory * self.increaseSpeed(self.y, 1)
        if self.y > screen_height + self.calculateRadius(self.y, 5):
            self.y = convergence[1]
            self.x = convergence[0]
            if self.player.coordonnees() > 550 and randint(1, 100) > 30:
                self.trajectory = 1
            else:
                self.trajectory = randint(-1, 1)

    def draw(self):
        pyxel.circ(self.x, self.y, self.calculateRadius(self.y, 10), pyxel.COLOR_BLACK)
        pyxel.circ(self.x, self.y, self.calculateRadius(self.y, 8), pyxel.COLOR_WHITE)


class TimeOfDay:
    def __init__(self, speed=1, day=True):
        self.speed = speed
        self.day = day
        self.pos = [1, 100]
        self.graphicsPositionX = 22
        self.sky = sky_height - 30
        self.graphicsPositionX = 0
        self.graphicsPositionY = 16
        self.objetHeight = 63
        self.objetWidth = 63

    def update(self):
        self.pos[0] += self.speed
        self.pos[1] = (
            self.sky * sin(radians(-180 * self.pos[0] / screen_width)) + self.sky
        )
        if self.pos[0] > screen_width:
            self.day = not self.day
            self.pos[0] = 1
            if self.day:
                self.graphicsPositionX = 0
                self.graphicsPositionY = 16
                self.objetHeight = 63
                self.objetWidth = 63
            else:
                self.graphicsPositionX = 0
                self.graphicsPositionY = 80
                self.objetHeight = 47
                self.objetWidth = 47

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
            self.graphicsPositionX,
            self.graphicsPositionY,
            self.objetHeight,
            self.objetWidth,
            pyxel.COLOR_BLACK,
        )


class Milestones:
    def __init__(self):
        self.min_height = 8
        self.min_width = 2
        self.scaling_step = 1.5
        self.start = 10

    def update(self):
        pass

    def findSlope(self, x0, y0):
        return (y0 - convergence[1]) / (x0 - convergence[0])

    def findDistance(self, x0, slope):
        return abs(sqrt(slope**2 + 1) * (x0 - convergence[0]))

    def findX(self, y0, slope):
        return (y0 - convergence[1]) / slope + convergence[0]

    def right(self):
        slope = self.findSlope(screen_width - self.start, 375)
        total_distance = self.findDistance(self.start, slope)
        cper_dist = self.findDistance(self.findX(sky_height, slope), slope)
        scaling_factor = 1
        distance = cper_dist
        while distance < total_distance:
            x = distance / (slope**2 + 1) ** (1 / 2) + convergence[0]
            y = slope * (x - convergence[0]) + convergence[1]
            x_align_correction = self.min_width * scaling_factor
            pyxel.rect(
                x - x_align_correction,
                y - self.min_height * scaling_factor,
                self.min_width * scaling_factor,
                self.min_height * scaling_factor,
                pyxel.COLOR_RED,
            )
            pyxel.rect(
                x - x_align_correction,
                y - (self.min_height - 1) * scaling_factor,
                self.min_width * scaling_factor,
                scaling_factor,
                pyxel.COLOR_WHITE,
            )
            distance += (total_distance - cper_dist) / 8 * scaling_factor
            scaling_factor += self.scaling_step

    def left(self):
        slope = self.findSlope(self.start, 375)
        total_distance = self.findDistance(self.start, slope)
        cper_dist = self.findDistance(self.findX(sky_height, slope), slope)
        scaling_factor = 1
        distance = cper_dist
        while distance < total_distance:
            x = -distance / (slope**2 + 1) ** (1 / 2) + convergence[0]
            y = slope * (x - convergence[0]) + convergence[1]
            pyxel.rect(
                x,
                y - self.min_height * scaling_factor,
                self.min_width * scaling_factor,
                self.min_height * scaling_factor,
                pyxel.COLOR_RED,
            )
            pyxel.rect(
                x,
                y - (self.min_height - 1) * scaling_factor,
                self.min_width * scaling_factor,
                scaling_factor,
                pyxel.COLOR_WHITE,
            )
            distance += (total_distance - cper_dist) / 8 * scaling_factor
            scaling_factor += self.scaling_step

    def draw(self):
        self.right()
        self.left()


class Player:
    def __init__(self):
        self.player_width = 95
        self.player_height = 150
        self.player_speed = 10
        self.wheel_size = (32, 15)
        self.wheel_place = 86
        self.player_x = pyxel.width / 2 - self.player_width / 2
    
   
    def update(self):
        self.p = self.coordonnees()
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 5:
            self.player_x -= self.player_speed
        if (
            pyxel.btn(pyxel.KEY_RIGHT)
            and self.player_x < screen_width - self.player_width - 5
        ):
            self.player_x += self.player_speed

     def coordonnees(self):
        return self.player_x
                
    def draw(self):
        pyxel.blt(
            self.player_x,
            screen_height - self.player_height,
            2,
            16,
            10,
            self.player_width,
            self.player_height,
            pyxel.COLOR_PINK,
        )  #affichage de la moto entière sans le pneu
        pyxel.blt(
            self.player_x + self.wheel_size[0],
            (screen_height
            - self.player_height)
            + self.wheel_place
            + pyxel.frame_count % 18,
            2,
            48,
            160,
            self.wheel_size[0],
            self.wheel_size[1],
        )  #affichage du premier chevron de la roue ( position haute )
        pyxel.blt(
            self.player_x + self.wheel_size[0],
            (screen_height
            - self.player_height)
            + self.wheel_place
            + self.wheel_size[1] + 3
            + pyxel.frame_count % 18,
            2,
            48,
            160,
            self.wheel_size[0],
            self.wheel_size[1],
        )  #affichage du deuxième chevron de la roue ( position centrale )
        if pyxel.frame_count % 18 + 2 * (self.wheel_size[1]+3) < 45:
            pyxel.blt(
                self.player_x + self.wheel_size[0],
                (screen_height
                - self.player_height)
                + self.wheel_place
                + 2*(self.wheel_size[1] + 3)
                + pyxel.frame_count % 18,
                2,
                48,
                160,
                self.wheel_size[0],
                self.wheel_size[1],
            )  #affichage du troisième chevron de la roue ( position basse si possible )
Game()
