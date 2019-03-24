#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 15:39:29 2019

@author: wkg
"""

import os

import pandas as pd

os.chdir("/media/wkg/storage/mcbi-datapalooza-2019")

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

# pull in zip_data
zip_data = pd.read_csv("zip_data.csv", index_col=None)

# remove pesky "Unnamed" column
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]

# Change zips to str and pad with 0s
zip_data["zip"] = zip_data["zip"].apply(lambda x: str(x).zfill(5))

zip_data = pd.merge(zip_data, life_exp, how="left", on="zip")
