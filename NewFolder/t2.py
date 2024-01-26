import pandas as pd

a = {
    "09:35:00": 15
}
    
print(a)
print(len(a))
df = pd.DataFrame(a, columns=['a','b','c'])
print(df, i)
df.to_csv('test.csv', index=False)
print(df)