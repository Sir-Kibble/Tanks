import pygame
from tankChassis import TankChassis
from tankTurret import TankTurret
import math
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
        self.reloadTime = 100
        self.sprites = pygame.sprite.OrderedUpdates()
        self.chassis = TankChassis()
        self.turret = TankTurret()
        self.hp = 100
        self.pipe = pipe
        self.collisionRect = pygame.Rect(xPosition, yPosition, 40, 40)
        self.update_position()

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
            # reload cannon if needed
            if not self.cannonIsLoaded:
                self.reloadTime -= 1

            if self.reloadTime < 1:
                self.cannonIsLoaded = True
                self.reloadTime = 100

            # self.actions[action["type"]](action["args"])
            if action["type"] == "fireCannon":
                self.fire_cannon()
            elif action["type"] == "moveDown":
                self.move_down(action["args"])
            elif action["type"] == "moveUp":
                self.move_up(action["args"])
            elif action["type"] == "moveLeft":
                self.move_left(action["args"])
            elif action["type"] == "moveRight":
                self.move_right(action["args"])
            elif action["type"] == "moveForwards":
                self.move_forwards(action["args"])
            elif action["type"] == "moveBackwards":
                self.move_backwards(action["args"])
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
                "cannonIsLoaded": self.cannonIsLoaded
            }
            self.pipe.send(updateObject)

    def update_position(self):
        self.chassis.rect.x = self.xPosition
        self.chassis.rect.y = self.yPosition
        self.turret.rect.x = self.xPosition
        self.turret.rect.y = self.yPosition
        self.collisionRect.move(self.xPosition, self.yPosition)

    def fire_cannon(self):
        if self.cannonIsLoaded:
            print "\n\nFIRE!!!!!!!!!!!\n\n"
            self.cannonIsLoaded = False


    def move_forwards(self, distance):
        self.yPosition += math.sin((self.chassisTheta * math.pi) / 180) * distance
        self.xPosition += math.cos((self.chassisTheta * math.pi) / 180) * distance
        self.update_position()

    def move_backwards(self, distance):
        self.yPosition -= math.sin((self.chassisTheta * math.pi) / 180) * distance
        self.xPosition -= math.cos((self.chassisTheta * math.pi) / 180) * distance
        self.update_position()

    def rotateChassis(self, angle):
        self.chassisTheta += angle % 360

    def rotateTurret(self, angle):
        self.turretTheta += angle % 360

    def readySprites(self, screen, pos):
        self.update_position()
        self.sprites.empty()
        # doing negative rotations as it seems to work properlys
        self.chassis.image = rot_center(self.chassis.originalImage, -1 * self.chassisTheta)
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
