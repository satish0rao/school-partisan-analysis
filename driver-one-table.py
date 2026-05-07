import pandas as pd
import shapefile as shp
import glob as g
import sys
import os.path
import scipy.stats
import os
import numpy as np

# year
year = '2025'

# Test IDs differ by test regime: STAR (≤2013) vs SBAC (≥2017)
if year in ('2017', '2018', '2022', '2025'):
    math = "2"
    ela = "1"
    score_measure = "Percentage Standard Met and Above"
else:
    math = "9 10 11 12 13 14 15"
    ela = "7"
    score_measure = "Percentage At Or Above Proficient"

tests = [("male_math",3,math),("female_math",4,math),("male_ela",3,ela),("female_ela",4,ela),
         ("afam",74, math),("afam_econ_dis",200,math),("afam_econ_ok",220,math),
         ("white",80, math),("white_econ_dis",206,math),("white_econ_ok",226,math),
         ("afam",74, ela),("afam_econ_dis",200, ela),("afam_econ_ok",220, ela),
         ("white",80, ela),("white_econ_dis",206, ela),("white_econ_ok",226, ela),
         ("hispanic",78, math),("hispanic_econ_dis",204, math),("hispanic_econ_ok",224, math),
         ("hispanic",78, ela),("hispanic_econ_dis",204, ela),("hispanic_econ_ok",224, ela),
         ("all_students", 1, math), ("all_students", 1, ela)]

not_used_tests = [("econ_dis",31, ela),("econ_ok",111,ela),("all",1,ela),
         ("econ_dis",31, math),("econ_ok",111,math),("all",1,math),
         ("afam",74, math),("afam_econ_dis",200,math),("afam_econ_ok",220,math),
         ("white",80, math),("white_econ_dis",206,math),("white_econ_ok",226,math),
         ("afam",74,ela),("afam_econ_dis",200,ela),("afam_econ_ok",220,ela),
         ("white",80,ela),("white_econ_dis",206,ela),("white_econ_ok",226,ela)]

# tests = []
#for (name,code) in [("hispanic",78),("hispanic_econ_dis",204),("hispanic_econ_ok",224),
#                    ("asian",76),("asian_econ_dis", 202),("asian_econ_ok",222),("male",3),("female",4)]:
#    for test_set in (math,ela):
#        tests.append((name,code,test_set))


# #tests = [('afam',74,ela),('white',80,ela)]

urban = True
non_urban = True

if urban == False:
    root_for_outfiles = 'non-urban-kahuna-files'
    param_file = 'params_non_urban.py'
    output_suffix = '.non-urban'
elif non_urban == False:
    root_for_outfiles = 'urban-kahuna-files'
    param_file = 'params_urban.py'
    output_suffix = '.urban'
else:
    root_for_outfiles = 'kahuna-files'
    param_file = 'params_all.py'
    output_suffix = ''

output_dir = 'results'
os.makedirs(output_dir, exist_ok=True)

cmd = "cp %s params.py" % param_file
print("Running ", cmd)
os.system(cmd)


for (prefix,code,test_set) in tests:
    if not os.path.isfile("%s/%s.%s.%s.csv" % (root_for_outfiles,prefix,year,test_set)):
        if not os.path.isfile("school-data/%s.%s.txt" % (prefix, year)):
            cmd = "cd school-data; python3 split_by_demo.py %s.%s.txt %d %s; cd .." % (prefix, year, code, year)
            print("Running ", cmd)
            os.system(cmd)
        cmd = "python3 join_precinct_school_method2.py school-data/%s.%s.txt %s %s" % (prefix, year, year, test_set)
        print("Running ", cmd)
        os.system(cmd)
        cmd = "mv kahuna.csv \"%s/%s.%s.%s.csv\"" % (root_for_outfiles, prefix, year, test_set)
        print("Running ", cmd)
        os.system(cmd)


# --- Cache skip: if both result files exist and are newer than every kahuna
# input used in this run, skip the analysis phases entirely.
_output_files = [
    "%s/vote_achievement_correlations.one-table.%s%s.csv" % (output_dir, year, output_suffix),
    "%s/covariates_achievement_correlations.%s%s.csv" % (output_dir, year, output_suffix),
]
_kahuna_files_in_use = [
    "%s/%s.%s.%s.csv" % (root_for_outfiles, prefix, year, test_set)
    for (prefix, _code, test_set) in tests
]
_existing_kahuna = [p for p in _kahuna_files_in_use if os.path.isfile(p)]
if _existing_kahuna and all(os.path.isfile(p) for p in _output_files):
    _out_mtime = min(os.path.getmtime(p) for p in _output_files)
    _in_mtime = max(os.path.getmtime(p) for p in _existing_kahuna)
    if _out_mtime >= _in_mtime:
        print("Skipping analysis: %s and %s are newer than all kahuna inputs." %
              tuple(_output_files))
        sys.exit(0)

# In-memory cache of kahuna DataFrames (read each file only once across phases).
_kahuna_cache = {}
def _read_kahuna(prefix, year_, test_set):
    key = (prefix, year_, test_set)
    if key not in _kahuna_cache:
        _kahuna_cache[key] = pd.read_csv(
            "%s/%s.%s.%s.csv" % (root_for_outfiles, prefix, year_, test_set))
    return _kahuna_cache[key]


