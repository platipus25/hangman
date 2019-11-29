# based on https://github.com/sindresorhus/cows
import re

cows = ""
with open("cows.txt", "r") as cows_raw:
  cows = cows_raw.read()
  cows_raw.close()
  cows = re.sub("\n$", "", cows)
  cows = cows.split("\n\n\n")


if __name__ == "__main__":
  print(*cows, sep="\n\n\n")