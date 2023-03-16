import pyxel
import math
import random


class Game:
    def __init__(self):
        pyxel.init(720, 480, title="Retro-racing Game", fps=60)
        pyxel.load("graphics.pyxres")
        self.road = Road()
        self.milestone = Milestones()
        self.timeOfDay = TimeOfDay()
        self.player = Player()
        self.ennemies = Ennemies()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.ennemies.update()
        self.timeOfDay.update()
        self.milestone.update()
        self.player.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_LIME)
        self.road.draw()
        self.ennemies.draw()
        self.timeOfDay.draw()
        self.milestone.draw()
        self.player.draw()


class Road:
    def __init__(self):
        self.convergent_point = [pyxel.width / 2, 200]
        self.overflow_x = 200
        self.line_thickness = 40
        self.end_road = pyxel.height / 2

    def createRoad(self):
        pyxel.tri(
            -self.overflow_x,
            pyxel.height,
            pyxel.width + self.overflow_x,
            pyxel.height,
            self.convergent_point[0],
            self.convergent_point[1],
            pyxel.COLOR_GRAY,
        )

    def outlineRoad(self):
        for n in range(2):
            for x in range(self.line_thickness):
                pyxel.line(
                    -self.overflow_x if n else pyxel.width + self.overflow_x,
                    pyxel.height + x,
                    self.convergent_point[0],
                    self.convergent_point[1],
                    pyxel.COLOR_WHITE,
                )

    def createLanes(self):
        for n in range(1, 3):
            for x in range(self.line_thickness):
                pyxel.line(
                    pyxel.width / 3 * n
                    + (self.line_thickness if n == 2 else -self.line_thickness),
                    pyxel.height + x,
                    self.convergent_point[0],
                    self.convergent_point[1],
                    pyxel.COLOR_WHITE,
                )

    def findSlope(self, x0, y0):
        return (y0 - self.convergent_point[1]) / (x0 - self.convergent_point[0])

    def draw(self):
        self.createRoad()
        self.outlineRoad()
        self.createLanes()


class Ennemies(Road):
    def __init__(self):
        super().__init__()
        self.x = self.convergent_point[0]
        self.y = self.convergent_point[1]
        self.scaling_factor = 0.05
        self.trajectory = random.choice([-1, 0, 1])

    def calculateRadius(self, y, initial_size):
        y -= self.convergent_point[1]
        return self.scaling_factor * y + initial_size

    def increaseSpeed(self, y, initial_speed):
        y -= self.convergent_point[1] - 1
        return initial_speed * y / 15

    def update(self):
        self.y += self.increaseSpeed(self.y, 1)
        self.x += self.trajectory * self.increaseSpeed(self.y, 1)
        if self.y > pyxel.height + self.calculateRadius(self.y, 5):
            self.y = self.convergent_point[1]
            self.x = self.convergent_point[0]
            self.trajectory = random.choice([-1, 0, 1])

    def draw(self):
        pyxel.circ(self.x, self.y, self.calculateRadius(self.y, 5), pyxel.COLOR_BLACK)
        pyxel.circ(self.x, self.y, self.calculateRadius(self.y, 5), pyxel.COLOR_WHITE)


class TimeOfDay(Road):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.width = 22
        self.y = 100
        self.graphicsPositionX = 22
        self.day = True

    def update(self):
        self.speed += 1
        self.y = 200 * math.sin(-math.pi * self.speed / pyxel.width) + 200
        if self.speed > pyxel.width:
            self.day = not self.day
            self.speed = 1
            if self.day:
                self.graphicsPositionX = 22
            else:
                self.graphicsPositionX = 44

    def draw(self):
        pyxel.rect(
            0,
            0,
            pyxel.width,
            self.end_road,
            pyxel.COLOR_CYAN if self.day else pyxel.COLOR_NAVY,
        )
        pyxel.blt(
            self.speed, self.y, 0, 6, self.graphicsPositionX, 22, 22, pyxel.COLOR_BLACK
        )


class Milestones(Road):
    def __init__(self):
        self.min_height = 8
        self.min_width = 2
        self.scaling_step = 1.5
        self.start = 10
        super().__init__()

    def update(self):
        pass

    def findDistance(self, x0, slope):
        return abs(((slope**2 + 1) ** (1 / 2)) * (x0 - self.convergent_point[0]))

    def findX(self, y0, slope):
        return (y0 - self.convergent_point[1]) / slope + self.convergent_point[0]

    def right(self):
        slope = self.findSlope(pyxel.width - self.start, 375)
        total_distance = self.findDistance(self.start, slope)
        cper_dist = self.findDistance(self.findX(self.end_road, slope), slope)
        scaling_factor = 1
        distance = cper_dist
        while distance < total_distance:
            x = (distance / ((slope**2 + 1) ** (1 / 2))) + self.convergent_point[0]
            y = slope * (x - self.convergent_point[0]) + self.convergent_point[1]
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
            distance += ((total_distance - cper_dist) / 8) * scaling_factor
            scaling_factor += self.scaling_step

    def left(self):
        slope = self.findSlope(self.start, 375)
        total_distance = self.findDistance(self.start, slope)
        cper_dist = self.findDistance(self.findX(self.end_road, slope), slope)
        scaling_factor = 1
        distance = cper_dist
        while distance < total_distance:
            x = (-distance / ((slope**2 + 1) ** (1 / 2))) + self.convergent_point[0]
            y = slope * (x - self.convergent_point[0]) + self.convergent_point[1]
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
            distance += ((total_distance - cper_dist) / 8) * scaling_factor
            scaling_factor += self.scaling_step

    def draw(self):
        self.right()
        self.left()


class Player:
    def __init__(self):
        self.x = pyxel.width / 2 - 95 / 2
        self.width = 95
        self.height = 150
	#position du joueur dans la liste des positions possibles
        self.playerposition = 2
	

    def update(self):
        #definition des positions possibles du joueur
        positions = [self.width, 200, pyxel.width / 2 - self.width / 2, 425, pyxel.width - self.width * 2 ]

	#lorqu'un touche 'flèche' est appuyée, le joueur passe à la position possible la plus proche
        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self.playerposition < 4: 
                self.playerposition += 1
                self.x = positions[self.playerposition]
        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.playerposition > 0: 
                self.playerposition += -1
                self.x = positions[self.playerposition]

    def draw(self):
        pyxel.blt(
            x=self.x,
            y=pyxel.height - self.height,
            img=2,
            u=16,
            v=10,
            w=self.width,
            h=self.height,
            colkey=pyxel.COLOR_PINK,
        )





Game()
