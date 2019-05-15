#!/usr/bin/env python
import pygame
import time
from multiprocessing import Process


class TankGame:
    WHITE = (234, 234, 234)

    def __init__(self):
        pygame.init()
        self.size = (640, 400)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("TankWorld runner")
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen.fill(self.WHITE)

    # tank1 = Tank(100, 100, 0, 0)
    # player1 = Player(100, 100, 0, 0)

    def set_players(self, players):
        self.players = players

    def run(self):
        playerProcesses = []
        for player in self.players:
            print "adding player process"
            playerProcesses.append(player)

        # for process in playerProcesses:
        #     if process.is_alive() is not True:
        #         print "pid: ", process.is_alive
        #         process.start()
        #         print "pid: ", process.pid, " has started"

        while self.running:
            timeout = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.WHITE)
            print "processing..."
            for player in self.players:
                print "Player ", player.name, " is active"
                player .start()
                print player.active
                start = time.time()

                while time.time() - start <= timeout:
                    #print "sleeping"
                    time.sleep(.5)
                print "Player", player.name, " is inactive"
                #player.toggle(False)
                player.terminate()
            # player1.tank.render(screen)
                print player.name, " tank: ", player.tank.yPosition
            #print "player1 tank: ", self.players[1].tank.yPosition

            self.enforce_rules()
            print "draw_updates"
            self.draw_updates()
            pygame.display.update()
            pygame.event.pump()
            self.clock.tick(10)
        pygame.quit()
        return 1

    def draw_updates(self):
        for player in self.players:
            player.tank.render(self.screen)

    def enforce_rules(self):
        for player in self.players:
            print "enforcing ", player.tank.xPosition, ", ", player.tank.yPosition

            if player.tank.hp < 0:
                self.players.remove(player)
            if player.tank.xPosition < 0:
                player.tank.xPosition = 0
            if player.tank.xPosition > self.size[0]:
                player.tank.xPosition = self.size[0]
            if player.tank.yPosition < 0:
                player.tank.yPosition = 0
            if player.tank.yPosition > self.size[1]-80:
                player.tank.yPosition = self.size[1]-80
