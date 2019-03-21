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

#note: need to change this jion!!!!!
zip_data = pd.merge(zip_data, agis, how="inner", on="zip")

zip_data = pd.merge(zip_data, income_noagi, how="inner", on="zip")

###############################

rpp = pd.read_csv("RegionalPriceParities.csv")
rpp = rpp[rppcc["LineCode"]==1]
