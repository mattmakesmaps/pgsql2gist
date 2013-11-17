__author__ = 'matt'
__date__ = '11/17/13'

from psycopg2.extras import RealDictCursor
from psycopg2 import connect
import json
import urllib2
import argparse

class PostGISConnection(object):
    ''' Context manager for Postgres connections.

        See http://www.python.org/dev/peps/pep-0343/
        and http://effbot.org/zone/python-with-statement.htm
        Ripped from TileStache.
    '''
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __enter__(self):
        """
        Extract relevant connection details from command line arguments.
        Create database connection.
        """
        dbconnkeys = ['host','port','user','password','database']
        dbinfo = {}
        for key, value in self.kwargs.iteritems():
            if key in dbconnkeys and value:
                dbinfo[key] = value

        self.db = connect(**dbinfo).cursor(cursor_factory=RealDictCursor)
        return self.db

    def __exit__(self, type, value, traceback):
        self.db.connection.close()


class interface(object):
    """
    Basic command line interface using argparse.
    Based on pgsql2shp.
    """
    def __init__(self):
        """
        Create parser and execute setup method.
        """
        self.parser = argparse.ArgumentParser(add_help=False,
                                              formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        # Build Parser
        self.setup()

    def setup(self):
        # Add positional arguments first
        self.parser.add_argument("database", help="PostGIS database name.")
        self.parser.add_argument("SELECT",
                            help="SELECT Statement. NOTE: Geometry must be GeoJSON stored in WGS84.")
        # Add optional arguments.
        self.parser.add_argument("-f", "--file",
                            help="Filename. NOTE: Must end in 'geosjon' or 'topojson' extension.",
                            default="upload.geojson")
        self.parser.add_argument("-d", "--description",
                                 help="Description of upload",
                                 default="File uploaded using pgsql2gist.")
        self.parser.add_argument("-h", "--host", help="PostGIS database hostname.", default="localhost")
        self.parser.add_argument("-p", "--port", help="PostGIS database port.", type=int, default=5432)
        self.parser.add_argument("-P", "--password", help="PostGIS user password.")
        self.parser.add_argument("-u", "--user", help="PostGIS database user.", default="postgres")
        self.parser.add_argument("-g", "--geom-col", help="Geometry Column.", default="geometry")
        # Add custom help flag
        self.parser.add_argument("-?", "--help", action="help")

def make_geojson_feature(row, geom_column):
    """
    Given a database row via Psycopg's RealDictCursor
    return back a completed GeoJSON feature containing
    properties and geometries.
    """
    geometry = json.loads(row.pop(geom_column))
    feature = dict(type='Feature', geometry=geometry, properties=row)
    encoded = json.dumps(feature)
    return encoded

def make_geojson_feature_collection(features_str):
    """
    Given a list containing GeoJSON features, return as a
    GeoJSON Feature Collection.
    """
    features_json = [json.loads(feature) for feature in features_str]
    feature_collection = dict(type='FeatureCollection', features=features_json)
    encoded_feature_collection = json.dumps(feature_collection)
    return encoded_feature_collection

if __name__ == '__main__':
    new_interface = interface().parser
    # vars() will convert the argparse namespace object to a python dict
    args = vars(new_interface.parse_args())

    with PostGISConnection(**args) as db:
        db.execute(args["SELECT"])
        features = [make_geojson_feature(row, args["geom_col"]) for row in db.fetchall()]

    # values will be converted to json object, for POST request to github API.
    values = {
        "description": args["description"],
        "public": "false",
        "files": {
            args["file"]: {
                "content": make_geojson_feature_collection(features)
            }
        }
    }

    # Build the POST request, with url and gist_json data object.
    url = 'https://api.github.com/gists'
    gist_json = json.dumps(values)
    req = urllib2.Request(url, gist_json)

    # Read the response from github; print html_url to user.
    response = json.loads(urllib2.urlopen(req).read())
    response_gist_url = response["html_url"]
    print response_gist_url
