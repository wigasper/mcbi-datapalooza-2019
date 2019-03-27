"""
Render a 2D map of Chicago with zip code boundaries.
"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os
import os.path


us_shape_file_dir = "/home/sebastian/Documents/mcbi-datapalooza-2019/se/heatmap_sandbox/cb_2017_us_zcta510_500k"
os.chdir(us_shape_file_dir)

# Chicago coordinates.
upperlon = -69
lowerlon = -80
lowerlat = 24.5548
upperlat = 45.5

m = Basemap(
    llcrnrlon=lowerlon,
    llcrnrlat=lowerlat,
    urcrnrlon=upperlon,
    urcrnrlat=upperlat,
    resolution='l',
    projection='cyl',
    lat_0=lowerlat,
    lat_1=upperlat,
    lon_0=lowerlon,
    lon_1=upperlon
    )


shp_info = m.readshapefile(os.path.basename(us_shape_file_dir), 'state')
plt.gca().axis("off")
plt.show()
