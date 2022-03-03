import pandas as pd

rankTable = pd.read_csv('rankTable.csv')

print(type(rankTable))
print(list(pd.DataFrame(rankTable.sum())))




