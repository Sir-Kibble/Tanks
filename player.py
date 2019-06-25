from Tank import Tank
import time
import pygame
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
            }
        })

    # invoked before all move actions to handle collisions gracefully
    # returns how far tank can be moved
    def check_move_legality(self, direction):
        print direction
        if direction == "left":
            # look through all players and see if
            # the have an x value within current player move distance
            # remmeber that the sprites are padded for rotation
            # 58x58 with 9px padding on each side
            # print self.gameState["gameState"]["players"]
            for key in self.gameState["gameState"]["tanks"]:
                if key["name"] == self.name:
                    keyCollisionRect = pygame.Rect(key["xPosition"]+9, key["yPosition"]+9, 40, 40)
                    for checkKey in self.gameState["gameState"]["tanks"]:
                        checkKeyCollisionRect = pygame.Rect(checkKey["xPosition"]+9, checkKey["yPosition"]+9, 40, 40)
                        if checkKey["name"] == self.name:
                            continue
                        if keyCollisionRect.colliderect(checkKeyCollisionRect):
                            print "collission!"
                            return 0
                    # if key["xPosition"]+49 - self.tank.xPosition < 5 and key["xPosition"]+49 - self.tank.xPosition >= 0:
                    #     print "hit x!!!!!"
                    #     if key["yPosition"] - self.tank.yPosition < 49 and key["yPosition"]+49 - self.tank.yPosition >= 0:
                    #         print "hit y!!!!!!1111"
                    #         print key["xPosition"]+49 - self.tank.xPosition
                    #         return key["xPosition"]+49 - self.tank.xPosition
        return 1

    def moveDown(self):
        self.__getGameUpdates()
        self.player_pipe.send({
            "type": "moveDown",
            "args": 1
        })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()

    def moveLeft(self):
        self.__getGameUpdates()
        self.player_pipe.send({
            "type": "moveLeft",
            "args": self.check_move_legality("left")
        })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()

    def moveRight(self):
        self.__getGameUpdates()
        self.player_pipe.send({
            "type": "moveRight",
            "args": 1
        })
        updates = self.player_pipe.recv()
        self.updateSelf(updates)
        self.__sendUpdates()

    def rotateChassis(self, degrees):
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
