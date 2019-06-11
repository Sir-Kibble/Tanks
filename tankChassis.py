import pygame


class TankChassis(pygame.sprite.Sprite):

    def __init__(self):
        super(TankChassis, self).__init__()
        # self.chassis = chassisImage
        # self.turret = turretImage
        self.image = pygame.image.load(
            "/mnt/mole/Projects/Programs/python3/chassis.png",
            "chassis.png"
            ).convert_alpha()

        self.originalImage = self.image
        self.rect = self.image.get_rect()
