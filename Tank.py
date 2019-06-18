import pygame
from tankChassis import TankChassis
from tankTurret import TankTurret
#from multiprocessing import Process


class Tank():

    def __init__(
        self,
        pipe,
        xPosition,
        yPosition,
        chassisTheta,
        turretTheta
    ):
        #super(Tank, self).__init__()
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.chassisTheta = chassisTheta
        self.turretTheta = turretTheta
        self.cannonIsLoaded = True
        self.reloadTime = 2
        self.sprites = pygame.sprite.OrderedUpdates()
        self.chassis = TankChassis()
        self.turret = TankTurret()
        self.update_position()
        self.hp = 100
        self.pipe = pipe

    def set_state(
        self,
        startX,
        startY,
        chassisTheta,
        turretTheta
    ):
        self.startX = startX
        self.startY = startY
        self.chassisTheta = chassisTheta
        self.turretTheta = turretTheta

    def run(self):
        while True:
            action = self.pipe.recv()
            # self.actions[action["type"]](action["args"])
            if action["type"] == "moveDown":
                self.move_down(action["args"])
            elif action["type"] == "moveUp":
                self.move_up(action["args"])
            elif action["type"] == "moveLeft":
                self.move_left(action["args"])
            elif action["type"] == "moveRight":
                self.move_right(action["args"])
            elif action["type"] == "rotateChassis":
                self.rotateChassis(action["args"])
            elif action["type"] == "rotateTurret":
                self.rotateTurret(action["args"])
            updateObject = {
                "xPosition": self.xPosition,
                "yPosition": self.yPosition,
                "chassisTheta": self.chassisTheta,
                "turretTheta": self.turretTheta,
                "hp": self.hp,
            }
            self.pipe.send(updateObject)

    def update_position(self):
        self.chassis.rect.x = self.xPosition
        self.chassis.rect.y = self.yPosition
        self.turret.rect.x = self.xPosition
        self.turret.rect.y = self.yPosition

    def move_left(self, distance):
        self.xPosition -= distance
        self.update_position()

    def move_right(self, distance):
        self.xPosition += distance
        self.update_position()

    def move_up(self, distance):
        self.yPosition -= distance
        self.update_position()

    def move_down(self, distance):
        self.yPosition += distance
        self.update_position()

    def rotateChassis(self, angle):
        self.chassisTheta += angle % 360

    def rotateTurret(self, angle):
        self.turretTheta += angle % 360

    def readySprites(self, screen, pos):
        self.update_position()
        self.sprites.empty()
        self.chassis.image = rot_center(self.chassis.originalImage, self.chassisTheta)
        self.turret.image = rot_center(self.turret.originalImage, self.turretTheta)
        self.sprites.add(self.chassis)
        self.sprites.add(self.turret)
        self.sprites.draw(screen)
        pygame.display.update()


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
