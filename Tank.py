import pygame
from tankChassis import TankChassis
from tankTurret import TankTurret
#from multiprocessing import Process


class Tank():

    def __init__(
        self,
        startX,
        startY,
        chassisTheta,
        turretTheta,
        pipe
    ):
        #super(Tank, self).__init__()
        self.xPosition = startX
        self.yPosition = startY
        self.chassisTheta = chassisTheta
        self.turretTheta = turretTheta
        self.sprites = pygame.sprite.OrderedUpdates()
        self.chassis = TankChassis()
        self.turret = TankTurret()
        self.update_position()
        self.hp = 100
        self.pipe = pipe

        self.actions = {
            "moveDown": self.move_down()
        }

    def run(self):
        while True:
            print "receiving"
            action = self.pipe.recv()
            #self.actions[action["type"]](action["args"])
            if action["type"] == "moveDown":
                self.move_down()
            updateObject = {
                "xPosition": self.xPosition,
                "yPosition": self.yPosition,
                "chassisTheta": self.chassisTheta,
                "turretTheta": self.turretTheta,
                "hp": self.hp
            }
            self.pipe.send(updateObject)

    def update_position(self):
        self.chassis.rect.x = self.xPosition
        self.chassis.rect.y = self.yPosition
        self.turret.rect.x = self.xPosition
        self.turret.rect.y = self.yPosition

    def move_left(self):
        self.xPosition -= 5
        self.update_position()

    def move_right(self):
        self.xPosition += 5
        self.update_position()

    def move_up(self):
        self.yPosition -= 5
        self.update_position()

    def move_down(self):
        self.yPosition += 5
        self.update_position()

    def render(self, surface):
        self.update_position()
        self.sprites.empty()
        self.sprites.add(self.chassis)
        self.sprites.add(self.turret)
        self.sprites.draw(surface)
        pygame.display.update()
