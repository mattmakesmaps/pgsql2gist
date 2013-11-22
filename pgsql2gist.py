__author__ = 'matt'
__date__ = '11/19/13'

from psycopg2.extras import RealDictCursor
from psycopg2 import connect, Error
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

        try:
            self.db = connect(**dbinfo).cursor(cursor_factory=RealDictCursor)
        except Error as e:
            print "PostGIS Connection Error: ", e.message
            print 'Terminating Script'
            raise SystemExit
        return self.db

    def __exit__(self, type, value, traceback):
        self.db.connection.close()


class GistAPI_Interface(object):
    """
    Provides functions for interacting with the github gist API.
    """
    def __init__(self, description, file, content):
        self.url = 'https://api.github.com/gists'
        self.description = description
        self.public = "false"
        self.file = file
        self.content = content
        self.response_content = None

    def http_request(self, json_data):
        """
        Given a JSON object properly formatted for the gist API
        Submit via http POST.
        """
        request = urllib2.Request(self.url, json_data)
        try:
            response = urllib2.urlopen(request)
        # Catch URL/HTTP errors, then abort script.
        except urllib2.HTTPError as e:
            print 'ERROR: Server returned HTTP Error Code:', e.code
            print 'Terminating Script'
            raise SystemExit
        except urllib2.URLError as e:
            print 'ERROR: Server Could Not Be Reached.'
            print 'REASON: ', e.reason
            print 'Terminating Script'
            raise SystemExit
        else:
            return response

    def submit(self):
        """
        Develop and submit a POST request to the github gist api.
        Populate response_content with resulting data.
        """
        # Build data payload.
        data = {
            "description": self.description,
            "public": self.public,
            "files": {
                self.file: {
                    "content": self.content
                }
            }
        }
        data_as_json = json.dumps(data)

        # TODO: Implement response validation logic. E.g. check we have a good response.
        # Submit Request
        response = self.http_request(data_as_json)
        # Populate instance attribute with JSON response from github.
        self.response_content = json.loads(response.read())
        return True

class CLI_Interface(object):
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

    def get_args_dict(self):
        """
        Given an argparse parser object, wrap in a call to vars(), returning dictionary.
        This method also calls the input validation method.
        """
        args = self.parser.parse_args()
        args_dict = vars(args)
        #if self._validate_args_dict(args_dict):
        if self._validate_args_dict(args_dict):
            return args_dict

    def _validate_args_dict(self, args_dict):
        """
        Internal method to perform validation tasks against the argparse arguments (as dict).
        Each validation function should return True or raise a SystemExit error with
        an error message. If all functions pass, return true.
        """
        validation_functions = [self._validate_file_ext]
        for func in validation_functions:
            func(args_dict)
        return True

    def _validate_file_ext(self, args_dict):
        """
        Validate that file extensions are either geojson or topojson.
        Required for data to render in mapping interface.
        """
        valid_extensions = ['.geojson','topojson']
        v_test = False
        for ext in valid_extensions:
            if args_dict['file'].endswith(ext):
                v_test = True
        if v_test:
            return True
        else:
            print 'ERROR: File extension does not end in .geojson or .topojson'
            raise SystemExit

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
    arg_parse = CLI_Interface()
    args = arg_parse.get_args_dict()

    with PostGISConnection(**args) as db:
        try:
            db.execute(args["SELECT"])
        except Error as e:
            print "PostGIS SQL Execution Error: ", e.message
            print 'Terminating Script'
            raise SystemExit

        features = [make_geojson_feature(row, args["geom_col"]) for row in db.fetchall()]

    gist_handler = GistAPI_Interface(args["description"], args["file"], make_geojson_feature_collection(features))
    #gist_handler.submit()
    print gist_handler.response_content["html_url"]
