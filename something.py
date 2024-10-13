import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import sys

table = pd.read_csv('output_dataset.csv')
half = int(len(table)/2)
y = table.iloc[:half, -1]
yFinal = table.iloc[half:,-1]

def convertToNum(value):
  base = 94
  allchar = []
  fourchar = 0
  chars = 0
  for i in range(100):
    if i < len(value):
      char = value[-1*i]
      fourchar += base**chars * (ord(str(char)) - 32)
    else:
      char = 0
    chars+=1
    if chars % 4 == 0:
      allchar.append(fourchar)
      fourchar = 0
      chars = 0
  return allchar

numerical_representation = []
for i in range(0, len(table)):
  value = table.loc[i, table.columns[0]]
  numerical_representation.append(convertToNum(value))

table2names = [("d" + str(num)) for num in range(25)]
table.drop(table.columns[0], axis=1, inplace=True)
table2 = pd.DataFrame(numerical_representation)
table2.columns = table2names
result = pd.concat([table2, table], axis=1, join="inner")

x = result.iloc[:half, 0:-2]
xFinal = result.iloc[half:, 0:-2]

userInput = sys.argv[1]

model6 = RandomForestRegressor(n_estimators=1000, random_state=0)
model6.fit(table2, table.iloc[:, -1])

input_data = np.array(convertToNum(userInput)).reshape(1, 25)
input_final = pd.DataFrame(input_data)
input_final.columns = table2names
prediction = model6.predict(input_final)
print("There is a " + str(100-100*prediction[0]) + "% chance that this is a phishing site.  ")