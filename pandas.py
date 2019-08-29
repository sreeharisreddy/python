import pandas as pd
df = pd.read_csv("example.csv") 
print (df)
print (df.head())
print(df.head(3))
print(df.tail(3))

df_excel = pd.read_exel("example.xls")
df_delim = pd.read_csv('pokemon_data.txt', delimiter='\t')
df['HP']
