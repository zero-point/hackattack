from requests import get
from flask import Flask, render_template
import json
from werkzeug.contrib.cache import MemcachedCache


app = Flask(__name__)
app.debug = True

cache = MemcachedCache(['127.0.0.1:11211'], default_timeout=65)

event_colors = {
    'roadClosed': '#ff0000',
    'laneOrCarriagewayClosed': '#ff0000',
    'contraflow': '#FF8000',
    'trafficContolInOperation': '#ff69b4',
    'unknown': '#0047AB'
}

event_symbols = {
    'roadClosed': 'roadblock',
    'laneOrCarriagewayClosed': 'roadblock',
    'contraflow': 'embassy',
    'trafficContolInOperation': 'police',
    'unknown': 'fire-station'
}


@app.route('/')
def hello_world():
    return render_template('index.html')


# @app.route('/events.geojson')
# def events():
#     rv = cache.get('events-geojson')
#     if rv is None:
#         print 'memcached empty'
#         rv = get_events_response()
#         cache.set('events-geojson', rv)
#     else:
#         print 'memcached has it'
#     return json.dumps(rv)


def get_events_response():
    """
    Generator that gets the traffic response from the live feed.
    """
    resp = get('http://dashboard.glasgow.gov.uk/api/live/trafficEvents.php?type=json').json()
    try:
        situations = resp['payloadPublication']['situation']
    except Exception:
        if 'error' in resp:
            return resp['error']
        else:
            raise

    res = {'type': 'FeatureCollection', 'features': []}

    for situation in situations:
        record = situation['situationRecord']
        point = record['groupOfLocations']['locationContainedInGroup']['tpegpointLocation']['point']
        coord = point['pointCoordinates']
        d = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(coord['longitude']), float(coord['latitude'])]
            },
            'properties': {}
        }
        d['properties']['type'] = record.get('networkManagementType', 'unknown')
        d['properties']['comment'] = record['nonGeneralPublicComment']['comment']['value']
        d['properties']['marker-color'] = event_colors[d['properties']['type']]
        d['properties']['marker-symbol'] = event_symbols[d['properties']['type']]
        name = point['name']
        if isinstance(name, list):
            for name in point['name']:
                d['properties'][name['tpegDescriptorType']] = name['descriptor']['value']
        elif isinstance(name, dict):
            d['properties'][name['tpegDescriptorType']] = name['descriptor']['value']
        else:
            raise Exception('name is weird type')

        res['features'].append(d)

    return res


if __name__ == '__main__':
    app.run()
