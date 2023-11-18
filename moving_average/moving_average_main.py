#simple strategy based on moving averages
#if n1>n2 days moving average is lower than the n2 days moving average, this indicates a positive trend, hence buy

#strategy code
mean1 = 0
mean2 = 0
num1 = 0
initial = 1 #sum1>sum2
close_series = []

def main(close, n1=20, n2=5):
    global mean1, mean2, num1,num2, initial, close_series
    if(num1<n1):
        close_series.append(close)
        num1+=1
    else:
        close_series.pop(0)
        close_series.append(close)
        mean1 = sum(close_series)/n1
        mean2 = mean1*n1/n2

    if(initial==0 and mean1<mean2):
        print("buying")
        initial=1
        return "buy"
    elif(initial==1 and mean1>mean2):
        print("selling")
        initial=0
        return "sell"