import pandas as pd
import shapefile as shp
import glob as g
import sys
import os.path
import scipy.stats
import os
import numpy as np
import statsmodels.api as sm


math = "9 10 11 12 13 14 15"
ela = "7"

tests = [("econ_dis",31, ela),("econ_ok",111,ela),("all",1,ela),
         ("econ_dis",31, math),("econ_ok",111,math),("all",1,math),
         ("afam",74, math),("afam_econ_dis",200,math),("afam_econ_ok",220,math),
         ("white",80, math),("white_econ_dis",206,math),("white_econ_ok",226,math),
         ("afam",74,ela),("afam_econ_dis",200,ela),("afam_econ_ok",220,ela),
         ("white",80,ela),("white_econ_dis",206,ela),("white_econ_ok",226,ela)]

# tests = []
for (name,code) in [("hispanic",78),("hispanic_econ_dis",204),("hispanic_econ_ok",224),
                    ("asian",76),("asian_econ_dis", 202),("asian_econ_ok",222),("male",3),("female",4)]:
    for test_set in (math,ela):
        tests.append((name,code,test_set))


#tests = [('afam',74,ela),('white',80,ela),('afam',74,math),('white',80,math)]
tests = [('afam',74,math),('white',80,math)]

urban = True
non_urban = True



if urban == False:
    root_for_outfiles = 'non-urban-kahuna-files'
    param_file = 'params_non_urban.py'
elif non_urban == False:
    root_for_outfiles = 'urban-kahuna-files'
    param_file = 'params_urban.py'
else:
    root_for_outfiles = 'kahuna-files'
    param_file = 'params_all.py'

cmd = "cp %s params.py" % param_file
print "Running ", cmd
os.system(cmd)

for (prefix,code,test_set) in tests:
    if not os.path.isfile("%s/kahuna.%s.%s.csv" % (root_for_outfiles,prefix,test_set)):
        if not os.path.isfile("school-data/%s.txt" % prefix):
            cmd = "cd school-data; python split_by_demo.py %s.txt %d; cd .." % (prefix, code)
            print "Running ", cmd
            os.system(cmd)
        cmd = "python join_precinct_school_method2.py school-data/%s.txt %s" % (prefix,test_set)
        print "Running ", cmd
        os.system(cmd)
        cmd = "mv kahuna.csv \"%s/kahuna.%s.%s.csv\"" % (root_for_outfiles, prefix, test_set)
        print "Running ", cmd
        os.system(cmd)



table = {}


for i in range(len(tests)):
    for j in range(len(tests)):
        (prefix1,code1,test_set1) = tests[i]
        (prefix2,code2,test_set2) = tests[j]
        if (test_set1 != test_set2):
            continue
        file1 = "%s/kahuna.%s.%s.csv" % (root_for_outfiles,prefix1,test_set1)
        file2 = "%s/kahuna.%s.%s.csv" % (root_for_outfiles,prefix2,test_set2)
        a = pd.read_csv(file1)
        b = pd.read_csv(file2)
        columns = ['number_x','score_x','score_y','vote_y']
        num_x = 0
        num_y = 0
        combined = a.merge(b,on='School Code')
        report = combined[(combined['number_x'] > num_x) & (combined['number_y'] > num_y)][columns]
        report['diff'] = report['score_y'] - report['score_x']
        description = report['diff'].describe()

        correlations = report.corr()
        # print "(%s,%s)" % (prefix1, prefix2) , test_set1, test_set2
        # print correlations

        if not test_set1 in table.keys():
            table[test_set1] = {}

        if not prefix1 in table[test_set1]:
            table[test_set1][prefix1] = {}
            
        #table[test_set1][prefix1][prefix2] = (correlations.loc['score_x']['vote_y'] - correlations.loc['score_y']['vote_y'],combined.count().loc['School Code'])
        table[test_set1][prefix1][prefix2] = (correlations.loc['diff']['vote_y'],combined.count().loc['School Code'],description['mean'],description['std'],correlations.loc['score_x']['vote_y'])


