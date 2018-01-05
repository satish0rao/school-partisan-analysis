import pandas as pd
import shapefile as shp
import glob as g
import sys
import os.path
import scipy.stats
import os

math = "9 10 11 12 13 14 15"
ela = "7"

tests = [("econ",31, ela),("econ_not",111,ela),("all",1,ela),
         ("econ",31, math),("econ_not",111,math),("all",1,math),
         ("afam",74, math),("afam_not",200,math),("afam_ok",220,math),
         ("white",80, math),("white_not",206,math),("white_ok",226,math),
         ("afam",74,ela),("afam_not",200,ela),("afam_ok",220,ela),
         ("white",80,ela),("white_not",206,ela),("white_ok",226,ela)]
         

urban = False
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


for i in range(len(tests)):
    for j in range(len(tests)):
        (prefix1,code1,test_set1) = tests[i]
        (prefix2,code2,test_set2) = tests[j]
        print "\n%s,%s versus %s,%s" % (prefix1,test_set1,prefix2,test_set2)
        cmd = "python quick_test.py \"%s/kahuna.%s.%s.csv\" \"%s/kahuna.%s.%s.csv\"" % (root_for_outfiles,prefix1,test_set1,root_for_outfiles,prefix2,test_set2)
        print "Running ", cmd
        os.system(cmd)


