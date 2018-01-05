import pandas as pd
import shapefile as shp
import glob as g
import sys
import os.path
import scipy.stats

import params

argv = sys.argv



scores_file = 'school-data/ca2012_1_csv_v3.txt'
#studentGroups = [220] # African Americans
#studentGroups = [1] # all students

#testIds = [9,10,11,12,13,14,15]  #  math tests.
testIds = [7] # ela test

if len(argv) > 1:
    scores_file = argv[1]
    if len(argv)>2:
        testsIds = []
        for x in range(2,len(argv)):
            testIds.append(int(argv[x]))
            
    # studentGroups = []
    # for i in xrange(2,len(argv)):
    #     print i, argv, len(argv)
    #     studentGroups.append(int(argv[i]))


    
testing = False

if testing:
    # TODO:  put in small test files/and globs to do speed up run.
    pass
else:
    schools = pd.read_csv("school-data/ca2012entities_csv.txt")
    zipcodes = pd.read_csv("zipcodes/US Zip Codes from 2013 Government Data")
    shapefiles = g.glob("election-data/california-2016-election-precinct-maps/shapefiles/*.shp")
    entities = pd.read_csv("school-data/ca2012entities_csv.txt")
    votes = pd.read_csv("election-data/california-2016-election-precinct-maps/final-results/all_precinct_results.csv")
    #scores = pd.read_csv("school-data/ca2012_1_csv_v3.txt")
    scores = pd.read_csv("%s" % scores_file)


print "Finished reading files..."

#print zipHash.keys()

def ptDist(p1,p2):
    return (p1[0]-p2[0])**2 * (p1[1] - p2[1])**2

def geom_lookup(point,latsToZips):
    min = '0000'
    min_val = 10000
    min_zip = False
    for diff in xrange(0,5):
        for x in xrange(-diff,diff):
            for y in xrange(-diff,diff):
                key = (int(point[0]+x),int(point[1]+y))
                if key in latsToZips:
                    #print key, ' is in hash'
                    #print zipHash[key]
                    for z in latsToZips[key]:
                        cur_dist = ptDist((z[0],z[1]),point) 
                        if (cur_dist < min_val):
                            min_val = cur_dist
                            min_zip = z[2]
                        if cur_dist > 2*min_val+3:
                            return min_zip
    return min_zip

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
school_key_column = 'School Code'
urban_precincts = {}

if not os.path.isfile("school_to_precinct.csv"):

    zipToPos = {}

    for index,row in zipcodes.iterrows():
        key = int(row['ZIP'])
        if key in zipToPos:
            print "Zip should only appear once"
        else:
            zipToPos[key] = (row['LNG'],row['LAT'])

    posToSchoolZip = {}

    zipToSchool ={}

    schools = entities[entities['Type Id'] == 7] # Schools rather than districts or counties.

    schoolsPrecincts = {}
    schoolNames = {}


    for index,row in schools.iterrows():
        key = int(row["Zip Code"])
        while (not key in zipToPos.keys()):
            print "Hmmm: zipcode %d for school %s has no position?" % (key, row['School Name'])
            key = key-1

        (lng,lat) = zipToPos[key]

        key = (int(lng),int(lat))
        if key in posToSchoolZip:
            posToSchoolZip[key].append((lng,lat,row["Zip Code"]))
        else:
            posToSchoolZip[key] = [(lng,lat,row["Zip Code"])]

        key = row["Zip Code"]
        if key in zipToSchool:
            zipToSchool[key].append(row[school_key_column])
        else:
            zipToSchool[key] = [row[school_key_column]]

        schoolNames[row[school_key_column]] = row['School Name']


    precincts = []
    lats = []
    longs = []

    schoolsPrecincts = {}

    urban_shapefiles = ['037-los-angeles.shp','075-san-francisco.shp']


    for fname in shapefiles:
        parts = fname.split('.')
        print "processing ", fname
        print parts
        sf = shp.Reader(parts[0])
        fields = sf.fields[1:] 
        field_names = [field[0] for field in fields] 
        print fields
        
        urban_precinct = False
        if fname.split('/')[-1] in urban_shapefiles:
            urban_precinct = True

        for shape in sf.shapeRecords():
            close_schools = []
            if len(shape.shape.points) > 1:
                close_school_zip = geom_lookup(shape.shape.points[0],posToSchoolZip)
                if not close_school_zip:
                    continue
                close_schools = zipToSchool[close_school_zip]
                
                # for debugging.
                lat = shape.shape.points[0][1]
                lng = shape.shape.points[0][0]
            else:
                print "reusing zipcode for" , atr

            atr = dict(zip(field_names, shape.record))  

            precinct = atr['pct16']

            urban_precincts[precinct] = urban_precinct

            for key in close_schools:
                if key in schoolsPrecincts:
                    schoolsPrecincts[key].append(precinct)
                else:
                    schoolsPrecincts[key] = [precinct]


        school_ids = []
        school_names = []
        precincts_ids  = []
        urban_or_nots = []

        for key in schoolsPrecincts.keys():
            for precinct in schoolsPrecincts[key]:
                school_ids.append(key)
                school_names.append(schoolNames[key])
                precincts_ids.append(precinct)
                urban_or_nots.append(urban_precincts[precinct])

        output = pd.DataFrame({"school": school_ids, "school name": school_names, 
                               "precinct":precincts_ids, "urban":urban_or_nots})
        output.to_csv("school_to_precinct.csv")
