import numpy as np
import os
from datetime import datetime
print("starting")
a = np.arange(0,20)

for i in a:
    print(i)
    if(i==5):
        print(datetime.now())
        print("restarting")
        os.system('python test_restart.py')