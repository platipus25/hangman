import util
import ui
import random
import requests
from cows import cows
from hangman import sequences as hangman_sequences
from betting import betting as bet

from subprocess import call

def gen(wordsList):
  word = random.choice(words)
  guessedSoFar = "*" * len(word)
  unique = len(set(word))
  remaining = int(1 * unique)
  sequence = hangman_sequences[-1]
  if len(hangman_sequences) > remaining:
    sequence = hangman_sequences[remaining]
  guessHistory = []
  def hint(guessed):
    resp = requests.get("https://api.datamuse.com/words", params={"ml": word}).json()
    hints = filter(lambda entry: not word in entry["word"], resp)
    hints = [entry["word"] for entry in hints]
    #print(hints)
    #print(f"word: {word}")
    return random.choice(hints)
  return [word, guessedSoFar, guessHistory, hint, remaining, sequence]

def cost(word, guess, guessHistory):
  found = util.findStr(util.split(word), guess)
  if len(found) > 0 or guess in guessHistory:
    return 0
  return 1

def reward():
  global word
  bet.defaultGame.balance += len(word)
  print(random.choice(cows))

numwords = 10
words = requests.get("https://api.noopschallenge.com/wordbot/", params={"set": "common", "count": numwords}).json()["words"]
#print(words)

word, guessed, guessHistory, hint, remaining, sequence = gen(words)

def iterate():
  global word, guessed, guessHistory, hint, remaining, sequence
  if guessHistory:
    guessHistory.sort()
    print(f"You've guessed: {', '.join(guessHistory)}")
  print(f"""{guessed}
{remaining} guess{"es" if remaining != 1 else ""} remaining""")
  guess = input("⇒ ")
  while not guess:
    guess = input("(hint: {}) ⇒ ".format(hint(guessed)))
  guessed = util.copy(word, guessed, guess)
  guessCost = cost(word, guess, guessHistory)
  if not guess in guessHistory:
    guessHistory.append(guess)
  remaining -= guessCost
  if guessCost > 0:
    frame = sequence[-1]
    if remaining < len(sequence):
      frame = sequence[remaining]
    print(frame)
  checkWinLose()

def won():
  global remaining, guessed
  return remaining > 0 and word==guessed

def lost():
  global remaining
  return remaining <= 0

def checkWinLose():
  global word, guessed, guessHistory, hint, remaining, sequence
  if won():
    print(f"""You win! \nThe word was {word} \nYou had {remaining} guess{"es" if remaining != 1 else ""} left""")
    reward()
  elif lost():
    print("You ran out of guesses\n")
    print(f"Balance: {ui.chalk.green(bet.defaultGame.balance)}\nDebt: {ui.chalk.red(bet.defaultGame.debt)}")
    print("Would you like to buy another guess? ", end = "")
    resp = input()
    renewing = 0
    if resp.isnumeric():
      renewing = int(resp)
    elif resp in ["y", "yes", "yup", "yah", "yeah", "aye"]:
      renewing = 1
    if renewing:
      bet.defaultGame.balance -= renewing
      remaining += renewing
    else:
      print(f"""You lost \nThe word was {ui.chalk.cyan(word)}""") 
  if won() or lost():
    bet.defaultGame.iterate()
    arrayOfResults = bet.defaultGame.betResultsTable.getvalue().split("\n")
    if(len(arrayOfResults) >= 2):
      print(arrayOfResults[-2]) # last betting result
    #bet.defaultGame.dashboard()
    word, guessed, guessHistory, hint, remaining, sequence = gen(words)

while True:
  call("clear")
  while True:
    #bet.defaultGame.iterate()
    iterate()