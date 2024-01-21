def get_next_time(curr_time):
    print(int(curr_time[-5:-3])==0)
    if int(curr_time[-5:-3])==0:
      print('here')
      next_time = curr_time[:2] + ":30:00"
    else:
      if int(curr_time[:2]) <9:
        next_time = "0" + str(int(curr_time[:2])+1) + ":00:00"
      else:
        next_time = str(int(curr_time[:2])+1) + ":00:00"
    return next_time

print(get_next_time("09:00:00"))