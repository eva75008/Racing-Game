import pyxel


class Game:
    def __init__(self):
        pyxel.init(720, 480, title="Retro-racing Game", fps=60)
        pyxel.load("graphics.pyxres")
        self.road = Road()
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(12)
        self.road.draw()


class Road:
    def __init__(self):
        self.width1 = -50
        self.width2 = pyxel.width + 50
        self.milestone = Milestone()

    def createRoad(self):
        pyxel.tri(
            self.width1,
            pyxel.height,
            self.width2,
            pyxel.height,
            pyxel.width / 2,
            -200,
            13,
        )

    def outlineRoad(self):
        for x in range(80):
            pyxel.trib(
                self.width1,
                pyxel.height + x,
                self.width2,
                pyxel.height + x,
                pyxel.width / 2,
                -200,
                7,
            )

    def roadLines(self):
        for x in range(200):
            pyxel.trib(
                self.width1,
                pyxel.height + x + 1400,
                self.width2,
                pyxel.height + x + 1400,
                pyxel.width / 2,
                -200,
                7,
            )

    def draw(self):
        self.createRoad()
        self.outlineRoad()
        self.roadLines()
        self.milestone.draw()


class Milestone:
    def __init__(self):
        self.margin_top = 20
        self.spacing = 70
        self.slope = 0.54

    def invertDirection(self, y):
        return abs(y - pyxel.height)

    def draw(self):
        for x in range(2):
            for y in range(self.margin_top, pyxel.height, self.spacing):
                pyxel.blt(
                    x=self.invertDirection(y) * self.slope - 43
                    if x == 1
                    else y * self.slope + 495,
                    y=y,
                    img=1,
                    u=7,
                    v=0,
                    w=10,
                    h=40,
                    colkey=0,
                )


Game()
