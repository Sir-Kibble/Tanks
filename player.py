from Tank import Tank


class Player:
    def __init__(
        self,
        startX,
        startY,
        chassisTheta,
        turretTheta
    ):
        self.tank = Tank(
            startX,
            startY,
            chassisTheta,
            turretTheta
        )

    def play(self):
        print "moving ", self.tank.xPosition, ", ", self.tank.yPosition
        self.tank.move_down()
        print "now at ", self.tank.xPosition, ", ", self.tank.yPosition
