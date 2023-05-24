import pyxel
from math import sin, radians, sqrt
from random import uniform


screen_width = 720
screen_height = 480
convergence = (screen_width / 2, 200)
sky_height = screen_height / 2


class Game:
    def __init__(self):
        pyxel.init(screen_width, screen_height, "Retro-racing Game", 60)
        pyxel.load("graphic.pyxres")
        self.road = Road()
        self.milestonel = Milestones(0)
        self.milestoner = Milestones(720)
        self.timeOfDay = TimeOfDay()
        self.score = 0
        self.player = Player(self)
        self.enemy_timer = 0
        self.enemies = Enemies(self.player)
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def init_score(self):
        self.score = 0

    def update(self):
        self.score += 0.1
        self.timeOfDay.update()
        self.milestonel.update()
        self.milestoner.update()
        self.player.update()
        self.enemies.update()
        self.enemy_timer += 1
        if self.enemy_timer >= 20:
            self.enemies.create_enemy()
            self.enemy_timer = 0

    def draw(self):
        pyxel.cls(pyxel.COLOR_LIME)
        self.road.draw()
        self.enemies.draw()
        self.timeOfDay.draw()
        self.milestonel.draw()
        self.milestoner.draw()
        self.player.draw()
        pyxel.text(10, 10, f"Score: {int(self.score)}", pyxel.COLOR_WHITE)


class Road:
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
    def __init__(self, player, number=3):
        self.player = player
        self.enemies = []
        self.scaling_factor = 0.05

    def calculate_radius(self, y, initial_size):
        y -= convergence[1]
        return self.scaling_factor * y + initial_size

    def increase_speed(self, y, initial_speed):
        y -= convergence[1] - 1
        return initial_speed * 2 ** (y / 60)

    def create_enemy(self):
        enemy = {
            "x": convergence[0],
            "y": convergence[1],
            "trajectory": uniform(1.6, -1.6),
        }
        self.enemies.append(enemy)

    def update(self):
        for enemy in self.enemies:
            enemy["y"] += self.increase_speed(enemy["y"], 1)
            enemy["x"] += enemy["trajectory"] * self.increase_speed(enemy["y"], 1)
            if enemy["y"] > screen_height + self.calculate_radius(enemy["y"], 8):
                self.enemies.remove(enemy)

            # Check collision with player
            if self.check_collision(enemy):
                self.player.onCollision()

    def check_collision(self, enemy):
        # Calculate the radius of the ball used in the collision detection
        radius = self.calculate_radius(enemy["y"], 8)

        # Calculate the dimensions of the player rectangle used in the collision detection
        x = self.player.x + self.player.width * 0.3
        y = self.player.y + self.player.height * 0.3
        width = self.player.width * 0.4
        height = self.player.height * 0.4

        # Check if the ball collides with the player
        return (
            enemy["x"] + radius >= x
            and enemy["x"] - radius <= x + width
            and enemy["y"] + radius >= y
            and enemy["y"] - radius <= y + height
        )

    def draw(self):
        for enemy in self.enemies:
            pyxel.circ(
                enemy["x"],
                enemy["y"],
                self.calculate_radius(enemy["y"], 8),
                pyxel.COLOR_WHITE,
            )


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
    def __init__(self, game):
        self.game = game
        self.width = 95
        self.height = 150
        self.player_speed = 10
        self.wheel_size = (32, 15)
        self.wheel_speed = 18  # the lower the faster and wheel_speed <= 18
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height

    def update(self):
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q)) and self.x > 5:
            self.x -= self.player_speed
        if (
            (pyxel.btn(pyxel.KEY_RIGHT)
            or pyxel.btn(pyxel.KEY_D))
            and self.x < screen_width - self.width - 5
        ):
            self.x += self.player_speed
    
    def restart(self):
        while not pyxel.btn(KEY_SPACE):
            pyxel.cls(8)
            text(320, 210, "Click on SPACE to RESTART", 7)
   
            
            
    def onCollision(self):
        pyxel.play(2, 2)
        self.game.init_score()
        restart()
        

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
