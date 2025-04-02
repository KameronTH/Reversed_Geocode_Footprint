**Creator**: Kameron Hall\
**Date**: 2025-03-16\
**Programming Language**: Python\
**Packages used**: Geopandas, pandas\
**Update Frequency**: Occasionally
# Purpose
The purpose of this project was to show my proficiency in data manipulation and visualization using QGIS and python.
In this example, I utilized the [geopy](https://geopy.readthedocs.io/en/stable/) python module to interface with the [Nominatim API](https://nominatim.org/) to reverse geocode building footprints
from [Microsoft's Building Footprint](https://github.com/microsoft/USBuildingFootprints?tab=readme-ov-file) data. This was just an example, and I do not recommend using Nominatim for bulk geocoding as it can be intensive on the server.

# Files Overview

## Layouts/Finals/2025-03-16 Reversed Geocoded MS Footprints.png
![Reversed Geocoded MS Footprints](Layouts/Finals/2025-03-16 Reversed Geocoded MS Footprints.png)
A layout showing the addresses of the reverse geocoded footprints in relation to non-geocoded footprints.

## BuildingFootprintsSelector.py
This script contains a class I created to reverse geocode, extract addresses from geometry, building footprints which 
were stored in a geojson file format. I use geopandas to manipulate spatial data.The geocoding was tested using Nominatim, 
but should work with other geopy geocoders.

# Acknowledgements
[Microsoft's US Building Footprints](https://github.com/microsoft/USBuildingFootprints?tab=readme-ov-file)\
[© OpenStreetMap contributors](https://www.openstreetmap.org/copyright)\
[Geopandas](https://geopandas.org/en/stable/)\
[geopy](https://geopy.readthedocs.io/en/stable/)\
[QGIS](https://qgis.org/) 
