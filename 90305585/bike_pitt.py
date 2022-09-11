import argparse
import collections
import csv
import json
import glob
import math
import os
import pandas
import re
import requests
import string
import sys
import time
import xml

from requests.api import get

class Bike():
    def __init__(self, baseURL, station_info, station_status):
        # initialize the instance
    
        self.info=json.loads(get(baseURL+station_info,verify=False).content)
        self.status=json.loads(get(baseURL+station_status,verify=False).content)
       
       # pass

    def total_bikes(self):
        sum=0
        for avail in self.status["data"]["stations"]:
            sum+=int(avail["num_bikes_available"])

        return sum

            


        # return the total number of bikes available
        return None

    def total_docks(self):
        sum=0
        for avail in self.status["data"]["stations"]:
            sum+=int(avail["num_docks_available"])

        return sum

        # return the total number of docks available
        return None

    def percent_avail(self, station_id):
        data=self.status["data"]["stations"]
       

        for num in data:
            if(int(num["station_id"])==station_id):
                bike=num["num_bikes_available"]
                dock=num["num_docks_available"]
                percent=int(dock/(dock+bike)*100)
                result=str(percent)+"%"
                return result
        
        return ""


        

        


        # return the percentage of available docks

       

    def closest_stations(self, latitude, longitude):
        data=self.info["data"]["stations"]
        res=[]
       
        result=None

        for station in data:
            res.append([station,self.distance(station["lat"],station["lon"],latitude,longitude)])

        res2= sorted(res,key=lambda distance: distance[1])

        

        
        result={res2[0][0]["station_id"]:res2[0][0]["name"],res2[1][0]["station_id"]:res2[1][0]["name"],res2[2][0]["station_id"]:res2[2][0]["name"]}


        return result
        

            
        
            
        


       
            

        


        # return the stations closest to the given coordinates
    def closest_bike(self, latitude, longitude):
        data=self.info["data"]["stations"]
        data2=self.status["data"]["stations"]
        res=[]
       
       

        for station in data:
            res.append([station,self.distance(station["lat"],station["lon"],latitude,longitude)])
        
        res2= sorted(res,key=lambda distance: distance[1])

        for bike in res2:
            for bike2 in data2:
                if(bike[0]["station_id"]==bike2["station_id"] and int(bike2["num_bikes_available"])>0):
                    return {bike[0]["station_id"]:bike[0]["name"]}
                    

        return { }
        



        # return the station with available bikes closest to the given coordinates
        
        
    def station_bike_avail(self, latitude, longitude):
        data=self.info["data"]["stations"]
        data2=self.status["data"]["stations"]
        res=[]


        for bike in data:
            if float(bike["lat"]) ==latitude and float(bike["lon"])==longitude:
                for num in data2:
                    if(num["station_id"]==bike["station_id"]):
                        return {num["station_id"]:int(num["num_bikes_available"])}
        return {}
                
       

        

        
        # return the station id and available bikes that correspond to the station with the given coordinates
        
        

    def distance(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - math.cos((lat2-lat1)*p)/2 + math.cos(lat1*p)*math.cos(lat2*p) * (1-math.cos((lon2-lon1)*p)) / 2
        return 12742 * math.asin(math.sqrt(a))


# testing and debugging the Bike class

if __name__ == '__main__':
    instance = Bike('https://api.nextbike.net/maps/gbfs/v1/nextbike_pp/en', '/station_information.json', '/station_status.json')
    print('------------------total_bikes()-------------------')
    t_bikes = instance.total_bikes()
    print(type(t_bikes))
    print(t_bikes)
    print()

    print('------------------total_docks()-------------------')
    t_docks = instance.total_docks()
    print(type(t_docks))
    print(t_docks)
    print()

    print('-----------------percent_avail()------------------')
    p_avail = instance.percent_avail(342885) # replace with station ID
    print(type(p_avail))
    print(p_avail)
    print()

    print('----------------closest_stations()----------------')
    c_stations = instance.closest_stations(40.444618, -79.954707) # replace with latitude and longitude
    print(type(c_stations))
    print(c_stations)
    print()

    print('-----------------closest_bike()-------------------')
    c_bike = instance.closest_bike(40.444618, -79.954707) # replace with latitude and longitude
    print(type(c_bike))
    print(c_bike)
    print()

    print('---------------station_bike_avail()---------------')
    s_bike_avail = instance.station_bike_avail(40.438761, -79.997436) # replace with exact latitude and longitude of station
    print(type(s_bike_avail))
    print(s_bike_avail)
