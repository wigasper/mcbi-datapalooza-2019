#!/usr/bin/env python3
import os
import time

import pandas as pd
from census import Census
from us import states

#os.chdir("/media/wkg/storage/mcbi-datapalooza-2019")
os.chdir("/Users/wigasper/Documents/mcbi-datapalooza-2019")

zip_data = pd.read_csv("zipcodes.csv", index_col=None)

# remove pesky "Unnamed" column
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]

# Change zips to str and pad with 0s
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))

# Create Census object with API key
cens = Census("641afb80c092a21ba85b039d816e211551bccad4")


# variables at:
#       https://api.census.gov/data/2017/acs/acs5/variables.html
# census API wrapper package:
#       https://github.com/datamade/census

# total population variable: B01003_001E
def get_census_val(cens_obj, variable, zipcode):
    result = cens_obj.acs5.zipcode(variable, zipcode)
    if len(result) > 0:
        return result[0].get(variable)
    else:
        return 0.0

start = time.perf_counter()
zip_data["population"] = zip_data["zip"].apply(lambda x: get_census_val(cens, 
                                                            "B01003_001E", x))
print("elapsed time for pull: " + str(time.perf_counter() - start))

zip_data.to_csv("zip_data.csv")
# short test

#tester = zip_data[0:20]
#start = time.perf_counter()
#tester["population"] = tester["zip"].apply(lambda x: get_census_val(cens, "B01003_001E", x))
#print("test time: " + str(time.perf_counter() - start))



#cens.acs5.zipcode()



cens.acs5.zipcode("B01003_001E", "68154")

#test = cens.acs5.zipcode("B01003_001E", 68154)
#cens.sf1.state_zipcode("B00001_001E", 31, 68154)



#cens.acs5.get(('NAME', 'B00001_001E'), {'for': 'state:{}'.format(states.NE.fips)})


#def get_census_val(cens_obj, variable, zipcode):
#    result = cens_obj.acs5.zipcode(variable, zipcode)
#    return result[0].get(variable)

#test1 = get_census_val(cens, "B01003_001E", 68154)

#zip_data['population'] = get_census_val(cens, "B01003_001E", )