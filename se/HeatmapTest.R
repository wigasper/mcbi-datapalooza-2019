library(ggplot2)
library(ggmap) # Google maps package
library(RColorBrewer) # Color selection


# Read in RPP/longitude/latitude data 
rpp.data <- read.csv(file='RPP_latlon.csv', header=TRUE)

# Register google maps API key for ggmap function
register_google(key= 'AIzaSyAbiPNQB5LDv38RX9DKVujf2EEgNOP_aIw')

# Get map with the centered on the mean of latitude/longitude values
mean.latitude <- mean(rpp.data[,'lat'])
mean.longitude <- mean(rpp.data[,'lon'])

# Make sure to choose scale 2 or 3 or else not whole US will be shown or too big of map
h.map <- get_map(location = c(mean.longitude, mean.latitude), zoom = 3, scale = 2)
# Convert into ggmap object
h.map <- ggmap(h.map, extent = "device", legend="none")

# Plot heat map layer: polygons with fill colors based on rel. freq. of events
h.map <- h.map + stat_density2d(data=rpp.data, aes(x=lon, y=lat, fill = ..level.., alpha=..level..), geom='polygon')

# DEfine the spectral colors to fill the density contours 
h.map <- h.map + scale_fill_gradientn(colours = rev(brewer.pal(7, "Spectral")))

print(h.map) # Display the plot

