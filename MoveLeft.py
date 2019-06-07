from Player import Player


class MoveLeft(Player):

    def __init__(self):
        super(MoveLeft, self).__init__()

    def play(self):
        self.moveRight()
        self.rotateTurret(-35)
        self.rotateChassis(-20)
