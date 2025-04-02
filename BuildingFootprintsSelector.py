from typing import TypeAlias

import geopandas as gpd
import geopy.geocoders
import pyproj
from time import sleep
class BuildingFootprintsGeocoder:
    """The purpose of this class is to use the geopy package to interface with API's of geocoding services.
    This script allows for easy geocoding of building footprints, particularly from Microsoft's USBuildingFootprints."""
    def __init__(self, 
                 microsoft_footprints:str, 
                 mask:gpd.GeoDataFrame | gpd.GeoSeries, 
                 geocoder:geopy.geocoders,
                 rate_limit:int = 4):
        self.microsoft_footprints = microsoft_footprints
        self.CRS = pyproj.CRS(4326) # Ensures all data follows same projection
        self.mask = mask
        self.geocoder = geocoder
        self.start_count = 0
        self.total_count = None
        self.geocoded_footprints = None
        self.rate_limit = rate_limit

    
    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, x):
        if x.crs == self.CRS:
            self._mask = x
        else:
            x = x.to_crs(self.crs)
            return x

    @property
    def rate_limit(self):
        return self._rate_limit

    @rate_limit.setter
    def rate_limit(self, x):
        if type(x) is int:
            self._rate_limit = x
        else:
            raise TypeError(f"The rate_limit argument should be int, not {type(x)}.")


    def _reverse_geocode_point(self, lat, long):
        """This is a helper method that geocodes a lat/long coordinate that is in the WGS84 projection"""
        address = self.geocoder.reverse((long, lat), exactly_one=True)
        self.start_count += 1
        print(f"Progress of reverse geocoding: {self.start_count} out of {self.total_count}")
        sleep(self.rate_limit) # For rate limiting API calls. One second is minimum, so want to respect API policy.
        
        if address is None:
            return "No address found."
        else:
            return address.address

    def _mask_building_footprints(self):
        """This is a quick method to mask building footprints to a polygon."""
        masked_footprints = gpd.read_file(self.microsoft_footprints, mask=self.mask)
        self.total_count = masked_footprints.shape[0]
        if masked_footprints.crs != self.CRS:
            masked_footprints = masked_footprints.to_crs(self.CRS)
        else:
            pass
        return masked_footprints

    def reverse_geocode_footprints(self, crs) -> gpd.GeoDataFrame:
        """This method geocodes the footprints in the featureclass based on their centroids and joins the geocoded results to the polygon."""
        footprints = self._mask_building_footprints()
        footprints.loc[:, "centroid"] = footprints.to_crs(crs).centroid.to_crs(self.CRS) # Need to reproject CRS to get accurate centroid from geopandas
        footprints.loc[:, "address"] = footprints.loc[:, "centroid"].apply(lambda coord: self._reverse_geocode_point(coord.x,coord.y))
        footprints = footprints.drop(columns=["centroid"])
        self.geocoded_footprints = footprints
        return footprints
    
    def address_parser(self, geocoded_footprint:gpd.GeoDataFrame):
        """This method parses addresses based on the list returned by the geopy geocoder."""
        def parser(address):
            if address == "No address found.":
                return None
            parsed_address = address.split(",")
            if len(parsed_address) == 8:
                parsed_address = f"{parsed_address[1]} {parsed_address[2]}\n{parsed_address[3]}, {parsed_address[5]} {parsed_address[6]}"
            elif len(parsed_address) == 7:
                parsed_address = f"{parsed_address[0]} {parsed_address[1]}\n{parsed_address[2]}, {parsed_address[4]} {parsed_address[5]}"
            elif len(parsed_address) == 6:
                parsed_address = f"{parsed_address[0]}\n{parsed_address[1]}, {parsed_address[3]} {parsed_address[4]}"
            elif len(parsed_address) < 6:
                return "Not enough data to parse."
            return parsed_address

        geocoded_footprint.loc[:, "parsed_address"] = geocoded_footprint["address"].apply(parser)
        return geocoded_footprint