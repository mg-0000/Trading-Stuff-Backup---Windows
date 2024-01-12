
def round_nearest(n):
  tmp = n*10 - int(n*10)
  # tmp = int(n*100)
  print(tmp,round(n,1))
  if(tmp < 0.25):
    return round(n,1)
  elif(tmp < 0.5):
    return round(n,1) + 0.05
  elif(tmp < 0.75):
    return round(n,1) - 0.05
  else:
    return round(n,1) 

print(round_nearest(223.775))