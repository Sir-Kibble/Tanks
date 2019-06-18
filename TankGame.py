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
        print players
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
            self.players[x]["player"].activate()
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
                        # "tankProps": {
                        #     "xPosition": self.players[x]["player"].tank.xPosition,
                        #     "yPosition": self.players[x]["player"].tank.yPosition,
                        #     "turretTheta": self.players[x]["player"].tank.turretTheta,
                        #     "chassisTheta": self.players[x]["player"].tank.chassisTheta,
                        #     "hp": self.players[x]["player"].tank.hp
                        # },
                        "gameState": self.__getGameState()
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
            print "drawing ", self.players[x]["player"].name, " at y: ", self.players[x]["player"].tank.yPosition, " x: ", self.players[x]["player"].tank.xPosition
            self.players[x]["player"].tank.readySprites(self.screen, self.size)
            # rotateImage(
            #     self.screen,
            #     self.size,
            #     self.players[x]["player"].tank.chassis.originalImage,
            #     self.players[x]["player"].tank.chassisTheta
            # )

    # currently only handles single tank per player, but want to expand
    def __getGameState(self):
        state = {
            "players": [],
            # "allies": [],
            # "enemies": [],
            # "objects": [],
            # "shells": [],
        }
        for x in range(0, len(self.players)):
            state["players"].append({
                "name": self.players[x]["player"].name,
                "xPosition": self.players[x]["player"].tank.xPosition,
                "yPosition": self.players[x]["player"].tank.yPosition,
                "turretTheta": self.players[x]["player"].tank.turretTheta,
                "chassisTheta": self.players[x]["player"].tank.chassisTheta,
                "hp": self.players[x]["player"].tank.hp
            })
        return state

    def enforce_rules(self):
        self.enforce_boundaries()

    def enforce_boundaries(self):
        for x in range(0, len(self.players)):
            print "enforcing ", self.players[x]["player"].tank.yPosition,
            ", ",
            self.players[x]["player"].tank.yPosition
            if self.players[x]["player"].tank.xPosition < -9:
                self.players[x]["player"].tank.xPosition = -9
            if self.players[x]["player"].tank.xPosition > self.size[0]-49:
                self.players[x]["player"].tank.xPosition = self.size[0]-49
            if self.players[x]["player"].tank.yPosition < -9:
                self.players[x]["player"].tank.yPosition = -9
            if self.players[x]["player"].tank.yPosition > self.size[1]-49:
                self.players[x]["player"].tank.yPosition = self.size[1]-49

# def rotateImage(screen, pos, image, angle):
#     """rotate an image while keeping its center and size"""
#     w, h = image.get_size()
#     box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
#     box_rotate = [p.rotate(angle) for p in box]
#     min_box = (
#         min(box_rotate, key=lambda p: p[0])[0],
#         min(box_rotate, key=lambda p: p[1])[1]
#     )
#     max_box = (
#         max(box_rotate, key=lambda p: p[0])[0],
#         max(box_rotate, key=lambda p: p[1])[1]
#     )
#     pivot = pygame.math.Vector2(w/2, -h/2)
#     pivot_rotate = pivot.rotate(angle)
#     pivot_move = pivot_rotate - pivot
#     origin = (
#         pos[0] + min_box[0] - pivot_move[0],
#         pos[1] - max_box[1] + pivot_move[1]
#     )
#
#     rotated_image = pygame.transform.rotate(image, angle)
#     screen.blit(rotated_image, origin)

    # loc = (image.get_rect().x + image.get_rect().center[0],
    #        image.get_rect().y+ image.get_rect().center[1])
    # rot_sprite = pygame.transform.rotate(image, angle)
    # newLoc = rot_sprite.get_rect().center
