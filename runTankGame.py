#!/usr/bin/env python
from TankGame import TankGame
from player import Player


game = TankGame()
player1 = Player("P1", 0, 0, 0, 0)
player2 = Player("P2", 200, 200, 0, 0)
game.set_players([player1, player2])

print game.run()
exit
