#!/usr/bin/env python
import pygame
import time
from multiprocessing import Process, Pipe


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
        self.players = {}

    def set_players(self, players):
        x = 0
        for player in players:
            game_pipe, player_pipe = Pipe()
            player.set_pipe(player_pipe)
            self.players[x] = {
                "player": player,
                "pipe": game_pipe
            }
            x += 1

    def run(self):
        # start players
        for x in range(0, len(self.players)):
            self.players[x]["player"].start()
            Process(target=self.players[x]["player"].tank.run).start()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for x in range(0, len(self.players)):
                        self.players[x]["pipe"].send("kill")
                        self.players[x]["pipe"].recv()
                    self.running = False
            self.screen.fill(self.WHITE)
            for x in range(0, len(self.players)):
                self.players[x]["pipe"].send({
                        "type": "play",
                        "tankProps": {
                            "xPosition": self.players[x]["player"].tank.xPosition,
                            "yPosition": self.players[x]["player"].tank.yPosition,
                            "turretTheta": self.players[x]["player"].tank.turretTheta,
                            "chassisTheta": self.players[x]["player"].tank.chassisTheta,
                            "hp": self.players[x]["player"].tank.hp
                        }
                })
                updates = self.players[x]["pipe"].recv()
                self.players[x]["player"].tank.xPosition = updates["tankProps"]["xPosition"]
                self.players[x]["player"].tank.yPosition = updates["tankProps"]["yPosition"]
                self.players[x]["player"].tank.chassisTheta = updates["tankProps"]["chassisTheta"]
                self.players[x]["player"].tank.turretTheta = updates["tankProps"]["turretTheta"]
                self.players[x]["player"].tank.hp = updates["tankProps"]["hp"]

            self.enforce_rules()
            print "draw_updates"
            self.draw_updates()
            pygame.event.pump()
            self.clock.tick(10)
            time.sleep(.5)
        pygame.quit()
        return 1

    def draw_updates(self):
        for x in range(0, len(self.players)):
            print "drawing ", self.players[x]["player"].name, " at y: ", self.players[x]["player"].tank.yPosition
            self.players[x]["player"].tank.render(self.screen)

    def enforce_rules(self):
        for x in range(0, len(self.players)):
            print "enforcing ", self.players[x]["player"].tank.yPosition,
            ", ",
            self.players[x]["player"].tank.yPosition
            if self.players[x]["player"].tank.xPosition < 0:
                self.players[x]["player"].tank.xPosition = 0
            if self.players[x]["player"].tank.xPosition > self.size[0]:
                self.players[x]["player"].tank.xPosition = self.size[0]
            if self.players[x]["player"].tank.yPosition < 0:
                self.players[x]["player"].tank.yPosition = 0
            if self.players[x]["player"].tank.yPosition > self.size[1]-80:
                self.players[x]["player"].tank.yPosition = self.size[1]-80
