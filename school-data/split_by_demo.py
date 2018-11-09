import pandas as pd
import sys

out_file = 'african_am.txt'
subgroup_id = 220

argv = sys.argv

year = '2013'

if len(argv) > 1:
    out_file = argv[1]
    print argv
    subgroup_id = int(argv[2])
    if len(argv)>3:
        year = argv[3]

chunksize = 10 ** 5
first = True

infile = 'ca%s_all_csv_v3.txt' % year
if subgroup_id == 1:
    infile = 'ca%s_1_csv_v3.txt' % year

if year=='2017':
    if subgroup_id !=1:
        infile = 'sb_ca2017_all_csv_v2.txt'
    else:
        infile = 'sb_ca2017_1_csv_v2.txt'


for chunk in pd.read_csv(infile, chunksize=chunksize):
    this_one = chunk[chunk['Subgroup ID'] == subgroup_id]
    if first:
        this_one.to_csv(out_file)
        first = False
    else:
        with open(out_file, 'a') as f:
            this_one.to_csv(f,header=False)

