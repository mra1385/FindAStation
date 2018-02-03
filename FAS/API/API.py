# import modules
from math import radians, cos, sin, asin, sqrt
import urllib.request
import urllib
import json
import xml.etree.ElementTree as ET
from operator import itemgetter
import requests


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
        v = urllib.request.urlopen(url).read()
        j = json.loads(v)
        try:
            components = j['results'][0]['address_components']
        except:
            components = []
        country = town = None
        for c in components:
            if "country" in c['types']:
                country = c['long_name']
            if "locality" in c['types']:
                town = c['long_name']

        # query for station locations and status if country/city is
        # United States/Washington area
        if country == 'United States' and town in ['Washington','Arlington','Alexandria']:
            xml_path = 'https://www.capitalbikeshare.com/data/stations/' \
                       'bikeStations.xml'
            tree = ET.parse(urllib.request.urlopen(xml_path))
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

        # query for station locations and status if country/city is
        # United States/New York
        elif country == 'United States' and town in 'New York':
            station_location = dict()
            station_status = dict()
            url = 'https://www.citibikenyc.com/stations/json'
            v = urllib.request.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = \
                    {'Latitude': i['latitude'],
                     'Longitude': i['longitude']}
                station_status[i['stationName']] = \
                    [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status

        # query for station locations and status if country/city is
        # United States/Chicago
        elif country == 'United States' and town in 'Chicago':
            station_location = dict()
            station_status = dict()
            url = 'https://www.divvybikes.com/stations/json'
            v = urllib.request.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = \
                    {'Latitude': i['latitude'], 'Longitude': i['longitude']}
                station_status[i['stationName']] = \
                    [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status

        # search for station locations and status if
        # country/city is Canada/Toronto
        elif country == 'Canada' and town in 'Toronto':
            station_location = dict()
            station_status = dict()
            url = 'http://www.bikesharetoronto.com/stations/json'
            v = urllib.request.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = \
                    {'Latitude': i['latitude'], 'Longitude': i['longitude']}
                station_status[i['stationName']] = \
                    [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status

        # query for station locations and status if
        # country/city is United States/San Francisco Bay area
        elif country == 'United States' \
                and town in ['San Francisco','Palo Alto', 'Redwood City', 'Mountain View', 'San Jose']:
            station_location = dict()
            station_status = dict()
            url = 'http://www.bayareabikeshare.com/stations/json'
            v = urllib.request.urlopen(url).read()
            j = json.loads(v)
            for i in j['stationBeanList']:
                station_location[i['stationName']] = \
                    {'Latitude': i['latitude'], 'Longitude': i['longitude']}
                station_status[i['stationName']] = \
                    [i['availableBikes'], i['availableDocks']]
            self.station_location = station_location
            self.station_status = station_status

        elif country == 'United States' and town in 'Philadelphia':
            station_location = dict()
            station_status = dict()
            url = 'https://www.rideindego.com/stations/json/'

            class MyOpener(urllib.request.FancyURLopener):
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

        # query for station locations and status if
        # country/city is Canada/Montreal
        elif country == 'Canada' and town in 'Montréal':
            xml_path = 'http://montreal.bixi.com/data/bikeStations.xml'
            tree = ET.parse(urllib.request.urlopen(xml_path))
            root = tree.getroot()
            station_location = dict()
            station_status = dict()
            for child in root:
                station_location[child[1].text] = \
                    {'Latitude': float(child[4].text),
                     'Longitude': float(child[4].text)}
                station_status[child[1].text] = \
                    [child[12].text, child[13].text]
            self.station_location = station_location
            self.station_status = station_status

        # query for station locations and status if
        # country/city is United Kingdom/London
        elif country == 'United Kingdom' and town in 'London':
            xml_path = 'https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml'
            root = ET.fromstring(requests.get(xml_path).content)
            station_location = dict()
            station_status = dict()
            for child in root:
                station_location[child[1].text] = \
                    {'Latitude': float(child[3].text),
                     'Longitude': float(child[4].text)}
                station_status[child[1].text] = [child[10].text, child[11].text]
            self.station_location = station_location
            self.station_status = station_status

        # query for station locations and status if
        # country/city is United States/Boston
        elif country == 'United States' and town in 'Boston':
            xml_path = 'http://www.thehubway.com/data/stations/bikeStations.xml'
            tree = ET.parse(urllib.request.urlopen(xml_path))
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

        # query for station locations and status if
        # country/city is United States/Minneapolis
        elif country == 'United States' and town in 'Minneapolis':
            xml_path = 'https://secure.niceridemn.org/data2/bikeStations.xml'
            tree = ET.parse(urllib.request.urlopen(xml_path))
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
        Finds closest station with available bike based on passed coordinates
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