#  To run.

1) unzip files in school-data directory.
2) python driver-one-table.py

Take a look at join_precinct_school_method2.py to 
see what is up. Code needs cleaning, pretty ugly.


------------------

Data Descriptions:

 school-data/README  - tells sources of files.
 
 zipcodes/   - contains zipcodes latitude/longitudes.

 election-data/   - contains precinct level returns and shapfiles for precincts.

 seda/  - covariates 
 
 nces/  nces data files for district


--------------------------------

1) Matching schools to precinct.

  Method 1:  Match precinct to zipcode, only use the precincts with same zipcode of school to determine vote.
  Method 2:  Match precincts to closest school using zipcode locations for location of school.
