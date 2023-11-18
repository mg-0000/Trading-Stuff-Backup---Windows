import math

mean = 0
std = 0
summation = 0
sq_sum = 0
n = 0

#peak detection function
h_peak = 1.5
peak = 0
def peak_detect(price, mean, std, rst):
    if(rst == 1):
        peak = price
        return 0
    elif(price>peak):
        peak=price
        return 0
    elif(price-mean>h_peak*std):
        return 1

#trough detection function
h_trough = 1.5
trough = 0
def trough_detect(price, mean, std, rst):
    if(rst == 1):
        trough = price
        return 0
    elif(price>trough):
        trough=price
        return 0
    elif(price-mean>h_trough*std):
        return 1

#main function
peak_rst = 0
trough_rst = 0
case_1 = 0  #peak followed by peak
case_2 = 0  #trough_followed by trough
case_3 = 0  #peak followed by trough

prev_detect = "none"
current_detect = prev_detect
def main(price):
    n+=1
    summation+=price
    mean = summation/n
    sq_sum+=price*price
    std = math.sqrt((sq_sum/n)-(mean*mean))

    trough_detect = trough_detect(price,mean,std,peak_rst)
    peak_detect = peak_detect(price,mean,std,trough_rst)
    if(trough_detect==1 or peak_detect==1):
        peak_rst = 1
        trough_rst = 1
        current_detect = "trough"
    elif(peak_detect==1):
        peak_rst = 1
        trough_rst = 1
        current__detect = "peak"
        
    if(prev_detect=="none"0):
        prev_detect = current__detect
    else:
        if(prev_detect=="peak" and current__detect=="peak"):
            case_1+=1
        elif(prev_detect=="trough" and current__detect=="trough"):
            case_2+=1
        elif(prev_detect=="peak" and current__detect=="trough"):
            case_3+=1

    print(case_1,case_1,case_3)