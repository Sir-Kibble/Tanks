from player import Player


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
        self.rotateChassis(5)
