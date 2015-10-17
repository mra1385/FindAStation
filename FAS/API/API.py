# import modules
from math import radians, cos, sin, asin, sqrt
import urllib
import xml.etree.ElementTree as ET
from operator import itemgetter

# create class with station geocoordinates/status, and methods to find nearest bikes and docks
class LoadStations():
    """ class loads stations with geo coordinates
    """
    def __init__(self):
        xml_path = 'https://www.capitalbikeshare.com/data/stations/bikeStations.xml'
        tree = ET.parse(urllib.urlopen(xml_path))
        root = tree.getroot()
        station_location = dict()
        for child in root:
            tmp_lst = {'Latitude' : float(child[4].text), 'Longitude' : float(child[5].text)}
            station_location[child[1].text] = tmp_lst
        self.station_lst = station_location


    def station_status(self):
        """
        Loads bikeshare xml feed with station status
        and adds number of bikes and docks to dictionary
        """
        xml_path = 'https://www.capitalbikeshare.com/data/stations/bikeStations.xml'
        station_status = dict()
        tree = ET.parse(urllib.urlopen(xml_path))
        root = tree.getroot()
        for child in root:
            station_status[child[1].text] = [child[12].text, child[13].text]
        return station_status


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


    def find_closest_bike(self, latitude, longitude):
        """
        Funds closest station with available bike based on passed geocoordinates
        and returns sorted list of three closest stations
        """
        closest_station = []
        station_availability = self.station_status()
        for station in self.station_lst.keys():
            if int(station_availability[station][0]) >= 2:
                closest_station.append([station, self.distance(float(longitude), float(latitude), self.station_lst[station]['Longitude'],
                                        self.station_lst[station]['Latitude']), station_availability[station][0], self.station_lst[station]['Latitude'],
                                        self.station_lst[station]['Longitude']])
            else:
                continue
        return sorted(closest_station, key=itemgetter(1))


    def find_closest_dock(self, latitude, longitude):
        """
        Funds closest station with available bike based on passed geocoordinates
        and returns sorted list of three closest stations
        """
        closest_station = []
        station_availability = self.station_status()
        for station in self.station_lst.keys():
            if int(station_availability[station][1]) >= 2:
                closest_station.append([station, self.distance(float(longitude), float(latitude), self.station_lst[station]['Longitude'],
                                        self.station_lst[station]['Latitude']), station_availability[station][1], self.station_lst[station]['Latitude'],
                                        self.station_lst[station]['Longitude']])
            else:
                continue
        return sorted(closest_station, key=itemgetter(1))