# based on sindresorhus/cows, but I drew the ascii art myself using box drawing characters.
import re

hangman = [
"""
  ┌───┐
  │   O
  │  \│/
  │   │
  │  / \\
  │
──┴──
""",
"""
  ┌───┐
  │   O
  │  \│/
  │   │
  │  /
  │
──┴──
""",
"""
  ┌───┐
  │   O
  │  \│/
  │   │
  │
  │
──┴──
""",
"""
  ┌───┐
  │   O
  │  \│/
  │
  │
  │
──┴──
""",
"""
  ┌───┐
  │   O
  │  \│
  │
  │
  │
──┴──
""",
"""
  ┌───┐
  │   O
  │   │
  │
  │
  │
──┴──
""",
"""
  ┌───┐
  │   O
  │
  │
  │
  │
──┴──
""",
"""
  ┌───┐
  │
  │
  │
  │
  │
──┴──
""",
"""
  ┌───
  │
  │
  │
  │
  │
──┴──
""",
"""
  ┌──
  │
  │
  │
  │
  │
──┴──
""",
"""
  ┌─
  │
  │
  │
  │
  │
──┴──
""",
"""
  ┌
  │
  │
  │
  │
  │
──┴──
""",
"""

  │
  │
  │
  │
  │
──┴──
""",
"""


  │
  │
  │
  │
──┴──
""",
"""



  │
  │
  │
──┴──
""",
"""




  │
  │
──┴──
""",
"""





  │
──┴──
""",
"""






──┴──
""",
"""






 ─┴─
""",
"""






  ┴
"""
]

# carefully crafted sequences of hangmannedness:
# I don't like the ones that show one leg being put on, but not one arm
# and the ones that show different ammounts of the gallows being put up are also messy
# hangman is a dark game; like ring a round the rosy
# its a children's game, but then "we all fall down!" is dark
sequences = {
  0: [0],
  1: [0, 7],
  2: [0, 3, 7],
  3: [0, 2, 3, 7],
  4: [0, 2, 3, 6, 7],
  5: [0, 2, 3, 5, 6, 7],
  6: [0, 2, 3, 4, 5, 6, 7], # shows putting on one arm, but not one leg
  7: [0, 1, 2, 3, 4, 5, 6, 7],
  8: [0, 1, 2, 3, 4, 5, 6, 7, 17],
  9: [0, 1, 2, 3, 4, 5, 6, 7, 16, 17],
 10: [0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18], # and from here on, its a mess
 11: [0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19],
 12: [0, 1, 2, 3, 4, 5, 6, 7, 15, 16, 17, 18, 19],
 13: [0, 1, 2, 3, 4, 5, 6, 7, 14, 15, 16, 17, 18, 19],
 14: [0, 1, 2, 3, 4, 5, 6, 7, 13, 14, 15, 16, 17, 18, 19],
 15: [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 16, 17, 18, 19],
 16: [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19],
 17: [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
 18: [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
 19: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
}

# replace indexes with the frames that they represent
for key in sequences:
  for frame in range(len(sequences[key])):
    print(sequences[key][frame])
    sequences[key][frame] = \
    hangman[sequences[key][frame]]
sequences = list(sequences.values()) # its just a dictionary for readability

if __name__ == "__main__":
  import time
  from subprocess import run
  for sequenceKey in sequences:
    sequence = sequences[sequenceKey]
    time.sleep(0.8)
    for frameIndex in sequence:
      run("clear")
      print(sequenceKey)
      print(hangman[frameIndex])
      time.sleep(0.5)