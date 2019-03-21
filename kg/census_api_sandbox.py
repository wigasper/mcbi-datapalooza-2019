#!/usr/bin/env python3
import os
import time

from tqdm import tqdm
import pandas as pd
from census import Census
# Census API wrapper package:
#       https://github.com/datamade/census

#from us import states

os.chdir("/media/wkg/storage/mcbi-datapalooza-2019")
#os.chdir("/Users/wigasper/Documents/mcbi-datapalooza-2019")

zip_data = pd.read_csv("zipcodes.csv", index_col=None)

# remove pesky "Unnamed" column
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]

# Change zips to str and pad with 0s
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))

# Create Census object with API key
cens = Census("641afb80c092a21ba85b039d816e211551bccad4")

zip_data["population"] = None

# get_census_val() : Gets the value of a given variable for a given zipcode
# Args: cens_obj - A Census object (census package)
#       variable - The variable to get a value for. From:
#           https://api.census.gov/data/2017/acs/acs5/variables.html
#       zipcode - The zipcode to get the variable's value for
# Returns the value of the variable for the zipcode, or None if a connection
# error. Also returns 0.0 if there is no value - this may need to be tweaked
# and is not adequately abstracted.
# Still needs to be tested with every variable change
def get_census_val(cens_obj, variable, zipcode):
    try:
        result = cens_obj.acs5.zipcode(variable, zipcode)
        if len(result) > 0:
            return result[0].get(variable)
        else:
            return 0.0
    except ConnectionError:
        return None
    except CensusException:
        return None

# Put zip codes into a list for ease of processing
zips = [[zipcode, None] for zipcode in zip_data["zip"]]

# Get populations for zip codes if value is None. I did it this way to be able
# non-redundantly call the API in batches in case of the common ConnectionError
for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B01003_001E", zipcode[0])
