#
# Assignment5 Interface
# Name: 
#

from pymongo import MongoClient
import os
import sys
import json
from math import cos, sin, sqrt, atan2, radians 

#Method to find Business Based on a city
def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):
    # Business Documents Based on a City to Search
    business_documents = collection.find({'city': {'$regex':cityToSearch, '$options':"$i"}})
    with open(saveLocation1, "w") as file:
        #Iterate for each Business Document
        for business_doc in business_documents:
            #Get the attributes for each business
            bussiness_name = business_doc['name']
            bussiness_address = business_doc['full_address'].replace("\n", ", ")
            business_city = business_doc['city']
            business_state = business_doc['state']
            #Write all the retrieved attributes to the output file
            file.write(bussiness_name.upper() + "$" + bussiness_address.upper() + "$" + business_city.upper() + "$" + business_state.upper() + "\n")

#Method to find Business Based on a Location
def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):
    # Business Documents Based on a Category to Search
    business_documents = collection.find({'categories':{'$in': categoriesToSearch}}, {'name': 1, 'latitude': 1, 'longitude': 1, 'categories': 1})
    # Latitude and Longitude of the Location 1
    latitude_first = float(myLocation[0])
    longitude_first = float(myLocation[1])
    with open(saveLocation2, "w") as file:
        #Iterate for each Business Document
        for business_doc in business_documents:
            #Get the attributes for each business
            business_name = business_doc['name']
            latitude_second = float(business_doc['latitude'])
            longitude_second = float(business_doc['longitude'])
            #Find out the distance between two locations based on latitudes and longitudes of both locations
            distanceBetweenLocations = DistanceBetweenLocationsFunc(latitude_second, longitude_second, latitude_first, longitude_first)
            #Check if the distance between locations is less than maxDistance
            if distanceBetweenLocations <= maxDistance:
                #Write all conditionally satisfying retrieved business names to output file
                file.write(business_name.upper() + "\n")
                
#Method to find Distance between two locations based on latitudes and longitudes                
def DistanceBetweenLocationsFunc(latitude_second, longitude_second, latitude_first, longitude_first):
    r = 3959
    #pi of latitude 1 and latitude 2
    rpi_latitude1 = radians(latitude_first)
    rpi_latitude2 = radians(latitude_second)
    #Find out the delta pi between two latitudes
    deltapi_latitudes = radians(latitude_second-latitude_first)
    #Find out the delta lamdba between two latitudes
    deltalambda_longitudes = radians(longitude_second-longitude_first)
    p = (sin(deltapi_latitudes/2) * sin(deltapi_latitudes/2)) + (cos(rpi_latitude1) * cos(rpi_latitude2) * sin(deltalambda_longitudes/2) * sin(deltalambda_longitudes/2))
    q = 2 * atan2(sqrt(p), sqrt(1-p))
    #Find out the final distance by multiplying r with q
    finalDistance = r * q
    
    #Return finalDistance calculated between two locations as Output
    return finalDistance

