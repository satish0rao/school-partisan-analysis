#  To run.

1) unzip files in school-data directory.
2) python join_precinct_school.py

Take a look at join_precinct_school.py to 
see what is up. Code needs cleaning, just
a start. 


------------------

Data Descriptions:

 school-data/README  - tells sources of files.
 
 zipcodes/   - contains zipcodes latitude/longitudes.

 election-data/   - contains precinct level returns and shapfiles for precincts.

--------------------------------

1) Matching schools to precinct.

  Method 1:  Match precinct to zipcode, only use the precincts with same zipcode of school to determine vote.
  Method 2:  Match precincts to closest school using zipcode locations for location of school.
