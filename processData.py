import pandas as pd
import os

def assertTrue(truth, failureMsg):
    if truth == False:
        raise Exception(failureMsg)
        

### Extract data from countryInfo.csv
sheetPath = os.path.join("data", "countryInfo.csv")
df = pd.read_csv(sheetPath, sep=',')

allCountries1 = sorted(list(set(list(df['country']))))
print("The number of countries in countriInfo.csv:", len(allCountries1))

cleanedDF = df[['country', 'alpha2', 'region']].copy()
cleanedDF = cleanedDF.rename(columns={"country": "name", "alpha2": "iso"})

# TODO: Add Hong Kong, Taiwan, ?

# print("","This is the cleaned data frame:", cleanedDF.head(n=5), sep='\n')
## print(list(cleanedDF.columns.values.tolist()))

### Extract data from countryInfo.csv

sheetPath = os.path.join("data", "population.csv")
df = pd.read_csv(sheetPath, sep=',')
# print("This is the keys:", list(df.columns.values.tolist()))

allCountries2 = sorted(list(set(list(df['country']))))
print("Number of countries in population.csv:", len(allCountries2))

df.drop(df[df['year'] < 2019].index, inplace = True)
# print("","This is the cleaned data frame:", df.head(n=5), sep='\n')

assertTrue(len(allCountries2) == len(df['country']), "Countries was dropped when cleaning population.csv")

allCountries3 = sorted(list(set(list(df['country']))))

assertTrue(len(set(allCountries1).intersection(allCountries2))==min(len(allCountries2),len(allCountries1)), 
           "WARNING! Countries will be removed from smaller data set!")

# print("Taiwan" in cleanedDF['name'].unique())


cdfnames = cleanedDF['name'].values
dfnames = df['country'].values
df_ind = []
for name1 in cdfnames:
    for j, name2 in enumerate(dfnames):
        if (name2 == name1):
            df_ind.append(j)

population_df = df['population'].iloc[df_ind]
# population_df.columns = ['population']

population_df = population_df.reset_index()
cleanedDF = cleanedDF.join(population_df)
print("","This is the cleaned data frame:", cleanedDF.head(n=5), sep='\n')

allRegions = sorted(list(set(list(cleanedDF['region']))))
# print(allRegions)
print(cleanedDF.loc[cleanedDF['region'] == 'Europe'])

for r in allRegions:
    print("number of countries in", r, "is", len(cleanedDF.loc[cleanedDF['region'] == r]))

cleanedDF = cleanedDF.drop(columns='index')
print("","This is the cleaned data frame:", cleanedDF.head(n=5), sep='\n')

### # Save Data
### cleanedDF.to_csv("CleanedData.csv", index=False)