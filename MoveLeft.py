from player import Player
import random


class MoveLeft(Player):

    def __init__(
        self,
        name,
        xPosition,
        yPosition,
        chassisTheta,
        turretTheta
    ):
        super(MoveLeft, self).__init__(
            name,
            xPosition,
            yPosition,
            chassisTheta,
            turretTheta
        )

    def play(self):
        self.moveForwards()
        self.fireCannon()
        self.rotateChassis(random.randint(-5, 3))
