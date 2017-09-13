import pandas as pd


chunksize = 10 ** 5
first = True
for chunk in pd.read_csv('ca2012_all_csv_v3.txt', chunksize=chunksize):
    this_one = chunk[chunk['Subgroup ID'] == 220]
    if first:
        this_one.to_csv("african_am.txt")
        first = False
    else:
        with open('african_am.txt', 'a') as f:
            this_one.to_csv(f,header=False)

