import time
from datetime import datetime
for i in range(20):
    t1 = datetime.now()
    f = open('test.txt', 'a')
    t2 = datetime.now()
    print(i, t2 - t1)
    f.write(str(i) + '/n')
    f.close()
    t1 = datetime.now()
    time.sleep(2)
    t2 = datetime.now()
    print(t2 - t1)