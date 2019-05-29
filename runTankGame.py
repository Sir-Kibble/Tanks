#!/usr/bin/env python
from TankGame import TankGame
from MoveDown import MoveDown
from MoveLeft import MoveLeft


game = TankGame()
player1 = MoveDown()
player2 = MoveLeft()

player1.set_state("P1", 0, 0, 0, 0)
player2.set_state("P2", 200, 340, 0, 0)

game.set_players([player1, player2])

print game.run()
exit
