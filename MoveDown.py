from Player import Player


class MoveDown(Player):

    def __init__(self):
        super(MoveDown, self).__init__()

    def play(self):
        self.moveDown()
        self.moveDown()
        self.moveDown()
        self.moveDown()
