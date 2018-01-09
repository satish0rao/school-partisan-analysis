import glob as g

to_move = g.glob("*_ok.*.csv")

for x in to_move:
    z = x.split('.')
    u = z[0:2]
    u = '.'.join(u)
    y = u.split('_')
    w = y[0]
    #w = '_'.join(w)
    w = w+ '_econ_ok'
    w = w+ '.'+z[2]
    w = w+ '.csv'
    cmd = 'mv \"%s\" \"%s\"' % (x,w)
    print cmd
                 