else:
    schoolsPrecincts = {}
    output = pd.read_csv("school_to_precinct.csv")
    for (idx,row) in output.iterrows():
        key = row['school']
        if key in schoolsPrecincts.keys():
            schoolsPrecincts[key].append(row['precinct'])
        else:
            schoolsPrecincts[key] = [row['precinct']]
        urban_precincts[row['precinct']] = row['urban']
            
# (1) Get voting for precincts matched to school, make dataframe, indicating clinton v trump.
#     (a) Results in final-results directory.


# Probably should use Dataframe.apply

precinctsClinton = {}
precinctsTrump = {}
    
for index,row in votes.iterrows():
    precinctsClinton[row['pct16']] = float(row['pres_clinton'])
    precinctsTrump[row['pct16']] = float(row['pres_trump'])

schoolVotes = {}
schoolUrban = {}

for key in schoolsPrecincts.keys():
    clinton = 0
    trump = 0

    urban_count = 0
    count = 0

    for x in schoolsPrecincts[key]:
        if x in precinctsTrump:
            #print "schoolVotes:", x, clinton,trump
            clinton += precinctsClinton[x]
            trump += precinctsTrump[x]
            count += 1
            if urban_precincts[x]:
                urban_count+=1

    if (urban_count >= count/2):
        #print "School %s is urban", key
        schoolUrban[key] = True
    else:
        schoolUrban[key] = False
    schoolVotes[key] = (clinton,trump)



# (2) Get test from schools, and correlate to number for clinton v trump.
#     (b) Test scores in school-data/...

grades = [9,10,11] #

#scores = scores[(scores['Test Id'].isin(testIds)) & (scores['Subgroup ID'].isin(studentGroups)) & (scores['Grade'].isin(grades))]
scores = scores[(scores['Test Id'].isin(testIds)) & (scores['Grade'].isin(grades))]

schoolScores = {}
schoolNumbers = {}

def include_school(key):
    if not key in schoolUrban:
        return False
    if schoolUrban[key]:
        return params.include_urban()
    else:
        return params.include_non_urban()

for index,row in scores.iterrows():
    key = row[school_key_column]

    if key == 0:
        continue

    if row["Percentage At Or Above Proficient"] != '*':
        if (row["Students Tested"] < 1) or (not include_school(key)):
            continue
        if not key in schoolScores.keys():
            schoolScores[key] = float(row["Percentage At Or Above Proficient"])
            schoolNumbers[key] = row["Students Tested"]
        else:
            schoolScores[key] = (schoolScores[key]*schoolNumbers[key] + row["Students Tested"]*float(row["Percentage At Or Above Proficient"]))/(1.0* (schoolNumbers[key] + row["Students Tested"]))
            schoolNumbers[key] += row["Students Tested"]

ids = []
votes = []
scores = []
names = []
numbers = []
districts = []

for key in schoolScores.keys():
    if key in schoolVotes:
        (clinton,trump) = schoolVotes[key]
        if clinton+trump > 0:
            #print key, schools[schools[school_key_column] == key]
            ids.append(key)
            names.append(schools[schools[school_key_column] == key]['School Name'].iloc[0])
            districts.append(schools[schools[school_key_column] == key]['District Name'].iloc[0])
            scores.append(schoolScores[key])
            votes.append(clinton/(clinton+trump))
            numbers.append(schoolNumbers[key])
         

kahuna = pd.DataFrame({'School Code': ids, 'School Name': names, 'District': districts, 'vote': votes,'score': scores, 'number': numbers})
kahuna.to_csv("kahuna.csv")


print kahuna.corr()

print kahuna.describe()

#print scipy.stats.pearsonr(kahuna['vote'],kahuna['score'])


#print output


