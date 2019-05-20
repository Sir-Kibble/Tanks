from Tank import Tank
import time
from multiprocessing import Process, Pipe


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
        self.active = True
        self.player_pipe, self.tank_pipe = Pipe()
        self.game_pipe = None
        self.tank = Tank(
            startX,
            startY,
            chassisTheta,
            turretTheta,
            self.tank_pipe
        )

    def run(self):
        while self.active:
            print self.name, " is moving down..."
            self.getGameUpdates()
            self.moveDown()
            time.sleep(1)
            self.sendUpdates()
            #print self.name, " now at ", self.tank.xPosition, ", ", self.tank.yPosition

    def set_pipe(self, pipe):
        self.game_pipe = pipe

    def getGameUpdates(self):
        action = self.game_pipe.recv()
        self.tank.xPosition = action["tankProps"]["xPosition"]
        self.tank.yPosition = action["tankProps"]["yPosition"]
        self.tank.chassisTheta = action["tankProps"]["chassisTheta"]
        self.tank.turretTheta = action["tankProps"]["turretTheta"]
        self.tank.hp = action["tankProps"]["hp"]
        if action["type"] == "kill":
            self.active = False

    def sendUpdates(self):
        self.game_pipe.send({
            "tankProps": {
                "xPosition": self.tank.xPosition,
                "yPosition": self.tank.yPosition,
                "turretTheta": self.tank.turretTheta,
                "chassisTheta": self.tank.chassisTheta,
                "hp": self.tank.hp
            }
        })

    def moveDown(self):
        self.player_pipe.send({
            "type": "moveDown",
            "args": 5
        })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)

    def updateSelf(self, updates):
        self.tank.xPosition = updates["xPosition"]
        self.tank.yPosition = updates["yPosition"]
        self.tank.chassisTheta = updates["chassisTheta"]
        self.tank.turretTheta = updates["turretTheta"]
        self.tank.hp = updates["hp"]
