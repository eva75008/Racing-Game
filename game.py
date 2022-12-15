import pyxel


class Game:
    def __init__(self):
        pyxel.init(720, 480, title="Retro-racing game", fps=60)
        pyxel.load("graphics.pyxres")
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width

    def draw(self):
        pyxel.cls(12)
        pyxel.blt(x=100, y=100, img=1, u=7, v=0, w=10, h=40, colkey=0)


Game()
