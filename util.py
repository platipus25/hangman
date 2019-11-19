

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
  
  out = []
  #print(findChar(inArray, needle[0]))
  # use different hypothetical starting points
  for offset in findChar(inArray, needle[0]):
    #print(offset)
    # go through the string from the starting point
    for i in range(offset, len(inArray)):
      v = inArray[i]
      #print(i, v, len(needle), i-offset, needle, out)
      if i-offset >= len(needle):
        #print("breaking early")
        break
      if v == needle[i-offset]:
        out.append(i)
    # if we found all of them, return
    if len(out) == len(needle):
      break
    else:
      # otherwise, scrap the hypotheical starting point, and move on to the next one
      out = []
  return out
  

def copy(fromStr, toStr, matching = ""):
  toStr = split(toStr)
  for i in findStr(split(fromStr), matching):
    toStr[i] = fromStr[i]
  return join(toStr)