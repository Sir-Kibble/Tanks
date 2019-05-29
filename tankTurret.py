import pygame


class TankTurret(pygame.sprite.Sprite):

    def __init__(self):
        super(TankTurret, self).__init__()
        # self.chassis = chassisImage
        # self.turret = turretImage
        self.image = pygame.image.load(
            "/mnt/mole/Projects/Programs/python3/turret.png",
            "turret.png"
            ).convert_alpha()

        self.originalImage = self.image
        self.rect = self.image.get_rect()
