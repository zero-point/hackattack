import csv
import json
from collections import defaultdict
from conversion import OSGB36toWGS84 as convert

GRAPH = defaultdict(list)
ROAD_FEATURES = defaultdict(list)

class Feature(object):
    def __init__(self, road, category, easting, northing, 
                       start_junction, end_junction, 
                       pedal_cycles, motor_cycles, cars, buses, light_goods, hgv, all_motor):
        self.road = road
        self.category = category

        self.easting = easting
        self.northing = northing

        self.start_junction = start_junction
        self.end_junction = end_junction

        self.pedal_cycles = pedal_cycles
        self.motor_cycles = motor_cycles
        self.cars = cars
        self.buses = buses
        self.light_goods = light_goods
        self.hgv = hgv
        self.all_motor = all_motor

    def __str__(self):
        return (self.road, self.start_junction, self.end_junction)

output = {"type": "FeatureCollection"}
features = []

with open('data/traffic_data.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        # Don't add an edge for every year
        if row[0] == '2000':
            GRAPH[row[8]].append(row[9])
            GRAPH[row[9]].append(row[8])

            coordinates = convert(int(row[6]), int(row[7]))
            coordinates[0] -= 0.0013
            features.append({"geometry": {"type": "Point",
                                          "coordinates": coordinates
                                          },
                             "type": "Feature",
                             "properties": {"DESCRIPTOR": row[4]}
                            })

        # Road names as keys to dictionaries containing features for all segments
        ROAD_FEATURES[row[4]].append(Feature(row[4], row[5], row[6], row[7], row[8], row[9],
                                             row[12], row[13], row[14], row[15], row[16], row[23], row[24]))

output["features"] = features
# print json.dumps(output)
with open('static/traffic.geojson', 'w') as outfile:
    json.dump(output, outfile)