groups1 = []
groups2 = []
which_tests = []
corrs = []
means = []
stds = []
counts = []
corr_xs = []
 
def short_float(f):
    x = '%.3f' % f
    return x

for key in table.keys():
    print key
    titles = table[key][table[key].keys()[0]].keys()
    titles.sort()
    print '\t'
    for t in titles:
        print t, '\t',
    print '\n'

    prefixes1 = table[key].keys()
    prefixes1.sort()
    for prefix in prefixes1:
        print prefix,
        prefixes = table[key][prefix].keys()
        prefixes.sort()
        for t in prefixes:
            entry = table[key][prefix][t]
            #print "(%.3f %d)\t" % (entry[0],entry[1])
            print "%.3f \t" % entry[0],
            groups1.append(prefix)
            groups2.append(t)
            if key == ela:
                which_tests.append("ela")
            else:
                which_tests.append("math")
            corrs.append(short_float(entry[0]))
            counts.append(entry[1])
            means.append(short_float(entry[2]))
            stds.append(short_float(entry[3]))
            corr_xs.append(short_float(entry[4]))
            
        print '\n'

output = pd.DataFrame({'A:group1': groups1, 'B:group2': groups2, 'C:test':which_tests, 'D:corr': corrs, 'E:counts': counts, 'F:mean':means, 'G:std': stds, 'H:corr_w_1':corr_xs})

output.to_csv("vote_achievement_correlations.csv", index = False)



#nces = pd.read_csv("nces/ccd_lea_052_1516_w_1a_011717.csv")
seda = pd.read_csv("seda/SEDA_cov_geodist_pool_v20.csv")

schools_precincts = pd.read_csv('school_to_precinct.csv')

#nces_seda = nces.merge(seda,left_on='LEAID',right_on='leaidC')
#nces_seda['ST_LEAID'] = nces_seda['ST_LEAID'].astype(str)

number = 0


#covariates = ['paredVblkwht','perblk','baplus_wht']
#covariates = ['paredVblkwht','baplus_wht','occsales_fem','perblk']
#covariates = ['occsales_fem']
covariates = ['vote_x']

for i in range(len(tests)):
    for j in range(len(tests)):
        #for x in seda.columns:
        (prefix1,code1,test_set1) = tests[i]
        (prefix2,code2,test_set2) = tests[j]
        if (test_set1 != test_set2): # and (prefix1 != prefix2):
            continue
        if (prefix1 == prefix2) and (test_set1 == test_set2):
            continue

        file1 = "%s/kahuna.%s.%s.csv" % (root_for_outfiles,prefix1,test_set1)
        file2 = "%s/kahuna.%s.%s.csv" % (root_for_outfiles,prefix2,test_set2)
        a = pd.read_csv(file1)
        b = pd.read_csv(file2)

        combined = a.merge(b,on='School Code')
        combined['diff'] =combined['score_y'] - combined['score_x']
        relevant_columns = ['School Code','District_x','School Name_x', 'score_x','score_y','number_x','number_y','vote_x','diff']
        combined = combined[relevant_columns]
        combined = combined.merge(seda,left_on='District_x',right_on='leaname')[relevant_columns +  covariates]
        print prefix1, test_set1, prefix2, test_set2
        print combined.corr()
        combined.to_csv("%s/%s.%s.%s.%s.csv" %(root_for_outfiles,prefix1,prefix2,test_set1,test_set2),index=False)

        combined = combined.dropna()
        Y = combined['diff']
        X = combined[covariates]

        model = sm.OLS(Y,X).fit()
        print "Covariates", covariates
        print model.summary()

        Y = combined['diff']
        #covariates1 = ['baplus_wht']
        covariates1 = covariates
        X = combined[covariates1 + ['vote_x']]

        model = sm.OLS(Y,X).fit()
        print "Covariates and vote", covariates1
        print model.summary()
