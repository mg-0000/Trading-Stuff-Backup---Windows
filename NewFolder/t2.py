import pandas as pd
a = []
for i in range(4,16):
    a.append([i, i+1,i+2])
    
print(a)
print(len(a))
df = pd.DataFrame(a, columns=['a','b','c'])
print(df, i)
df.to_csv('test.csv', index=False)
print(df)