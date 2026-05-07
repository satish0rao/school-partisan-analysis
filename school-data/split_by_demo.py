import pandas as pd
import sys
import os.path

out_file = 'african_am.txt'
subgroup_id = 220

argv = sys.argv

year = '2013'

if len(argv) > 1:
    out_file = argv[1]
    print(argv)
    subgroup_id = int(argv[2])
    if len(argv)>3:
        year = argv[3]

chunksize = 10 ** 5
first = True

infile = 'ca%s_all_csv_v3.txt' % year
if subgroup_id == 1:
    # Prefer the smaller _1_ file; fall back to _all_ if not present
    candidate = 'ca%s_1_csv_v3.txt' % year
    if os.path.isfile(candidate):
        infile = candidate

if year=='2017':
    if subgroup_id !=1:
        infile = 'sb_ca2017_all_csv_v2.txt'
    else:
        infile = 'sb_ca2017_1_csv_v2.txt'

if year=='2018':
    infile = 'sb_ca2018_all_csv_v3.txt'

if year=='2022':
    infile = 'sb_ca2022_all_csv_v1.txt'

if year=='2025':
    # Prefer the all-subgroups file when available; fall back to the _1_ file
    # (which contains only Subgroup ID = 1).
    if os.path.isfile('sb_ca2025_all_csv_v1.txt'):
        infile = 'sb_ca2025_all_csv_v1.txt'
    else:
        infile = 'sb_ca2025_1_csv_v1.txt'

# 2022/2025 SBAC files use caret delimiter and renamed columns
if year in ('2022', '2025'):
    read_kwargs = dict(sep='^', encoding='latin1', low_memory=False)
else:
    read_kwargs = dict(encoding='latin1', low_memory=False)

# 2025 also renames "Students Tested" -> "Total Students Tested"
_rename_2022 = {'Student Group ID': 'Subgroup ID', 'Test ID': 'Test Id'}
_rename_2025 = dict(_rename_2022, **{'Total Students Tested': 'Students Tested'})

for chunk in pd.read_csv(infile, chunksize=chunksize, **read_kwargs):
    if year == '2022':
        chunk = chunk.rename(columns=_rename_2022)
    elif year == '2025':
        chunk = chunk.rename(columns=_rename_2025)
    this_one = chunk[chunk['Subgroup ID'] == subgroup_id]
    if first:
        this_one.to_csv(out_file)
        first = False
    else:
        with open(out_file, 'a') as f:
            this_one.to_csv(f,header=False)

