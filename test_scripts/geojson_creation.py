__author__ = 'matt'
__date__ = '11/10/13'

"""
Copying stuff from TileStache VecTiles provider
"""

try:
    from psycopg2.extras import RealDictCursor
    from psycopg2 import connect
    import json

except ImportError, err:
    # Still possible to build the documentation without psycopg2
    def connect(*args, **kwargs):
        raise err

class Connection(object):
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
        'host': 'localhost',
        'user': 'matt',
        'database': 'tilestache',
        'port': int(5432)
    }
    # Specify what the geometry column is.
    # Will use to seperate from properties during GeoJSON construction.
    geomcol = 'geom'

    with Connection(dbinfo, geomcol) as db:
        db.execute("SELECT gid, s_hood, ST_AsGeoJSON(geom) AS geom FROM neighborhoods LIMIT 50;")
        features = [make_feature(row, geomcol) for row in db.fetchall()]

    feature_collection_str = make_feature_collection([features[0]])
    print feature_collection_str

    # Connection should be closed.
    print db