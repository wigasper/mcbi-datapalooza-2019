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

rpp_state = pd.read_csv("RPP_by_state.csv", index_col=None)
