import pandas as pd
import os
import random 
 
numberOfCountries = 10

class indexation:
    def __init__(self):
        self.idx = random.randint(0, numberOfCountries-1)

    def get(self):
        return self.idx

    def randomize(self):
        self.idx = random.randint(0, numberOfCountries-1)

i = indexation()

print(i.get())
print(i.get())
print(i.get())
print(i.get())
print(i.get())
print(i.randomize())
print(i.get())
print(i.get())
print(i.get())
print(i.get())
print(i.get())
# sheetPath = os.path.join("information", "CleanedData.csv")
# df = pd.read_csv(sheetPath, sep=',')
# allNames = df['name'].values
# print(df.head())

# print(df['name'].values)

# n = random.randint(0,len(allNames))
# print(n)