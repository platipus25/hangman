from hangman import util, Game as _Game

"""
Shows ascii art before guessing and just before losing
"""
class Game(_Game):
  def iterate(self):
    if not self.word:
      self.gen()
    frame = self.remaining if self.remaining < len(self.sequence) else -1
    print(self.sequence[frame])
    if self.guessHistory:
      self.guessHistory.sort()
      print(f"You've guessed: {', '.join(self.guessHistory)}")
    print(f"""{self.guessedSoFar}
  {self.remaining} guess{"es" if self.remaining != 1 else ""} remaining""")
  
    guess = input("⇒ ")
    while not guess:
      guess = input("(hint: {}) ⇒ ".format(self.hint(self.guessedSoFar)))
    self.guessedSoFar = util.copy(self.word, self.guessedSoFar, guess)
    guessCost = self.cost(guess)
    if not guess in self.guessHistory:
      self.guessHistory.append(guess)
    self.remaining -= guessCost
    self.checkWinLose()
  
  def checkWinLose(self):
    if self.lost():
      print(self.sequence[-1])
    super().checkWinLose()