from Tank import Tank
import time
import pygame
import math
from multiprocessing import Process, Pipe


class Player(Process):
    def __init__(
        self,
        name,
        xPosition,
        yPosition,
        chassisTheta,
        turretTheta
    ):
        super(Player, self).__init__()
        self.name = name
        self.active = False
        self.player_pipe, self.tank_pipe = Pipe()
        self.game_pipe = None
        self.gameState = {}
        self.tank = Tank(
            self.tank_pipe,
            xPosition,
            yPosition,
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

    # this is overwritten by child classes
    def play(self):
        time.sleep(.1)

    def set_pipe(self, pipe):
        self.game_pipe = pipe

    def __getGameUpdates(self):
        self.gameState = self.game_pipe.recv()
        for key in self.gameState["gameState"]["tanks"]:
            if key["name"] == self.name:
                self.tank.xPosition = key["xPosition"]
                self.tank.yPosition = key["yPosition"]
                self.tank.chassisTheta = key["chassisTheta"]
                self.tank.turretTheta = key["turretTheta"]
                self.tank.hp = key["hp"]
                self.tank.cannonIsLoaded = key["cannonIsLoaded"]
        # if gameState["type"] == "kill":
        #     self.active = False

    def __sendUpdates(self):
        self.game_pipe.send({
            "tankProps": {
                "xPosition": self.tank.xPosition,
                "yPosition": self.tank.yPosition,
                "turretTheta": self.tank.turretTheta,
                "chassisTheta": self.tank.chassisTheta,
                "hp": self.tank.hp,
                "cannonIsLoaded": self.tank.cannonIsLoaded
            }
        })

    # size is hardcoded in get_legal_distance, 600x400
    def moveForwards(self):
        self.__getGameUpdates()
        distance = get_legal_distance(
            self.name,
            self.gameState["gameState"],
            5,
            600,
            400
        )
        self.player_pipe.send({
            "type": "moveForwards",
            "args": distance
        })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()
        if (distance == 0):
            return False
        return True

    def moveBackwards(self):
        self.__getGameUpdates()
        distance = get_legal_distance(
            self.name,
            self.gameState["gameState"],
            5,
            600,
            400
        )
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()
        if (distance == 0):
            return False
        return True

    def fireCannon(self):
        self.__getGameUpdates()
        if self.tank.cannonIsLoaded:
            self.player_pipe.send({
                "type": "fireCannon",
            })
        else:
            self.player_pipe.send({
                "type": "pass",
            })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()

    def rotateChassis(self, degrees):
        if(degrees == 0):
            return
        degreesTemp = abs(degrees)
        direction = (abs(degrees) / degrees)
        theta = 10 * direction
        while(degreesTemp > 0):
            if(degreesTemp < 10):
                theta = degreesTemp * direction
            self.__getGameUpdates()
            self.player_pipe.send({
                "type": "rotateChassis",
                "args": theta
            })
            updates = self.player_pipe.recv()
            self.updateSelf(updates)
            self.__sendUpdates()
            degreesTemp -= 10

    def rotateTurret(self, degrees):
        degreesTemp = abs(degrees)
        direction = (abs(degrees) / degrees)
        theta = 10 * direction
        while(degreesTemp > 0):
            if(degreesTemp < 10):
                theta = degreesTemp * direction
            self.__getGameUpdates()
            self.player_pipe.send({
                "type": "rotateTurret",
                "args": theta
            })
            updates = self.player_pipe.recv()
            self.updateSelf(updates)
            self.__sendUpdates()
            degreesTemp -= 10

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
        self.tank.cannonIsLoaded = updates["cannonIsLoaded"]


def get_legal_distance(playerName, gameState, distance, xMax, yMax):
    for key in gameState["tanks"]:
        if key["name"] == playerName:
            keyCollisionRect = pygame.Rect(
                key["xPosition"]+9+math.cos((key["chassisTheta"] * math.pi) / 180) * distance,
                key["yPosition"]+9+math.sin((key["chassisTheta"] * math.pi) / 180) * distance,
                40,
                40
            )
            for checkKey in gameState["tanks"]:
                checkKeyCollisionRect = pygame.Rect(
                    checkKey["xPosition"]+9,
                    checkKey["yPosition"]+9,
                    40,
                    40
                )
                if checkKey["name"] == playerName:
                    continue
                # check bounds
                if (
                    keyCollisionRect.x < 0
                    or keyCollisionRect.x > xMax
                    or keyCollisionRect.y < 0
                    or keyCollisionRect.y > yMax
                ):
                    return 0
                if keyCollisionRect.colliderect(checkKeyCollisionRect):
                    return 0
    return distance
