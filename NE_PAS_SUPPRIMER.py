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
