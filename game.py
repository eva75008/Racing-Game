import pyxel


class Game:
    def __init__(self):
        pyxel.init(720, 480, title="Retro-racing Game", fps=60)
        # pyxel.load("graphics.pyxres")
        self.road = Road()
        self.milestone = Milestones()
        pyxel.run(self.update, self.draw)

    def update(self):
        # make milestones move
        self.milestone.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_LIME)
        self.road.draw()
        self.milestone.draw()


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

    def draw(self):
        self.createRoad()
        self.outlineRoad()
        self.createLanes()
        pyxel.rect(0, 0, pyxel.width, self.end_road, pyxel.COLOR_CYAN)


class Milestones(Road):
    def __init__(self):
        self.difference = pyxel.width - 10
        self.height = 35
        self.width = 8
        super().__init__()

    def update(self):
        # make the milestones move in the direction of the road
        pass

    def f(self, x):
        return (
            (x - self.convergent_point[0])
            / (-self.overflow_x - self.convergent_point[0])
        ) * (pyxel.height - self.convergent_point[1]) + self.convergent_point[1]

    def g(self, x):
        return (
            (x - self.convergent_point[0])
            / (pyxel.width + self.overflow_x - self.width - 10 - self.convergent_point[0])
        ) * (pyxel.height - self.convergent_point[1]) + self.convergent_point[1]

    def right(self):
        x = pyxel.width - 10 - self.width
        while x > 440:
            y = self.g(x)
            pyxel.rect(x, y - self.height, self.width, self.height, pyxel.COLOR_RED)
            # pyxel.rect(x, y, 10 - x / 30, 60 - x / 6, pyxel.COLOR_RED)
            pyxel.rect(x, y - self.height + 4, 8, 5, pyxel.COLOR_WHITE)
            x -= 1

    def left(self):
        x = 10
        while x < 280:
            y = self.f(x)
            pyxel.rect(x, y - self.height, self.width, self.height, pyxel.COLOR_RED)
            # pyxel.rect(x, y, 10 - x / 30, 60 - x / 6, pyxel.COLOR_RED)
            pyxel.rect(x, y - self.height + 4, 8, 5, pyxel.COLOR_WHITE)
            x += 1

    def draw(self):
        self.right()
        self.left()


Game()
