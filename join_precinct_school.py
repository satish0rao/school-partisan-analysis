import pandas as pd
import shapefile as shp
import glob as g


testing = False

if testing:
    # TODO:  put in small test files/and globs to do speed up run.
else:
    schools = pd.read_csv("school-data/ca2012entities_csv.txt")
    zipcodes = pd.read_csv("zipcodes/US Zip Codes from 2013 Government Data")
    shapefiles = g.glob("election-data/california-2016-election-precinct-maps/shapefiles/*.shp")
    entities = pd.read_csv("school-data/ca2012entities_csv.txt")
    votes = pd.read_csv("election-data/california-2016-election-precinct-maps/final-results/all_precinct_results.csv")
    scores = pd.read_csv("school-data/ca2012_all_csv_v3.txt")


zipHash = {}

for index,row in zipcodes.iterrows():
    key = (int(row['LNG']),int(row['LAT']))
    if not key in zipHash:
        zipHash[key] = [(row['LNG'],row['LAT'],row['ZIP'])]
    else:
        zipHash[key].append((row['LNG'],row['LAT'],row['ZIP']))

#print zipHash.keys()

def ptDist(p1,p2):
    return (p1[0]-p2[0])**2 * (p1[1] - p2[1])**2

def lookup(point):
    min = '0000'
    min_val = 10000
    for (x,y) in [(0,0),(-1,0),(1,0),(0,-1),(0,1),(1,1),(-1,-1)]:
        key = (int(point[0]+x),int(point[1]+y))
        if key in zipHash:
            #print key, ' is in hash'
            #print zipHash[key]
            for x in zipHash[key]:
                if (ptDist((x[0],x[1]),point) < min_val):
                    min_val = ptDist((x[0],x[1]),point)
                    min = x[2]
    return min
                    



zips = []
precincts = []
lats = []
longs = []


precinctPointsHash = {}
precinctZipHash = {}

for fname in shapefiles:
    parts = fname.split('.')
    print "processing ", fname
    print parts
    sf = shp.Reader(parts[0])
    fields = sf.fields[1:] 
    field_names = [field[0] for field in fields] 
    print fields
    for shape in sf.shapeRecords():
        if len(shape.shape.points) > 1:
            zipcode = lookup(shape.shape.points[0])
            lat = shape.shape.points[0][1]
            lng = shape.shape.points[0][0]
        else:
            print "reusing zipcode for" , atr
        atr = dict(zip(field_names, shape.record))  
        zips.append(zipcode)
        lats.append(lat)
        longs.append(lng)

        key = (int(lng),int(lat))
        precinct = atr['pct16']
        if key in precinctPointsHash.keys():
            precinctPointsHash[key].append((lat,lng,precinct))
        else:
            precinctPointsHash[key] = [(lat,lng,precinct)]
        if zipcode in precinctZipHash.keys():
            precinctZipHash[zipcode].append(precinct)
        else:
            precinctZipHash[zipcode] = [precinct]

        precincts.append(precinct)



output = pd.DataFrame({'zip':zips, 'precinct': precincts, 'longitude': longs, 'latitude': lats})
output.to_csv("precints_zipcodes.csv")


# How should we match schools to precincts?
# Match schools to precincts in two ways.
#   One by getting precincts with the same or nearby zipcodes.
#       This loses a lot of precints I think. 
#   One by getting precincts with the nearby lattitude/longitude.
#       This risks crossing city boundaries which can make
#       a political difference. 

# Probably should just do schools at a certain level (say high school) 
# and match a precinct to that school or something.

# For now just assign all precincts with the same zipcode to the school.



schools = entities[entities['Type Id'] == 7] # Schools rather than districts or counties.

schoolsPrecincts = {}

school_key_column = 'School Code'

for index,row in schools.iterrows():
    key = int(row["Zip Code"])
    if key in precinctZipHash:
        schoolsPrecincts[row[school_key_column]] = precinctZipHash[key]
    else:
        # Do something better here!
        continue


# (1) Get voting for precints matched to school, make dataframe, indicating clinton v trump.
#     (a) Results in final-results directory.


# Probably should use Dataframe.apply



precinctsClinton = {}
precinctsTrump = {}

for index,row in votes.iterrows():
    precinctsClinton[row['pct16']] = float(row['pres_clinton'])
    precinctsTrump[row['pct16']] = float(row['pres_trump'])

schoolVotes = {}

for key in schoolsPrecincts.keys():
    clinton = 0
    trump = 0
    for x in schoolsPrecincts[key]:
        if x in precinctsTrump:
            #print "schoolVotes:", x, clinton,trump
            clinton += precinctsClinton[x]
            trump += precinctsTrump[x]
    schoolVotes[key] = (clinton,trump)

# (2) Get test from schools, and correlate to number for clinton v trump.
#     (b) Test scores in school-data/...

testId = 11  # 
studentGroup = 1 # All students
grade = 9 #



scores = scores[(scores['Test Id'] == testId) & (scores['Subgroup ID'] == studentGroup) & (scores['Grade'] == 9)]

schoolScores = {}

for index,row in scores.iterrows():
    key = row[school_key_column]

    if row["Percentage At Or Above Proficient"] != '*':
        print row["Percentage At Or Above Proficient"]
        schoolScores[key] = float(row["Percentage At Or Above Proficient"])

ids = []
votes = []
scores = []
names = []

for key in schoolScores.keys():
    if key in schoolVotes:
        (clinton,trump) = schoolVotes[key]
        if clinton+trump > 0:
            ids.append(key)
            names.append(schools[schools[school_key_column] == key]['School Name'].iloc[0])
            scores.append(schoolScores[key])
            votes.append(clinton/(clinton+trump))
         



kahuna = pd.DataFrame({'School Code': ids, 'School Name': names, 'vote': votes,'score': scores})
kahuna.to_csv("kahuna.csv")


print kahuna.corr()


#print output


