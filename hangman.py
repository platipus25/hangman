import util
import ui
import random
import requests
from cows import cows
from sequences import sequences as hangman_sequences
from betting import betting as bet

from subprocess import call

class Game:
  _words = []
  word = ""
  guessedSoFar = []
  guessHistory = []
  remaining = 0
  sequence = []
  betting = None
  def __init__(self, numwords = 10):
    self._words = requests.get("https://api.noopschallenge.com/wordbot/", params={"set": "common", "count": numwords}).json()["words"]
  
  def hint(self, guessed):
      resp = requests.get("https://api.datamuse.com/words", params={"ml": self.word}).json()
      hints = filter(lambda entry: not self.word in entry["word"], resp)
      hints = [entry["word"] for entry in hints]
      #print(hints)
      #print(f"word: {word}")
      return random.choice(hints)

  def gen(self):
    self.word = random.choice(self._words)
    self.guessedSoFar = "*" * len(self.word)
    unique = len(set(self.word))
    self.remaining = int(1 * unique)
    self.sequence = hangman_sequences[-1]
    if len(hangman_sequences) > self.remaining:
      self.sequence = hangman_sequences[self.remaining]
    self.guessHistory = []
    self.betting = bet.Game(startingBalance = 1)
  def cost(self, guess):
    found = util.findStr(util.split(self.word), guess)
    if len(found) > 0 or guess in self.guessHistory:
      return 0
    return 1

  def reward(self):
    bet.defaultGame.balance += len(self.word)
    print(random.choice(cows))

  def iterate(self):
    if not self.word:
      self.gen()
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
    if guessCost > 0:
      frame = self.sequence[-1]
      if self.remaining < len(self.sequence):
        frame = self.sequence[self.remaining]
      print(frame)
    self.checkWinLose()

  def won(self):
      return self.remaining > 0 and self.word==self.guessedSoFar

  def lost(self):
    return self.remaining <= 0

  def checkWinLose(self):
    #global word, guessed, guessHistory, hint, remaining, sequence
    if self.won():
      print(f"""You win! \nThe word was {self.word} \nYou had {self.remaining} guess{"es" if self.remaining != 1 else ""} left""")
      self.reward()
    elif self.lost():
      print("You ran out of guesses\n")
      print(f"Balance: {ui.chalk.green(self.betting.balance)}\nDebt: {ui.chalk.red(self.betting.debt)}")
      print("Would you like to buy another guess? ", end = "")
      resp = input()
      renewing = 0
      if resp.isnumeric():
        renewing = int(resp)
      elif resp in ["y", "yes", "yup", "yah", "yeah", "aye"]:
        renewing = 1
      if renewing:
        bet.defaultGame.balance -= renewing
        self.remaining += renewing
      else:
        print(f"""You lost \nThe word was {ui.chalk.cyan(self.word)}""") 
    if self.won() or self.lost():
      bet.defaultGame.iterate()
      arrayOfResults = bet.defaultGame.betResultsTable.getvalue().split("\n")
      if(len(arrayOfResults) >= 2):
        print(arrayOfResults[-2]) # last betting result
      #bet.defaultGame.dashboard()
      self.gen()