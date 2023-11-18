sum=0
n=0

def main(close):
    global n, sum
    n+=1
    sum+=close
    if(close>sum/n):
        return "buy"
    else:
        return "sell"