# import modules
from math import radians, cos, sin, asin, sqrt
import urllib
import json
import xml.etree.ElementTree as ET
from operator import itemgetter


# create class with station coordinates/status, and methods to
# find nearest bikes and docks
class LoadStations:
    """ class loads stations with geo coordinates
    """
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

        # converts latitude/longitude into country/city name using
        # Google Maps API
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

        # query CaBi for station locations and status if country/city is
        # United States/Washington area
        if country.encode('ascii', 'ignore') == 'United States' \
                and town.encode('ascii', 'ignore') in ['Washington',
                                                       'Arlington',
                                                       'Alexandria']:
            xml_path = 'https://www.capitalbikeshare.com/data/stations/' \
                       'bikeStations.xml'
            tree = ET.parse(urllib.urlopen(xml_path))
            root = tree.getroot()
            station_location = dict()
            station_status = dict()
            for child in root:
                station_location[child[1].text] = \
                    {'Latitude': float(child[4].text),
                     'Longitude': float(child[5].text)}
                station_status[child[1].text] = [child[12].text, child[13].text]
            self.station_location = station_location
            self.station_status = station_status

        # query Citi Bike for station locations and status if country/city is
        # United States/New York
        elif country.encode('ascii', 'ignore') == 'United States' \
                and town.encode('ascii', 'ignore') in ['New York']:
            station_location = dict()
            station_status = dict()
            url = 'https://www.citibikenyc.com/stations/json'
            v = urllib.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = \
                    {'Latitude': i['latitude'],
                     'Longitude': i['longitude']}
                station_status[i['stationName']] = \
                    [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status

        # query Divvy Bike for station locations and status if country/city is
        # United States/Chicago
        elif country.encode('ascii', 'ignore') == 'United States' \
                and town.encode('ascii', 'ignore') in ['Chicago']:
            station_location = dict()
            station_status = dict()
            url = 'https://www.divvybikes.com/stations/json'
            v = urllib.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = \
                    {'Latitude': i['latitude'], 'Longitude': i['longitude']}
                station_status[i['stationName']] = \
                    [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status

        # query Bikeshare Toronto for station locations and status if
        # country/city is Canada/Toronto
        elif country.encode('ascii', 'ignore') == 'Canada' \
                and town.encode('ascii', 'ignore') in ['Toronto']:
            station_location = dict()
            station_status = dict()
            url = 'http://www.bikesharetoronto.com/stations/json'
            v = urllib.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = \
                    {'Latitude': i['latitude'], 'Longitude': i['longitude']}
                station_status[i['stationName']] = \
                    [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status

        # query Bay Area Bikes for station locations and status if
        # country/city is United States/San Francisco Bay area
        elif country.encode('ascii', 'ignore') == 'United States' \
                and town.encode('ascii', 'ignore') in ['San Francisco',
                                                       'Palo Alto',
                                                       'Redwood City',
                                                       'Mountain View',
                                                       'San Jose']:
            station_location = dict()
            station_status = dict()
            url = 'http://www.bayareabikeshare.com/stations/json'
            v = urllib.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = \
                    {'Latitude': i['latitude'], 'Longitude': i['longitude']}
                station_status[i['stationName']] = \
                    [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status

        elif country.encode('ascii', 'ignore') == 'United States' \
                and town.encode('ascii', 'ignore') in ['Philadelphia']:
            station_location = dict()
            station_status = dict()
            url = 'https://api.phila.gov/bike-share-stations/v1'

            class MyOpener(urllib.FancyURLopener):
                version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; ' \
                      'rv:1.8.1.11)Gecko/20071127 Firefox/2.0.0.11'

            myopener = MyOpener()
            v = myopener.open(url)
            j = json.load(v)
            for i in j['features']:
                station_location[i['properties']['name']] = \
                    {'Latitude': float(i['geometry']['coordinates'][1]),
                     'Longitude': float(i['geometry']['coordinates'][0])}
                station_status[i['properties']['name']] = \
                    [i['properties']['bikesAvailable'],
                     i['properties']['docksAvailable']]
            self.station_location = station_location
            self.station_status = station_status

        # query Bay Area Bikes for station locations and status if
        # country/city is Canada/Montreal
        elif country.encode('ascii', 'ignore') == 'Canada' \
                and town.encode('ascii', 'ignore') in ['Montral']:
            xml_path = 'http://montreal.bixi.com/data/bikeStations.xml'
            tree = ET.parse(urllib.urlopen(xml_path))
            root = tree.getroot()
            station_location = dict()
            station_status = dict()
            for child in root:
                station_location[child[1].text.encode('utf-8')] = \
                    {'Latitude': float(child[3].text),
                     'Longitude': float(child[4].text)}
                station_status[child[1].text.encode('utf-8')] = \
                    [child[11].text, child[12].text]
            self.station_location = station_location
            self.station_status = station_status

        # query Bay Area Bikes for station locations and status if
        # country/city is United Kingdom/London
        elif country.encode('ascii', 'ignore') == 'United Kingdom' \
                and town.encode('ascii', 'ignore') in ['London']:
            xml_path = 'https://tfl.gov.uk/tfl/syndication/feeds/' \
                       'cycle-hire/livecyclehireupdates.xml'
            tree = ET.parse(urllib.urlopen(xml_path))
            root = tree.getroot()
            station_location = dict()
            station_status = dict()
            for child in root:
                station_location[child[1].text] = \
                    {'Latitude': float(child[3].text),
                     'Longitude': float(child[4].text)}
                station_status[child[1].text] = [child[10].text, child[11].text]
            self.station_location = station_location
            self.station_status = station_status

        # query Bay Area Bikes for station locations and status if
        # country/city is United States/Boston
        elif country.encode('ascii', 'ignore') == 'United States' \
                and town.encode('ascii', 'ignore') in ['Boston']:
            xml_path = 'http://www.thehubway.com/data/stations/bikeStations.xml'
            tree = ET.parse(urllib.urlopen(xml_path))
            root = tree.getroot()
            station_location = dict()
            station_status = dict()
            for child in root:
                station_location[child[1].text] = \
                    {'Latitude': float(child[4].text),
                     'Longitude': float(child[5].text)}
                station_status[child[1].text] = [child[12].text, child[13].text]
            self.station_location = station_location
            self.station_status = station_status

        # query Bay Area Bikes for station locations and status if
        # country/city is United States/Minneapolis
        elif country.encode('ascii', 'ignore') == 'United States' \
                and town.encode('ascii', 'ignore') in ['Minneapolis']:
            xml_path = 'https://secure.niceridemn.org/data2/bikeStations.xml'
            tree = ET.parse(urllib.urlopen(xml_path))
            root = tree.getroot()
            station_location = dict()
            station_status = dict()
            for child in root:
                station_location[child[1].text] = \
                    {'Latitude': float(child[5].text),
                     'Longitude': float(child[6].text)}
                station_status[child[1].text] = [child[13].text, child[14].text]
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
        return round(km * 0.621371, 2)

    def find_closest_bike(self):
        """
        Funds closest station with available bike based on passed coordinates
        and returns sorted list of three closest stations
        """
        closest_station = []
        station_availability = self.station_status
        for station in self.station_location.keys():
            if int(station_availability[station][0]) >= 2:
                closest_station.append(
                    [station,
                     self.distance(float(self.longitude),
                                   float(self.latitude),
                                   self.station_location[station]['Longitude'],
                                   self.station_location[station]['Latitude']),
                     station_availability[station][0],
                     self.station_location[station]['Latitude'],
                     self.station_location[station]['Longitude']])
            else:
                continue
        return sorted(closest_station, key=itemgetter(1))[0:5]

    def find_closest_dock(self):
        """
        Funds closest station with available bike based on passed coordinates
        and returns sorted list of three closest stations
        """
        closest_station = []
        station_availability = self.station_status
        for station in self.station_location.keys():
            if int(station_availability[station][1]) >= 2:
                closest_station.append(
                    [station,
                     self.distance(float(self.longitude),
                                   float(self.latitude),
                                   self.station_location[station]['Longitude'],
                                   self.station_location[station]['Latitude']),
                     station_availability[station][1],
                     self.station_location[station]['Latitude'],
                     self.station_location[station]['Longitude']])
            else:
                continue
        return sorted(closest_station, key=itemgetter(1))[0:5]


# Testing Below #

# converts latitude/longitude into country/city name using
# Google Maps API
# def city(latitude,longitude):
#     url = "http://maps.googleapis.com/maps/api/geocode/json?"
#     url += "latlng=%s,%s&sensor=false" % (latitude, longitude)
#     v = urllib.urlopen(url).read()
#     j = json.loads(v)
#     components = j['results'][0]['address_components']
#     country = town = None
#     for c in components:
#         if "country" in c['types']:
#             country = c['long_name']
#         if "locality" in c['types']:
#             town = c['long_name']
#     print town.encode('ascii', 'ignore'), country
#
#
# toronto= (43.7, -79.4)
# montreal= (45.5017, -73.5673)
# dc= (38.9047, -77.0164)
# minneapolis= (44.9788, -93.2650)
# boston= (42.3601, -71.0589)
# london= (51.5072, -0.1275)
# nyc= (40.7127, -74.0059)
# sf= (37.7833, -122.4167)
# chicago= (41.8369, -87.6847)
# philly = (39.9500, -75.1667)
# test = LoadStations(philly[0], philly[1])
# print test.find_closest_bike()