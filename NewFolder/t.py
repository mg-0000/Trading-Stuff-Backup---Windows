import pandas as pd

path = "Data/CNXBAN_30minute2023_12_26.csv"
df = pd.read_csv(path)
closest_time = "09:30:00"
df2 = df[df['datetime'].str.contains(closest_time)].index[0]
print(df.iloc[df2]['open'])