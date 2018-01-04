import pandas as pd
import sys

one = 'kahuna.afam_dis.2.csv'
two  ='kahuna.white.2.csv'

argv = sys.argv

if len(argv) > 1:
    one = argv[1]
    two = argv[2]
    # studentGroups = []

a = pd.read_csv(one)
b = pd.read_csv(two)

combined = a.merge(b, on='School Code')

num_x = 0
num_y = 0

columns = ['score_x','vote_x','score_y','vote_y']

report = combined[(combined['number_x'] > num_x) & (combined['number_y'] > num_y)][columns]

print report.corr()
print report.describe()


