https://github.com/KeithGalli/pandas/blob/master/Pandas%20Data%20Science%20Tutorial.ipynb
  
import pandas as pd
df = pd.read_csv("example.csv") 
print (df)
print (df.head())
print(df.head(3))
print(df.tail(3))

df_excel = pd.read_exel("example.xls")
df_delim = pd.read_csv('pokemon_data.txt', delimiter='\t')
df['HP']

//reading all columns
df.columns
print(df[['Name', 'Type 1', 'HP']])  //read many cols

## Read Each Row
#print(df.iloc[0:4])
# for index, row in df.iterrows():
#     print(index, row['Name'])
#df.loc[df['Type 1'] == "Grass"]

## Read a specific location (R,C)
#print(df.iloc[2,1])

df.sort_values(['Type 1', 'HP'], ascending=[1,0])

#df['Total'] = df['HP'] + df['Attack'] + df['Defense'] + df['Sp. Atk'] + df['Sp. Def'] + df['Speed']

# df = df.drop(columns=['Total'])

df['Total'] = df.iloc[:, 4:10].sum(axis=1)

cols = list(df.columns)
df = df[cols[0:4] + [cols[-1]]+cols[4:12]]

#Saving Data
# df.to_csv('modified.csv', index=False)
#df.to_excel('modified.xlsx', index=False)
df.to_csv('modified.txt', index=False, sep='\t')
df.head(5)

#Filtering data
new_df = df.loc[(df['Type 1'] == 'Grass') & (df['Type 2'] == 'Poison') & (df['HP'] > 70)]
new_df.reset_index(drop=True, inplace=True)
new_df
new_df.to_csv('filtered.csv')

#conditional changes

# df.loc[df['Total'] > 500, ['Generation','Legendary']] = ['Test 1', 'Test 2']

# df

df = pd.read_csv('modified.csv')

#group by
df['count']=1
df.groupby(['Type 1', 'Type 2']).count()['count'] #not working

# Working with large data set
new_df = pd.DataFrame(columns=df.columns)

for df in pd.read_csv('modified.csv', chunksize=5):  #Process 5 rows at a time
    results = df.groupby(['Type 1']).count()
    
    new_df = pd.concat([new_df, results])


