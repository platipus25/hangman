

def split(string):
  return list(string)

def join(inArray):
  return "".join(inArray)

def contains(inArray, needle = ""):
  return needle in inArray

def findChar(inArray, needle = ""):
  if not contains(join(inArray), needle):
    return []
  
  out = []
  for i in range(len(inArray)):
    v = inArray[i]
    if v == needle:
      out.append(i)
  return out
  
def findStr(inArray, needle = ""):
  if not contains(join(inArray), needle):
    return []
  # use all occurances if it is only one char
  if len(needle) == 1:
    return findChar(inArray, needle)
  
  out = {}
  #print(f"Starting points: {findChar(inArray, needle[0])}")
  # use different hypothetical starting points
  for offset in findChar(inArray, needle[0]):
    out[offset] = []
    current = out[offset]
    
    #print(offset)
    # go through the string from the starting point
    for index in range(offset, len(inArray)):
      letter = inArray[index]
      needleUnOffsetIndex = index - offset
      #print(f"Letter in word: {letter}({index})\tCurrent: {current}")
      if needleUnOffsetIndex >= len(needle):
        #print(f"Reached the length of the needle ({len(needle)})")
        break
      if letter == needle[needleUnOffsetIndex]:
        current.append(index)
  #print(out)
  # flatten
  values = out.values()
  out = [item for sublist in values for item in sublist]
  return out
  

def copy(fromStr, toStr, matching = ""):
  toStr = split(toStr)
  for i in findStr(split(fromStr), matching):
    toStr[i] = fromStr[i]
  return join(toStr)

#print(findStr(split("isk isk isksksk"), "isk"))
