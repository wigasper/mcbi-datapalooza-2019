#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 09:04:26 2019

@author: wigasper
"""

import os
import re

import numpy as np
import us
from tqdm import tqdm_notebook
import pandas as pd
# Census API wrapper package:
#       https://github.com/datamade/census
from census import Census, CensusException

#os.chdir("/media/wkg/storage/mcbi-datapalooza-2019")
os.chdir("/Users/wigasper/Documents/mcbi-datapalooza-2019")

# Read in 
zip_data = pd.read_csv("zip_data.csv", index_col=None)

# remove pesky "Unnamed" column
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]

# Change zips to str and pad with 0s
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))

# read in
life_exp = pd.read_csv("life_expect_by_census_tract.csv", index_col=None)

# Drop unneeded columns
life_exp = pd.DataFrame(life_exp, columns=['Tract ID', 'e(0)'])
life_exp = life_exp.rename(index=str, columns={"Tract ID": "tract",
                                               "e(0)": "life_expectancy"})

# Convert Census tracts to zip codes
# Read in
zip_to_tract = pd.read_csv("zip_to_tract.csv", index_col=None)

# Change zips to str and pad with 0s
zip_to_tract["zip"] = zip_to_tract["zip"].apply(lambda x: str(x).zfill(5))
zip_to_tract = pd.DataFrame(zip_to_tract, columns=['zip', 'tract'])

# Merge and drop duplicates
life_exp = pd.merge(life_exp, zip_to_tract, how="left", on="tract")
life_exp = life_exp.drop_duplicates("zip")
life_exp = pd.DataFrame(life_exp, columns=['zip', 'life_expectancy'])

# Merge with zip_data
zip_data = pd.merge(zip_data, life_exp, how="left", on="zip")

income = pd.read_csv("16zpallagi.csv", index_col=None)

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

zip_data = pd.merge(zip_data, agis, how="left", on="zip")

income_noagi = pd.read_csv("16zpallnoagi.csv", index_col=None)

income_noagi = pd.DataFrame(income_noagi, columns=["ZIPCODE", "ELDERLY"])
income_noagi = income_noagi.rename(index=str, columns={"ZIPCODE": "zip",
                                                       "ELDERLY": "num_elderly_tax_returns"})
income_noagi["zip"] = income_noagi["zip"].apply(lambda x: str(x).zfill(5))

zip_data = pd.merge(zip_data, income_noagi, how="left", on="zip")

# Read in RPP CBSA-specific data and clean up
rpp = pd.read_csv("RegionalPriceParities.csv")
rpp = rpp[rpp["LineCode"]==1]
rpp = pd.DataFrame(rpp, columns=["GeoFips", "2016"])
rpp = rpp.rename(index=str, columns={"GeoFips": "cbsa", "2016": "rpp"})

# cbsa_to_zip to convert between CBSA and zip codes
cbsa_to_zip = pd.read_csv("cbsa_to_zip.csv")
cbsa_to_zip["zip"] = cbsa_to_zip["zip"].apply(lambda x: str(x).zfill(5))
cbsa_to_zip = pd.DataFrame(cbsa_to_zip, columns=["zip", "cbsa"])

# merge CBSAs to zip codes, drop duplicates due to redundant CBSAs (probably due to 
# abritrary geographic decisions, some zip codes have multiple CBSAs)
zip_data = pd.merge(zip_data, cbsa_to_zip, how="left", on="zip")
zip_data = zip_data.drop_duplicates("zip")

# merge in RPP data
zip_data = pd.merge(zip_data, rpp, how="left", on="cbsa")
# drop CBSA column
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains("cbsa")]

# read in
rpp_state = pd.read_csv("RPP_by_state_w_portions.csv", index_col=None)

# Drop Metropolitan data
rpp_state = rpp_state.loc[rpp_state.GeoName.str.contains("Nonmetropolitan"), :]
rpp_state = rpp_state[rpp_state["LineCode"]==1]

# Clean up state names
pat = r"^(.*)\s\(Nonmetropolitan Portion\)"
rpp_state["GeoName"] = rpp_state["GeoName"].apply(lambda x: re.sub(pat, r"\1", x))

# Need to convert names to two letter codes
states_dict = us.states.mapping("name", "abbr")
rpp_state["GeoName"] = rpp_state["GeoName"].apply(lambda x: states_dict[x])
rpp_state = pd.DataFrame(rpp_state, columns=["GeoName", "2016"])

# Some states don't have nonmetro areas, setting these values manually to the metro area values
rpp_state.loc[[64], ["2016"]] = 100.3
rpp_state.loc[[72], ["2016"]] = 116.4
rpp_state.loc[[248], ["2016"]] = 113.5
rpp_state.loc[[320], ["2016"]] = 99.8

# Change rpp_state to dict to allow us to easily replace NAs in the DF with the state
# non-metro RPP 
rpp_state = rpp_state.set_index("GeoName").T.to_dict("list")

# Fill NAs with their state abbreviation
zip_data.rpp = zip_data.rpp.fillna(zip_data.state)

# Get RPP function
# Above, we filled NAs for the RPP variable with the containing state abbreviation, this function
# replaces that state abbreviation with the non-metro RPP for the state
def get_rpp_for_state(rpp):
    if re.match("[^\d]{2}", rpp):
        if rpp in rpp_state.keys():
            return rpp_state[rpp][0]
        else:
            return np.nan
    else:
        return rpp

zip_data["rpp"] = zip_data["rpp"].apply(lambda x: get_rpp_for_state(x))

zip_data["freq_pop_45-49"] = zip_data["pop_45-49"] / zip_data["population"]
zip_data["freq_pop_50-54"] = zip_data["pop_50-54"] / zip_data["population"]
zip_data["freq_pop_55-59"] = zip_data["pop_55-59"] / zip_data["population"]
zip_data["freq_pop_60-64"] = zip_data["pop_60-64"] / zip_data["population"]
zip_data["freq_pop_65-69"] = zip_data["pop_65-69"] / zip_data["population"]
zip_data["freq_pop_70-74"] = zip_data["pop_70-74"] / zip_data["population"]
zip_data["freq_pop_75-inf"] = zip_data["pop_75-inf"] / zip_data["population"]


zip_data["median_indiv_income"] = zip_data["median_indiv_income"].clip(lower=0)
