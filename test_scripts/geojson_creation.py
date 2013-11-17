__author__ = 'matt'
__date__ = '11/10/13'

"""
Copying stuff from TileStache VecTiles provider
"""

try:
    from psycopg2.extras import RealDictCursor
    from psycopg2 import connect
    import json
    import urllib2

except ImportError, err:
    # Still possible to build the documentation without psycopg2
    def connect(*args, **kwargs):
        raise err

class PostGISConnection(object):
    ''' Context manager for Postgres connections.

        See http://www.python.org/dev/peps/pep-0343/
        and http://effbot.org/zone/python-with-statement.htm
    '''
    def __init__(self, dbinfo, geomcol):
        self.dbinfo = dbinfo
        self.geomcol = geomcol

    def __enter__(self):
        self.db = connect(**self.dbinfo).cursor(cursor_factory=RealDictCursor)
        return self.db

    def __exit__(self, type, value, traceback):
        self.db.connection.close()

def make_feature(row, geom_column):
    """
    Given a database row via Psycopg's RealDictCursor
    return back a completed GeoJSON feature containing
    properties and geometries.
    """
    geometry = json.loads(row.pop(geom_column))
    feature = dict(type='Feature', geometry=geometry, properties=row)
    encoded = json.dumps(feature)
    return encoded

def make_feature_collection(features_str):
    """
    Given a list containing GeoJSON features, return as a
    GeoJSON Feature Collection.
    """
    features_json = [json.loads(feature) for feature in features_str]
    feature_collection = dict(type='FeatureCollection', features=features_json)
    encoded_feature_collection = json.dumps(feature_collection)
    return encoded_feature_collection

if __name__ == '__main__':
    # Stub for connection parameters.
    dbinfo = {
        'host': 'pgsqlgis-repos',
        'user': 'postgres',
        'password': 'postgres',
        'database': 'osm_planet2',
        'port': int(5432)
    }
    # Specify what the geometry column is.
    # Will use to seperate from properties during GeoJSON construction.
    geomcol = 'geom'

    with PostGISConnection(dbinfo, geomcol) as db:
        #db.execute("SELECT gid, s_hood, ST_AsGeoJSON(geom) AS geom FROM neighborhoods LIMIT 50;")
        #db.execute("SELECT name, type, osm_id, ST_AsGeoJSON(ST_Transform(ST_PointOnSurface(geometry),4326)) AS geom FROM osm_new_waterareas WHERE name = 'Lake Chelan';")
        #db.execute("SELECT name, ST_AsGeoJSON(ST_Transform(ST_Buffer(ST_Collect(geometry), 0), 4326)) AS geometry FROM osm_new_waterareas WHERE name = 'Lake Chelan' GROUP BY name")
        db.execute("SELECT name, ST_Area(Geography(ST_Transform((ST_DUMP(ST_BUFFER(ST_Collect(geometry), 0))).geom,4326))) AS area, ST_AsGeoJSON(ST_Transform(ST_PointOnSurface((ST_DUMP(ST_BUFFER(ST_Collect(geometry), 0))).geom), 4326)) AS geom FROM osm_new_waterareas WHERE name = 'Lake Chelan' GROUP BY name;")
        features = [make_feature(row, geomcol) for row in db.fetchall()]

    feature_collection_str = make_feature_collection(features)

    values = {
        "description": "Features contained within an imposm db's osm_new_waterareas table, named Lake Chelan",
        "public": "false",
        "files": {
            "chelan.geojson": {
                "content": feature_collection_str
            }
        }
    }

    url = 'https://api.github.com/gists'
    gist_json = json.dumps(values)
    req = urllib2.Request(url, gist_json)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page
