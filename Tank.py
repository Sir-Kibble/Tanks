import pygame
from tankChassis import TankChassis
from tankTurret import TankTurret


class Tank:

    def __init__(
        self,
        startX,
        startY,
        chassisTheta,
        turretTheta
    ):
        self.xPosition = startX
        self.yPosition = startY
        self.chassisTheta = chassisTheta
        self.turretTheta = turretTheta
        self.sprites = pygame.sprite.OrderedUpdates()
        self.chassis = TankChassis()
        self.turret = TankTurret()
        self.update_position()
        self.hp = 100

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
        self.sprites.empty()
        self.sprites.add(self.chassis)
        self.sprites.add(self.turret)
        self.sprites.draw(surface)
