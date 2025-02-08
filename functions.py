import pandas as pd

df = pd.read_csv('cordenadas.csv', dtype=str)

print(df.loc[9, 'B'])
