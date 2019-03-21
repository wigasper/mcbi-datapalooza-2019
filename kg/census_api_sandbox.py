#!/usr/bin/env python3
import os

import pandas as pd
from census import Census
from us import states

os.chdir("/media/wkg/storage/mcbi-datapalooza-2019")

zip_data = pd.read_csv("zipcodes.csv", index_col=None)
zip_data = zip_data.loc[:, ~zip_data.columns.str.contains('Unnamed')]

cens = Census("641afb80c092a21ba85b039d816e211551bccad4")

cens.acs5.zipcode()

B00001_001E


cens.acs5.zipcode("S0101_C01_001E", 68154)

cens.sf1.state_zipcode("B00001_001E", 31, 68154)


cens.acs5.get(('NAME', 'B00001_001E'), {'for': 'state:{}'.format(states.NE.fips)})
