import pandas as pd
import shapefile as shp
import glob as g
import sys
import os.path
import scipy.stats
#from scipy.stats.stats import pearsonr
import os
import numpy as np
import numpy.linalg as nla
import statsmodels.api as sm


X = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]
Y = [0.5,2.0,2.0,6.0,3.0,8.0,6.0,7.0,10.0,11.0]

#print "Pearsonr"
#print pearsonr(a,b)

print "Numpy"
print np.corrcoef(X,Y)

#import pdb; pdb.set_trace
print "Numpy LEast Squares"
a = np.array([X])
print a.shape
b = np.array(Y)
print b.shape
print np.linalg.lstsq(a.T,b)

df = pd.DataFrame({'X':X,'Y':Y})

print "Correlation"
print df.corr()

print "OLS"


model = sm.OLS(Y,X).fit()
print "Raw"
print model.summary()

Y = df['Y']
X = df['X']

model = sm.OLS(Y,X).fit()
print "Pandas"
print model.summary()

