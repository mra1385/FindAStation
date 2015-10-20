# import modules
from math import radians, cos, sin, asin, sqrt
import urllib
import json
import xml.etree.ElementTree as ET
from operator import itemgetter

# create class with station geocoordinates/status, and methods to find nearest bikes and docks
class LoadStations:
    """ class loads stations with geo coordinates
    """
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

        # converts latitude/longitude into country/city name using Google Maps API
        url = "http://maps.googleapis.com/maps/api/geocode/json?"
        url += "latlng=%s,%s&sensor=false" % (latitude, longitude)
        v = urllib.urlopen(url).read()
        j = json.loads(v)
        components = j['results'][0]['address_components']
        country = town = None
        for c in components:
            if "country" in c['types']:
                country = c['long_name']
            if "locality" in c['types']:
                town = c['long_name']

        # query CaBi for station locations and status if country/city is United States/Washington
        if country.encode('ascii','ignore') == 'United States' and town.encode('ascii','ignore') == 'Washington':
            xml_path = 'https://www.capitalbikeshare.com/data/stations/bikeStations.xml'
            tree = ET.parse(urllib.urlopen(xml_path))
            root = tree.getroot()
            station_location = dict()
            station_status = dict()
            for child in root:
                station_location[child[1].text] = {'Latitude' : float(child[4].text), 'Longitude' : float(child[5].text)}
                station_status[child[1].text] = [child[12].text, child[13].text]
            self.station_location = station_location
            self.station_status = station_status

        # query Citi Bike for station locations and status if country/city is United States/New York
        elif country.encode('ascii','ignore') == 'United States' and town.encode('ascii','ignore') == 'New York':
            station_location = dict()
            station_status = dict()
            url = 'https://www.citibikenyc.com/stations/json'
            v = urllib.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = {'Latitude': i['latitude'], 'Longitude': i['longitude']}
                station_status[i['stationName']] = [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status

        # query Divvy Bike for station locations and status if country/city is United States/Chicago
        elif country.encode('ascii','ignore') == 'United States' and town.encode('ascii','ignore') == 'Chicago':
            station_location = dict()
            station_status = dict()
            url = 'https://www.divvybikes.com/stations/json'
            v = urllib.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = {'Latitude': i['latitude'], 'Longitude': i['longitude']}
                station_status[i['stationName']] = [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status


    def distance(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return round(km * 0.621371,2 )


    def find_closest_bike(self):
        """
        Funds closest station with available bike based on passed geocoordinates
        and returns sorted list of three closest stations
        """
        closest_station = []
        station_availability = self.station_status
        for station in self.station_location.keys():
            if int(station_availability[station][0]) >= 2:
                closest_station.append([station, self.distance(float(self.longitude), float(self.latitude), self.station_location[station]['Longitude'],
                                        self.station_location[station]['Latitude']), station_availability[station][0], self.station_location[station]['Latitude'],
                                        self.station_location[station]['Longitude']])
            else:
                continue
        return sorted(closest_station, key=itemgetter(1))[0:5]


    def find_closest_dock(self):
        """
        Funds closest station with available bike based on passed geocoordinates
        and returns sorted list of three closest stations
        """
        closest_station = []
        station_availability = self.station_status
        for station in self.station_location.keys():
            if int(station_availability[station][1]) >= 2:
                closest_station.append([station, self.distance(float(self.longitude), float(self.latitude), self.station_location[station]['Longitude'],
                                        self.station_location[station]['Latitude']), station_availability[station][1], self.station_location[station]['Latitude'],
                                        self.station_location[station]['Longitude']])
            else:
                continue
        return sorted(closest_station, key=itemgetter(1))[0:5]