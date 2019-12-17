import hangman
import to_spec

game = hangman.Game()
game = to_spec.Game()

while True:
  game.iterate()