import pyxel


class Game:
    def __init__(self):
        pyxel.init(720, 480, title="Retro-racing Game", fps=60)
        pyxel.load("graphics.pyxres")
        self.road = Road()
        self.milestone = Milestones()
        self.daynight = Daynight()
        self.player = Player()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.control()
        self.daynight.systeme()
        self.milestone.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_LIME)
        self.road.draw()
        self.daynight.draw()
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

    def draw(self):
        self.createRoad()
        self.outlineRoad()
        self.createLanes()

        pyxel.circ(self.convergent_point[0], self.convergent_point[1], 8, 0)
        pyxel.circ(self.convergent_point[0] - 2, self.convergent_point[1] - 2, 2, 7)

        pyxel.rect(0, 0, pyxel.width, self.end_road, pyxel.COLOR_CYAN)


class Player:
    def __init__(self):
        self.x = pyxel.width / 2 - 95 / 2
        self.width = 95
        self.height = 150
        self.time = 0
        self.delta = 0


    def control(self):
        right = pyxel.width - self.width * 2
        middle = pyxel.width / 2 - self.width / 2
        left = self.width
        self.time += 1
        self.dir = middle
        mouvement = None


        if self.time >= self.delta + 45:   #permet d'imposer un delay de 45/60s avant de se deplacer
            if pyxel.btnp(pyxel.KEY_RIGHT):
                mouvement = right
                self.delta = self.time   #la variable delta prend la valeur actuelle du temps
                if self.x == middle:
                    self.x = right
                if self.x == right:
                    self.x = right
                if self.x == left:
                    self.x = middle
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.delta = self.time  #la variable delta prend la valeur actuelle du temps
                if self.x == middle:
                    self.x = left
                if self.x == left:
                    self.x = left
                if self.x == right:
                    self.x = middle

    def right(self):
        self.x +=5
                    
                    
                        
    def update(self):
        mouvement()
        self.control()

    def draw(self):
        """
        affiche la moto en x y par l'image en ressource en u v de taille w h et couleur transparente : 14
        """
        pyxel.blt(
            x=self.x,
            y=pyxel.height - self.height,
            img=2,
            u=16,
            v=10,
            w=95,
            h=149,
            colkey=14,
        )


class Daynight:
    def __init__(self):
        self.systemposx = 1
        self.systemposy = 100
        self.u = 6
        self.v = 22
        self.end_road = pyxel.height / 2
        self.day = True

    def systeme(self):
        self.systemposx += 1
        self.systemposy = -(pyxel.sin((180 * self.systemposx) / 720)) * 200 + 215
        if self.systemposx >= 720:
            self.day = not self.day
            if self.day:
                self.systemposx = 1
                self.u = 6
                self.v = 22
            else:
                self.systemposx = 1
                self.u = 6
                self.v = 44

        pyxel.blt(
            x=self.systemposx,
            y=self.systemposy,
            img=0,
            u=self.u,
            v=self.v,
            w=22,
            h=22,
            colkey=0,
        )

    def draw(self):
        pyxel.rect(
            0,
            0,
            pyxel.width,
            self.end_road,
            pyxel.COLOR_CYAN if self.day else pyxel.COLOR_NAVY,
        )

        self.systeme()


class Milestones(Road):
    def __init__(self):
        self.min_height = 8
        self.min_width = 2
        self.scaling_step = 1.5
        self.start = 10
        super().__init__()

    def update(self):
        pass

    def findSlope(self, x0, y0):
        return (y0 - self.convergent_point[1]) / (x0 - self.convergent_point[0])

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


Game()
Footer
