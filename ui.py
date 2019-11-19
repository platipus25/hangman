from simple_chalk import chalk

# put ui module stuff here

def getNum(message, expandedMessage = "", numType = int):
  resp = input(message)
  while not resp.isnumeric():
    resp = input(expandedMessage or message)
  return numType(resp)

def confirm(message, additionalAffirmations = ["yup", "yah", "yeah", "aye"]):
  resp = input(message)
  return resp.lower() in ["yes", "y", *additionalAffirmations]

def deny(message, additionalDenials = ["nope", "nay", "naw"]):
  resp = input(message)
  return resp.lower() in ["no", "n", *additionalDenials]

def prompt(prompt = "Choose one:", choices = {}):
  # generate the list for indexes
  choices_indexes = list(choices.keys())
  print(f"{prompt}")
  for i in choices:
    print(f"{choices_indexes.index(i)}. {i}")
  
  choice = None
  # allow the user to choose by index or by name
  while not choice in choices:
    choice = input("\t – ")
    if choice.isnumeric() and int(choice) < len(choices_indexes):
      # its expecting the name, so if they chose by index, convert to name
       choice = choices_indexes[int(choice)]
  return choices[choice]
