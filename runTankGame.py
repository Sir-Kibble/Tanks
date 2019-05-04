from TankGame import TankGame
from player import Player


game = TankGame()
player1 = Player(0, 0, 0, 0)
player2 = Player(400, 400, 0, 0)
game.set_players([player1, player2])

print game.run()
exit
