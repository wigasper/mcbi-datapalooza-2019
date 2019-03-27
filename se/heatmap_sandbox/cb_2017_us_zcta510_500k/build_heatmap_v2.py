from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
import matplotlib as mpl
from matplotlib.colors import rgb2hex
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


# Read in population data.
pop_path = "onlyNE.csv"
DF = pd.read_csv(pop_path)
colormap = plt.cm.Purples 

us_shape_file_dir = "/home/sebastian/Documents/mcbi-datapalooza-2019/se/heatmap_sandbox/cb_2017_us_zcta510_500k"
os.chdir(us_shape_file_dir)

# Chicago coordinates.
upperlon = -90.232
lowerlon = -98.323
lowerlat = 39.234
upperlat = 43.213


m = Basemap(
    width=12000000,
    height=12000000,
    llcrnrlon=lowerlon,
    llcrnrlat=lowerlat,
    urcrnrlon=upperlon,
    urcrnrlat=upperlat,
    projection="lcc",
    resolution="l",
    lat_0=lowerlat,
    lat_1=upperlat,
    lon_0=lowerlon,
    lon_1=upperlon
    )


shp_info = m.readshapefile(
    os.path.basename(us_shape_file_dir),'states',drawbounds=True
    )
m.drawrivers()
# Convert integer ZIP5 field to character dtype.
DF['zip'] = DF['zip'].astype(str)

# Read population density info into popdens dict. Take square root of 
# actual density for better color mapping.
popdens = {
    str(i):j for (i, j) in zip(DF.zip.values,DF.score.values)
    }

# Choose a color for each state based on population density. Range
# vmin-vmax has arbitrarily been set to 0-6. Fee lfree to experiment 
# with other ranges.
ziplist = []
colors  = {}
vmin    = 0.
vmax    = 1.0


# Filter m.states_info to only Chicago zipcodes.
zip_info   = m.states_info
popdiv     = (max(popdens.values())/(vmax-vmin))
popdensscl = {i:(j) for (i,j) in popdens.items()}


for d in zip_info:
    iterzip = d["ZCTA5CE10"]
    if iterzip in popdensscl.keys():
        iterpop = popdensscl.get(iterzip,0)
        colors[iterzip] = colormap(iterpop/vmax)[:3]
    ziplist.append(iterzip)


for nshape,seg in enumerate(m.states):
    i, j = zip(*seg)
    if ziplist[nshape] in popdensscl.keys():
        color = rgb2hex(colors[ziplist[nshape]])
        edgecolor = "#000000"
        plt.fill(i,j,color,edgecolor=edgecolor);



# (Optional) include colorbar.
sm = plt.cm.ScalarMappable(
    cmap=colormap,norm=mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    )

mm = plt.cm.ScalarMappable(cmap=colormap)
mm.set_array([vmin, vmax])
plt.colorbar(mm,ticks=np.arange(vmin, vmax+1, 1),orientation="vertical")
plt.title("Chicago Population by ZIP5")
plt.gca().axis("off")
plt.show()
