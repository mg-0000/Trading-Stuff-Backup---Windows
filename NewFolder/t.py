def round_nearest(n):
  tmp = n*10 - int(n*10)
  if(tmp < 0.5):
    return round(round(n,1),2)
  elif(tmp==0.5):
    return round(round(n,1) + 0.05,2)
  else:
    return round(round(n,1) - 0.05,2)
  
while True:
    a = float(input("Enter sltp"))
    print(round_nearest(0.95*a))