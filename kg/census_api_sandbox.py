#!/usr/bin/env python3
import os
import time

from tqdm import tqdm
import pandas as pd
# Census API wrapper package:
#       https://github.com/datamade/census
from census import Census, CensusException

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

#zip_data["population"] = None

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

pops = pd.DataFrame(zips, columns=["zip", "population"])

zip_data = pd.merge(zip_data, pops, how="inner", on="zip")

zip_data.to_csv("zip_data.csv")

with open("pop_45_to_49.csv", "w") as fp:
    for item in zips:
        fp.write(str(item[0]))
        fp.write(", ")
        fp.write(str(item[1]))
        fp.write("\n")



# Get populations of people 45 to 49 "B07001_010E" for zip codes
zips = [[zipcode, None] for zipcode in zip_data["zip"]]

for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B07001_010E", zipcode[0])
        
pops = pd.DataFrame(zips, columns=["zip", "pop_45-49"])

zip_data = pd.merge(zip_data, pops, how="inner", on="zip")

# Save, because the API pulls take a long time
zip_data.to_csv("zip_data.csv")
        
#######
result = cens.acs5.zipcode("B07001_012E", "68114")

zips = [[zipcode, None] for zipcode in zip_data["zip"]]

for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B07001_011E", zipcode[0])

zip_data = pd.read_csv("zip_data.csv", index_col=None)

pops = pd.DataFrame(zips, columns=["zip", "pop_50-54"])

zip_data = pd.merge(zip_data, pops, how="inner", on="zip")
#$#####################
# get pop 49 to and write
with open("pop_50_to_54.csv", "w") as fp:
    for item in zips:
        fp.write(str(item[0]))
        fp.write(", ")
        fp.write(str(item[1]))
        fp.write("\n")

######### get 55 to 59

for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B07001_012E", zipcode[0])

with open("pop_55_to_59.csv", "w") as fp:
    for item in zips:
        fp.write(str(item[0]))
        fp.write(", ")
        fp.write(str(item[1]))
        fp.write("\n")

pops = pd.DataFrame(zips, columns=["zip", "pop_55-59"])
zip_data = pd.read_csv("zip_data.csv", index_col=None)
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))
zip_data = pd.merge(zip_data, pops, how="inner", on="zip")
zip_data.to_csv("zip_data.csv")

#####################################################
# NEXT PULL 60-64
populated_zips = zip_data[zip_data["population"] > 0]

zips = [[zipcode, None] for zipcode in populated_zips["zip"]]

for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B07001_013E", zipcode[0])

with open("pop_60_to_64.csv", "w") as fp:
    for item in zips:
        fp.write(str(item[0]))
        fp.write(", ")
        fp.write(str(item[1]))
        fp.write("\n")
        
zip_data = pd.read_csv("zip_data.csv", index_col=None)
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))
pops = pd.DataFrame(zips, columns=["zip", "pop_60-64"])

zip_data = pd.merge(zip_data, pops, how="left", on="zip")
zip_data.to_csv("zip_data.csv")

# get 65 to 69
populated_zips = zip_data[zip_data["population"] > 0]
zips = [[zipcode, None] for zipcode in populated_zips["zip"]]



for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B07001_014E", zipcode[0])

with open("pop_65_to_69.csv", "w") as fp:
    for item in zips:
        fp.write(str(item[0]))
        fp.write(", ")
        fp.write(str(item[1]))
        fp.write("\n")

pops = pd.DataFrame(zips, columns=["zip", "pop_65-69"])
zip_data = pd.read_csv("zip_data.csv", index_col=None)
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))
zip_data = pd.merge(zip_data, pops, how="left", on="zip")
zip_data.to_csv("zip_data.csv")

# next 70-75
################################

populated_zips = zip_data[zip_data["population"] > 0]

zips = [[zipcode, None] for zipcode in populated_zips["zip"]]

for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B07001_015E", zipcode[0])

with open("pop_70_to_74.csv", "w") as fp:
    for item in zips:
        fp.write(str(item[0]))
        fp.write(", ")
        fp.write(str(item[1]))
        fp.write("\n")
        
zip_data = pd.read_csv("zip_data.csv", index_col=None)
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))
pops = pd.DataFrame(zips, columns=["zip", "pop_70-74"])

zip_data = pd.merge(zip_data, pops, how="left", on="zip")
zip_data.to_csv("zip_data.csv")

# get 75+

zips = [[zipcode, None] for zipcode in populated_zips["zip"]]

for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B07001_016E", zipcode[0])

with open("pop_75_to_inf.csv", "w") as fp:
    for item in zips:
        fp.write(str(item[0]))
        fp.write(", ")
        fp.write(str(item[1]))
        fp.write("\n")

pops = pd.DataFrame(zips, columns=["zip", "pop_75-inf"])
zip_data = pd.read_csv("zip_data.csv", index_col=None)
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))
zip_data = pd.merge(zip_data, pops, how="left", on="zip")
zip_data.to_csv("zip_data.csv")

############### median individ. income

zips = [[zipcode, None] for zipcode in populated_zips["zip"]]

for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B19326_002E", zipcode[0])

with open("median_indiv_income.csv", "w") as fp:
    for item in zips:
        fp.write(str(item[0]))
        fp.write(", ")
        fp.write(str(item[1]))
        fp.write("\n")
        
zip_data = pd.read_csv("zip_data.csv", index_col=None)
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))
incs = pd.DataFrame(zips, columns=["zip", "median_indiv_income"])

zip_data = pd.merge(zip_data, incs, how="left", on="zip")
zip_data.to_csv("zip_data.csv")

######################
# median age
# B01002_001E
zips = [[zipcode, None] for zipcode in populated_zips["zip"]]

for zipcode in tqdm(zips):
    if zipcode[1] is None:
        zipcode[1] = get_census_val(cens, "B01002_001E", zipcode[0])

with open("median_age.csv", "w") as fp:
    for item in zips:
        fp.write(str(item[0]))
        fp.write(", ")
        fp.write(str(item[1]))
        fp.write("\n")
        
zip_data = pd.read_csv("zip_data.csv", index_col=None)
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))
incs = pd.DataFrame(zips, columns=["zip", "median_age"])

zip_data = pd.merge(zip_data, incs, how="left", on="zip")
zip_data.to_csv("zip_data.csv")












#######################
#





























#############
