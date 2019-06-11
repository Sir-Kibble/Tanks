#!/usr/bin/env python
from TankGame import TankGame
from MoveDown import MoveDown
from MoveLeft import MoveLeft


game = TankGame()
player1 = MoveDown("P1", 100, 100, 90, 180)
player2 = MoveLeft("P2", 200, 100, 0, 0)

game.set_players([player1, player2])

print game.run()
exit
