import util
import ui
import random
import requests
from cows import cows
from betting import betting as bet

from subprocess import call

def gen(wordsList):
  word = random.choice(words)
  guessedSoFar = "*" * len(word)
  unique = len(set(word))
  remaining = int(1 * unique)
  guessHistory = []
  def hint(guessed):
    return word
  return [word, guessedSoFar, guessHistory, hint, remaining]

def cost(word, guess):
  found = util.findStr(util.split(word), guess)
  if len(found) > 0:
    return 0
  return 1

def reward():
  print(random.choice(cows))

numwords = 10
words = requests.get("https://api.noopschallenge.com/wordbot/", params={"set": "common", "count": numwords}).json()["words"]
#print(words)

word, guessed, guesses, hint, remaining = gen(words)

def iterate():
  global word, guessed, guesses, hint, remaining
  print(f"""{guessed}
{remaining} guess{"es" if remaining != 1 else ""} remaining""")
  guess = input("⇒ ")
  while not guess:
    guess = input("(hint: {}) ⇒ ".format(hint(guessed)))
  guessed = util.copy(word, guessed, guess)
  remaining -= cost(word, guess)
  checkWinLose()

def won():
  global remaining, guessed
  return remaining >= 0 and word==guessed

def lost():
  global remaining
  return remaining < 0

def checkWinLose():
  global word, guessed, guesses, hint, remaining
  if won():
    print(f"""You win! \nThe word was {word} \nYou had {remaining} guess{"es" if remaining != 1 else ""} left""")
    reward()
  elif lost():
    print(f"""You lost \nThe word was {word}""") 
  if won() or lost():
    bet.iterate()
    bet.showDashboard()
    word, guessed, guesses, hint, remaining = gen(words)

while True:
  call("clear")
  while True:
    bet.defaultGame.iterate()

if False:
  if guessed == word:
    print(f"""You win! 
The word was {word}
You had {remaining} guess{"es" if remaining != 1 else ""} left""")
    reward()
    word, guessed, guesses, hint, remaining = gen(words)
  print(f"""{guessed}
{remaining} guess{"es" if remaining != 1 else ""} remaining""")
  guess = input("⇒ ")
  while not guess:
    guess = input("(hint: {}) ⇒ ".format(hint(guessed)))
  guessed = util.copy(word, guessed, guess)
  remaining -= cost(word, guess)