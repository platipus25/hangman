from random import randint
from io import StringIO
from ui import deny, getNum, chalk

class Game():
  balance_ = 0
  debt = 0
  interestCounter = 0
  interest = 0
  betResultsTable = StringIO()

  def __init__(self, startingBalance = 10, interest = 0):
    self.balance = startingBalance
    self.interest = interest
    self.betResultsTable = StringIO()

  @property
  def balance(self):
    return self.balance_

  @balance.setter
  def balance(self, newBalance):
    oldBalance = self.balance_
    if newBalance > oldBalance:
      # balance increased
      print(chalk.green(f"+{newBalance - oldBalance}"), file = self.betResultsTable)
    elif newBalance < oldBalance:
      # balance decreased
      print(chalk.red(f"-{abs(oldBalance - newBalance)}"), file = self.betResultsTable)
    
    # move negative money into debt
    if newBalance < 0:
      print(f"Newbalance: {newBalance}\nOldbalance: {oldBalance}")
      self.debt += abs(newBalance)
      newBalance = 0
    
    self.balance_ = newBalance

  def log(num):
    

  def dashboard(self):
    betResults = self.betResultsTable.getvalue()
    if betResults:
      betResults+="\n"
    dashboard = f"{betResults}Balance: {chalk.green(self.balance)}\nDebt: {chalk.red(self.debt)}"
    print(dashboard)
    return dashboard

  def iterate(self):
    self.dashboard()
    percent = randint(1, 100)
    bet = 0
    wantstosettledebt = False
    if self.debt > 0 and self.balance >= self.debt:
      wantstosettledebt = deny(f"Do you want to settle your debt of {chalk.red(self.debt)}? ")
      if wantstosettledebt:
        self.balance -= self.debt
        print(f"-{chalk.red(self.debt)}", file = self.betResultsTable)
        self.debt = 0
    #self.interestCounter+=1

    bet = getNum("How much do you want to bet?: ", expandedMessage = f"How much do you want to bet? (you have ${self.balance}): ", numType = float)

    if bet > self.balance:
      # TODO: implement simple interest
      print(f"You are borrowing {chalk.red(bet - self.balance)}")
      
      self.balance = self.balance - bet

    if percent > 50:
      #lose
      self.balance -= bet
    elif percent > 20:
      # break even
      print(chalk.yellow(f"{'no profit'}"), file = self.betResultsTable)
    else:
      # jackpot (triple bet)
      self.balance += bet*3

defaultGame = Game()
if __name__ == "__main__":
  while True:
    defaultGame.iterate()