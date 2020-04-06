# This program locate the user’s location from the tweet.
# The code used in this project is referred to this program:
# Bian, J. (2015). Twitter User Geocoder [Computer software].
# Retrieved from https://github.com/bianjiang/twitter-user-geocoder

import os
import json
import sys
import re
import csv
import codecs
from math import sin, cos, sqrt, atan2, radians, isinf
from scipy.spatial import cKDTree as KDTree

import pandas as pd


def singleton(cls):
    # Singleton pattern to avoid loading class multiple times
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton
class TweetUSStateGeocoder:

    def __init__(self,
                 geocode_filename='/Users/robertbao/Documents/2019_SF/train/us_geocode.csv',
                 us_places_to_state_mapping_filename='/Users/robertbao/Documents/2019_SF/train/us.states.json'):
        coordinates, self.locations = self.extract_coordinates_and_locations(rel_path(geocode_filename))
        self.tree = KDTree(coordinates)

        self.us_places_to_state_map = self.load_us_places_to_state_mapping_file(
            rel_path(us_places_to_state_mapping_filename))

        # keep only alpha, space, period and comma
        self.keep_alpha_p = re.compile(r'[^a-zA-Z\s\.,]')

        self.geomap = {}

    def load_us_places_to_state_mapping_file(self, local_filename):
        if os.path.exists(local_filename):
            with open(local_filename, 'r') as rf:
                return json.load(rf)
        else:
            print("missing us_places_to_state_mapping file: [%s]" % (local_filename))
            sys.exit(1)

    def extract_coordinates_and_locations(self, local_filename):
        """Extract geocode data from zip
        """
        if os.path.exists(local_filename):
            # open compact CSV
            rows = csv.reader(codecs.getreader('utf-8')(open(local_filename, 'rb')))
        else:
            print("missing geocode file: [%s]" % (local_filename))
            sys.exit(1)

        # load a list of known coordinates and corresponding locations
        coordinates, locations = [], []
        for latitude, longitude, state, place in rows:
            coordinates.append((latitude, longitude))
            locations.append(dict(state=state, city=place, latitude=latitude, longitude=longitude))
        return coordinates, locations

    def query_coordinates(self, coordinates):
        """Find closest match to this list of coordinates
        """
        try:
            distances, indices = self.tree.query(coordinates, k=1)  # , distance_upper_bound=0.1
        except ValueError as e:
            print('Unable to parse coordinates:', coordinates)
            raise e
        else:
            results = []
            for distance, index in zip(distances, indices):
                if not isinf(distance):
                    result = self.locations[index]
                    result['distance'] = distance

                    results.append(result)

            return results

    def distance(self, coordinate_1, coordinate_2):

        R = 6373.0

        lat1, lon1 = coordinate_1
        lat2, lon2 = coordinate_2

        lat1 = radians(float(lat1))
        lon1 = radians(float(lon1))
        lat2 = radians(float(lat2))
        lon2 = radians(float(lon2))

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat / 2)) ** 2 + cos(lat1) * cos(lat2) * (sin(dlon / 2)) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        return distance * 0.621371

    def get_by_coordinate(self, coordinate):
        """Search for closest known location to this coordinate
        """
        tug = TweetUSStateGeocoder()
        results = tug.query_coordinates([coordinate])
        return results[0] if results else None

    def search_by_coordinates(self, coordinates):
        """Search for closest known locations to these coordinates
        """
        tug = TweetUSStateGeocoder()
        return tug.query_coordinates(coordinates)

    def get_state(self, address):

        address = address.strip()

        state = None

        if address not in self.geomap:

            p = re.findall(r'.*?([-+]?\d*\.\d+),([-+]?\d*\.\d+)', address)

            if len(p) > 0:
                coordinate = p.pop()
                nearest = self.get_by_coordinate(coordinate)

                if nearest:
                    c2 = nearest['latitude'], nearest['longitude']
                    d = self.distance(coordinate, c2)
                    if (d < 20):  # less than 100 miles
                        state = nearest['state']
                        self.geomap[address] = state

            else:

                address_ = address.replace(', ', ',')
                address_ = re.sub(self.keep_alpha_p, '', address_)
                address_ = address_.lower()

                for i in range(3):
                    # state = us_places_to_state_map[address] if address in us_places_to_state_map else None
                    if address_ in self.us_places_to_state_map['%s' % i]:
                        state = self.us_places_to_state_map['%s' % i][address_]
                        self.geomap[address] = state
                        break
                        # print('[%s]->%s'%(address, state))
        else:
            state = self.geomap[address]

        return state


def rel_path(filename):
    """Return the path of this filename relative to the current script
    """
    return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)


def location(data):
    tug = TweetUSStateGeocoder()
    data['state_name'] = data['location'].apply(lambda x: tug.get_state(str(x)))
    # df['state_name'].apply(lambda x: states.lookup(str(x)))  # Get the full state name here.
    data = data[pd.notnull(data['state_name'])]
    return data
