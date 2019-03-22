import os

import pandas as pd

os.chdir("/media/wkg/storage/mcbi-datapalooza-2019")

income = pd.read_csv("16zpallagi.csv", index_col=None)

income_noagi = pd.read_csv("16zpallnoagi.csv", index_col=None)
income_noagi = pd.DataFrame(income_noagi, columns=["ZIPCODE", "ELDERLY"])
income_noagi = income_noagi.rename(index=str, columns={"ZIPCODE": "zip",
                                                       "ELDERLY": "num_elderly_tax_returns"})
income_noagi["zip"] = income_noagi["zip"].apply(lambda x: str(x).zfill(5))

agis = pd.DataFrame(income, columns=["zipcode", "agi_stub", "N1"])

agis = pd.pivot_table(agis, values="N1", index="zipcode", columns="agi_stub")
agis = agis.reset_index()

agis["zipcode"] = agis["zipcode"].apply(lambda x: str(x).zfill(5))

agis = agis.rename(index=str, columns={"zipcode": "zip",
                                       1: "num_tax_returns_0-25k",
                                       2: "num_tax_returns_25k-50k",
                                       3: "num_tax_returns_50k-75k",
                                       4: "num_tax_returns_75k-100k",
                                       5: "num_tax_returns_100k-200k",
                                       6: "num_tax_returns_200k-inf"})

agis = agis[1:]

zip_data = pd.read_csv("zipcodes.csv", index_col=None)

# remove pesky "Unnamed" column
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]

# Change zips to str and pad with 0s
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))

zip_data = pd.merge(zip_data, agis, how="left", on="zip")

zip_data = pd.merge(zip_data, income_noagi, how="left", on="zip")

###############################

cbsa_to_zip = pd.read_csv("cbsa_to_zip.csv")
cbsa_to_zip["zip"] = cbsa_to_zip["zip"].apply(lambda x: str(x).zfill(5))

cbsa_to_zip = pd.DataFrame(cbsa_to_zip, columns=["zip", "cbsa"])

zip_data = pd.merge(zip_data, cbsa_to_zip, how="left", on="zip")
zip_data = zip_data.drop_duplicates("zip")

rpp = pd.read_csv("RegionalPriceParities.csv")
rpp = rpp[rpp["LineCode"]==1]
rpp = pd.DataFrame(rpp, columns=["GeoFips", "2016"])
rpp = rpp.rename(index=str, columns={"GeoFips": "cbsa", "2016": "rpp"})

zip_data = pd.merge(zip_data, rpp, how="left", on="cbsa")


zip_data = zip_data.loc[:, ~zip_data.columns.str.contains("cbsa")]

###############
# read in
rpp_state = pd.read_csv("RPP_by_state_w_portions.csv", index_col=None)

# drop Metropolitan data
rpp_state = rpp_state.loc[rpp_state.GeoName.str.contains("Nonmetropolitan"), :]
rpp_state = rpp_state[rpp_state["LineCode"]==1]



###### regex test
import re
import us
import math

pat = r"^(.*)\s\(Nonmetropolitan Portion\)"
    
rpp_state["GeoName"] = rpp_state["GeoName"].apply(lambda x: 
                                                    re.sub(pat, r"\1", x))
    
states_dict = us.states.mapping("name", "abbr")

rpp_state["GeoName"] = rpp_state["GeoName"].apply(lambda x: 
                                                    states_dict[x])
rpp_state = pd.DataFrame(rpp_state, columns=["GeoName", "2016"])

# Some states don't have nonmetro areas, setting these values manually to the
# metro area values
rpp_state.loc[[64], ["2016"]] = 100.3
rpp_state.loc[[72], ["2016"]] = 116.4
rpp_state.loc[[248], ["2016"]] = 113.5
rpp_state.loc[[320], ["2016"]] = 99.8

# separate zip_data into 2 DFs based on whether we have a value for 
#zip_data_rpp_valid = zip_data[zip_data["rpp"]>=0]

import numpy as np
# change rpp_state to dict
rpp_state = rpp_state.set_index("GeoName").T.to_dict("list")

zip_data.rpp = zip_data.rpp.fillna(zip_data.state)

zip_data["rpp"] = zip_data["rpp"].apply(lambda x: get_rpp_for_state(x))

def get_rpp_for_state(rpp):
    if re.match("[^\d]{2}", rpp):
        if rpp in rpp_state.keys():
            return rpp_state[rpp][0]
        else:
            return np.nan
    else:
        return rpp


nans = 0
if math.isnan(zip_data["rpp"].values[0]):
    nans += 1





math.isnan(zip_data.loc[[0],['rpp']].values[0])
def rpp_modifier(val):
    if math.isnan(val):

for sample in zip_data:
    if math.isnan(sample["rpp"].values[0]):
        sample["rpp"].values[0] = 