table = {}


for i in range(len(tests)):
    for j in range(len(tests)):
        (prefix1,code1,test_set1) = tests[i]
        (prefix2,code2,test_set2) = tests[j]
        if (test_set1 != test_set2):
            continue
        if prefix1 == prefix2:
            continue
        a = _read_kahuna(prefix1, year, test_set1)
        b = _read_kahuna(prefix2, year, test_set2)
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
    print(key)
    titles = sorted(table[key][next(iter(table[key]))].keys())
    print('\t')
    for t in titles:
        print(t, '\t', end=' ')
    print('\n')

    prefixes1 = sorted(table[key].keys())
    for prefix in prefixes1:
        print(prefix, end=' ')
        prefixes = sorted(table[key][prefix].keys())
        for t in prefixes:
            entry = table[key][prefix][t]
            #print "(%.3f %d)\t" % (entry[0],entry[1])
            print("%.3f \t" % entry[0], end=' ')
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

        print('\n')

output = pd.DataFrame({'A:group1': groups1, 'B:group2': groups2, 'C:test':which_tests, 'D:corr': corrs, 'E:counts': counts, 'F:mean':means, 'G:std': stds, 'H:corr_w_1':corr_xs})
output['I:measure'] = score_measure

output.to_csv("%s/vote_achievement_correlations.one-table.%s%s.csv" % (output_dir, year, output_suffix), index = False)



table = {}
nces = pd.read_csv("nces/ccd_lea_052_1516_w_1a_011717.csv", encoding='latin1', low_memory=False)
seda = pd.read_csv("seda/SEDA_cov_geodist_pool_v20.csv", encoding='latin1', low_memory=False)

schools_precincts = pd.read_csv('school_to_precinct.csv')

nces_seda = nces.merge(seda,left_on='LEAID',right_on='leaidC')
#nces_seda['ST_LEAID'] = nces_seda['ST_LEAID'].astype(str)

# Pre-filter SEDA covariates to numeric, non-constant columns. Doing this once
# avoids the same dtype/nunique check inside the inner loop.
_seda_cols = [
    x for x in seda.columns
    if np.issubdtype(seda[x].dtype, np.number) and seda[x].nunique(dropna=True) > 1
]
for x in _seda_cols:
    table[x] = {}

# Loop order swapped: outer (i, j) pair, inner covariate. This lets each
# kahuna→kahuna→nces_seda merge happen once per pair instead of once per
# (pair × covariate), turning the analysis from ~10 min into seconds.
num_x = 0
num_y = 0
for i in range(len(tests)):
    for j in range(len(tests)):
        (prefix1,code1,test_set1) = tests[i]
        (prefix2,code2,test_set2) = tests[j]
        if (test_set1 != test_set2):
            continue
        if prefix1 == prefix2:
            continue
        a = _read_kahuna(prefix1, year, test_set1)
        b = _read_kahuna(prefix2, year, test_set2)
        combined = a.merge(b, on='School Code')
        combined = combined.merge(nces_seda, left_on='District_x', right_on='leaname')
        nrows = combined['School Code'].count()
        filtered = combined[(combined['number_x'] > num_x) & (combined['number_y'] > num_y)]
        diff = filtered['score_y'] - filtered['score_x']
        score_x = filtered['score_x']
        description = diff.describe()

        if test_set1 not in table[_seda_cols[0]]:
            for x in _seda_cols:
                table[x].setdefault(test_set1, {})
        for x in _seda_cols:
            table[x][test_set1].setdefault(prefix1, {})
            x_col = filtered[x]
            corr_diff_x = diff.corr(x_col)
            corr_score_x_x = score_x.corr(x_col)
            table[x][test_set1][prefix1][prefix2] = (
                corr_diff_x, nrows, description['mean'], description['std'], corr_score_x_x
            )



groups1 = []
groups2 = []
which_tests = []
covariates = []
corrs = []
means = []
stds = []
counts = []
corr_xs = []
 
def short_float(f):
    x = '%.3f' % f
    return x

table1 = table

for covariate in table1.keys():
    table = table1[covariate]
    for key in table.keys():
        print(key)
        titles = sorted(table[key][next(iter(table[key]))].keys())
        print('\t')
        for t in titles:
            print(t, '\t', end=' ')
            print('\n')

        prefixes1 = sorted(table[key].keys())
        for prefix in prefixes1:
            print(prefix, end=' ')
            prefixes = sorted(table[key][prefix].keys())
            for t in prefixes:
                entry = table[key][prefix][t]
                #print "(%.3f %d)\t" % (entry[0],entry[1])
                print("%.3f \t" % entry[0], end=' ')
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
                covariates.append(covariate)

            print('\n')


output = pd.DataFrame({'A:group1': groups1, 'B:group2': groups2, 'C:test':which_tests, 'D:corr': corrs, 'E:counts': counts, 'F:mean':means, 'G:std': stds, 'H:corr_w_1':corr_xs, 'G:Covariate': covariates})
output['I:measure'] = score_measure

output.to_csv("%s/covariates_achievement_correlations.%s%s.csv" % (output_dir, year, output_suffix), index = False)
