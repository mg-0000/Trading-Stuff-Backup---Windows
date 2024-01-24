import pandas as pd

a = [[1,2,3]]
df = pd.DataFrame(a)
for i in range(0,5):
    a.append([i,i+1,i+2])
    df = pd.DataFrame(a)
    print(i, a, df)
    df.to_csv('test.csv', mode='w', header=False)

df.to_csv('test.csv', mode='w', header=False)