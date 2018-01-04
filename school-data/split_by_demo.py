import pandas as pd
import sys

out_file = 'african_am.txt'
subgroup_id = 220

argv = sys.argv

if len(argv) > 1:
    out_file = argv[1]
    print argv
    subgroup_id = int(argv[2])

chunksize = 10 ** 5
first = True
for chunk in pd.read_csv('ca2012_all_csv_v3.txt', chunksize=chunksize):
    this_one = chunk[chunk['Subgroup ID'] == subgroup_id]
    if first:
        this_one.to_csv(out_file)
        first = False
    else:
        with open(out_file, 'a') as f:
            this_one.to_csv(f,header=False)
