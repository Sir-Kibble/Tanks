from Player import Player


class MoveDown(Player):

    def __init__(
        self,
        name,
        xPosition,
        yPosition,
        chassisTheta,
        turretTheta
    ):
        super(MoveDown, self).__init__(
            name,
            xPosition,
            yPosition,
            chassisTheta,
            turretTheta
        )

    def play(self):
        self.rotateTurret(1)
