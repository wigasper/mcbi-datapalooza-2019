#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:07:05 2019

@author: wkg
"""

import os

import pandas as pd

os.chdir("/media/wkg/storage/mcbi-datapalooza-2019")

income = pd.read_csv("16zpallagi.csv", index_col=None)

agis = pd.DataFrame(income, columns=["zipcode", "agi_stub", "N1"])

agis = pd.pivot_table(agis, values="N1", index="zipcode", columns="agi_stub")
agis = agis.reset_index()

agis["zipcode"] = agis["zipcode"].apply(lambda x: str(x).zfill(5))

agis = agis.rename(index=str, columns={1: "num_returns_0_to_25k",
                                       2: "num_returns_25k_to_50k",
                                       3: "num_returns_50k_to_75k",
                                       4: "num_returns_75k_to_100k",
                                       5: "num_returns_100k_to_200k",
                                       6: "num_returns_200k_to_inf"})

agis = agis[1:]

