import pandas as pd

nces = pd.read_csv("nces/ccd_lea_052_1516_w_1a_011717.csv")
seda = pd.read_csv("seda/SEDA_cov_geodist_pool_v20.csv")

schools_precincts = pd.read_csv('school_to_precinct.csv')

a = nces.merge(seda,left_on='LEAID',right_on='leaidC')[['LEAID','ST_LEAID']]
