from Tank import Tank
import time
from multiprocessing import Process, Pipe


class Player(Process):
    def __init__(self):
        super(Player, self).__init__()
        self.name = ""
        self.active = False
        self.player_pipe, self.tank_pipe = Pipe()
        self.game_pipe = None
        self.tank = Tank(self.tank_pipe)

    def set_state(
        self,
        name,
        startX,
        startY,
        chassisTheta,
        turretTheta
    ):
        self.name = name
        self.xPosition = startX
        self.yPosition = startY
        self.chassisTheta = chassisTheta
        self.turretTheta = turretTheta
        self.tank.set_state(
            startX,
            startY,
            chassisTheta,
            turretTheta
        )

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def run(self):
        while self.active:
            self.play()
            time.sleep(.01)

    def play(self):
        time.sleep(.1)
    # this is overwritten by child classes

    def set_pipe(self, pipe):
        self.game_pipe = pipe

    def __getGameUpdates(self):
        action = self.game_pipe.recv()
        self.tank.xPosition = action["tankProps"]["xPosition"]
        self.tank.yPosition = action["tankProps"]["yPosition"]
        self.tank.chassisTheta = action["tankProps"]["chassisTheta"]
        self.tank.turretTheta = action["tankProps"]["turretTheta"]
        self.tank.hp = action["tankProps"]["hp"]
        if action["type"] == "kill":
            self.active = False

    def __sendUpdates(self):
        self.game_pipe.send({
            "tankProps": {
                "xPosition": self.tank.xPosition,
                "yPosition": self.tank.yPosition,
                "turretTheta": self.tank.turretTheta,
                "chassisTheta": self.tank.chassisTheta,
                "hp": self.tank.hp,
            }
        })

    def moveDown(self):
        self.__getGameUpdates()
        self.player_pipe.send({
            "type": "moveDown",
            "args": 5
        })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()

    def moveLeft(self):
        self.__getGameUpdates()
        self.player_pipe.send({
            "type": "moveLeft",
            "args": 5
        })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()

    def moveRight(self):
        self.__getGameUpdates()
        self.player_pipe.send({
            "type": "moveRight",
            "args": 5
        })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()

    def rotateChassis(self, degrees):
        self.__getGameUpdates()
        self.player_pipe.send({
            "type": "rotateChassis",
            "args": degrees
        })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()

    def rotateRight(self, degrees):
        exit

    def rotateToAngle(self, angle):
        exit

    def updateSelf(self, updates):
        self.tank.xPosition = updates["xPosition"]
        self.tank.yPosition = updates["yPosition"]
        self.tank.chassisTheta = updates["chassisTheta"]
        self.tank.turretTheta = updates["turretTheta"]
        self.tank.hp = updates["hp"]
