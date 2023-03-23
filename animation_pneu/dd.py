import pyxel
import math
from random import randint

screen_width = 720
screen_height = 480
convergence = [screen_width // 2, 200]
sky_height = screen_height // 2

class Game:

    def __init__(self):
        pyxel.init(screen_width, screen_height, "Retro-racing Game", 60)
        pyxel.load("zzae.pyxres")
        self.road = Road()
        self.milestone = Milestones()
        self.timeOfDay = TimeOfDay()
        self.varx = self.timeOfDay.x
        self.player = Player()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.road.update()
        self.timeOfDay.update()
        self.milestone.update()
        self.varx = self.timeOfDay.x
        self.player.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_LIME)
        self.road.draw()
        self.timeOfDay.draw()
        self.milestone.draw()
        self.player.draw(self.varx)


class Road:
    def __init__(self, overflow_x=200, line_thickness=40):
        self.overflowX = overflow_x
        self.line_thickness = line_thickness
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
    def __init__(self):
        (self.x, self.y) = convergence
        self.scaling_factor = 0.05
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
        if self.y > screen_height + self.calculateRadius(self.y, 5):
            self.y = convergence[1]
            self.x = convergence[0]
            self.trajectory = randint(-1, 1)

    def draw(self):
        pyxel.circ(self.x, self.y, self.calculateRadius(self.y, 10), pyxel.COLOR_BLACK)
        pyxel.circ(self.x, self.y, self.calculateRadius(self.y, 8), pyxel.COLOR_WHITE)


class TimeOfDay:
    def __init__(self, speed=1):
        self.speed = speed
        self.x = 1
        self.y = 100
        self.width = 22
        self.graphicsPositionX = 22
        self.day = True

    def update(self):
        self.x += self.speed
        self.y = 200 * math.sin(math.radians(-180 * self.x / screen_width)) + 200
        if self.x > screen_width:
            self.day = not self.day
            self.x = 1
            if self.day:
                self.graphicsPositionX = 22
            else:
                self.graphicsPositionX = 44

    def draw(self):
        pyxel.rect(
            0,
            0,
            screen_width,
            sky_height,
            pyxel.COLOR_CYAN if self.day else pyxel.COLOR_NAVY,
        )

        pyxel.blt(
            self.x,
            self.y,
            0,
            6,
            self.graphicsPositionX,
            22,
            22,
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
        return abs(math.sqrt(slope ** 2 + 1) * (x0 - convergence[0]))

    def findX(self, y0, slope):
        return (y0 - convergence[1]) / slope + convergence[0]

    def right(self):
        slope = self.findSlope(screen_width - self.start, 375)
        total_distance = self.findDistance(self.start, slope)
        cper_dist = self.findDistance(self.findX(sky_height, slope), slope)
        scaling_factor = 1
        distance = cper_dist
        while distance < total_distance:
            x = distance / (slope ** 2 + 1) ** (1 / 2) + convergence[0]
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
            x = -distance / (slope ** 2 + 1) ** (1 / 2) + convergence[0]
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
        self.x = screen_width / 2 - 95 / 2
        self.width = 95
        self.height = 150

    def update(self):
        right = screen_width - self.width * 2
        middle = screen_width / 2 - self.width / 2
        left = self.width

        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self.x == middle:
                self.x = right
            if self.x == right:
                self.x = right
            if self.x == left:
                self.x = middle
        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.x == middle:
                self.x = left
            if self.x == left:
                self.x = left
            if self.x == right:
                self.x = middle


    def draw(self, varx):
        pyxel.blt(
            x=self.x,
            y=screen_height - self.height,
            img=2,
            u=16,
            v=10,
            w=self.width,
            h=self.height,
            colkey=pyxel.COLOR_PINK,
        )
        print(varx)
        if (varx)%60<=30:
            pyxel.blt(
                x=self.x+32,
                y=(screen_height - self.height)+95,
                img=2,
                u=48,
                v=160,
                w=33,
                h=42,
                colkey=pyxel.COLOR_PINK,
            )


Game()
