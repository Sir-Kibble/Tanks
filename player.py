from Tank import Tank
import time
from multiprocessing import Process


class Player(Process):
    def __init__(
        self,
        name,
        startX,
        startY,
        chassisTheta,
        turretTheta
    ):
        super(Player, self).__init__()
        self.name = name
        self.active = False
        self.tank = Tank(
            startX,
            startY,
            chassisTheta,
            turretTheta
        )

    def toggle(self, active):
        self.activate = active

    def run(self):
        while True:
            print self.name, " active? ", self.active
            if self.active:
                print self.name, " moving ", self.tank.xPosition, ", ", self.tank.yPosition
                self.tank.move_down()
                #print self.name, " now at ", self.tank.xPosition, ", ", self.tank.yPosition
            else:
                #print self.name, " is sleeping"
                time.sleep(.1)
