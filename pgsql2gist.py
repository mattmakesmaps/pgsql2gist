__author__ = 'matt'
__date__ = '11/19/13'
__version__ = '0.1'
"""
POST GeoJSON or TopoJSON features from PostGIS to a Github Gist.

Example usage: python pgsql2gist.py --host localhost --user matt tilestache \
               "SELECT name, ST_AsGeoJSON(geom) AS geometry FROM neighborhoods LIMIT 5;"

Current SELECT Statement Requirements:
 - Geometry must be in EPSG:4326 WGS84 coordinate system
 - Geometry must be wrapped in ST_AsGeoJSON(), ST_AsTopoJSON()

usage: pgsql2gist.py [-f FILE] [-d DESCRIPTION] [-h HOST] [-p PORT]
                     [-P PASSWORD] [-u USER] [-g GEOM_COL] [-?]
                     database SELECT

positional arguments:
  database              PostGIS database name.
  SELECT                SELECT Statement. NOTE: Geometry must be GeoJSON
                        stored in WGS84.

optional arguments:
  -f FILE, --file FILE  Filename. NOTE: Must end in 'geosjon' or 'topojson'
                        extension. (default: upload.geojson)
  -d DESCRIPTION, --description DESCRIPTION
                        Description of upload (default: File uploaded using
                        pgsql2gist.)
  -h HOST, --host HOST  PostGIS database hostname. (default: localhost)
  -p PORT, --port PORT  PostGIS database port. (default: 5432)
  -P PASSWORD, --password PASSWORD
                        PostGIS user password. (default: None)
  -u USER, --user USER  PostGIS database user. (default: postgres)
  -g GEOM_COL, --geom-col GEOM_COL
                        Geometry Column. (default: geometry)
  -?, --help
"""

from psycopg2.extras import RealDictCursor
from psycopg2 import connect, Error
import argparse
import json
import time
import urllib2
import sys

class PostGISConnection(object):
    """
    Ripped from TileStache.
    Context manager for Postgres connections.
    See http://www.python.org/dev/peps/pep-0343/
    and http://effbot.org/zone/python-with-statement.htm
    """
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

class GeoJSONConstructor(object):
    """
    Given the following inputs, generate a GeoJSON feature collection.

    Required Parameters:
    records (LIST) - Each element is a dictionary representing
    columns and values for a single geojson feature.
    geom_col (STRING) - Indicates which dict key represents the geometry column.

    TODO: Include validation checks. Add Exception Handling.
    """
    def __init__(self, records, geom_col='geometry'):
        self.records = records
        self.geom_col = geom_col

    def make_feature(self, record, geom_column):
        """
        Given a database row via Psycopg's RealDictCursor
        return back a completed GeoJSON feature containing
        properties and geometries.
        """
        geometry = json.loads(record.pop(geom_column))
        feature = dict(type='Feature', geometry=geometry, properties=record)
        encoded_feature = json.dumps(feature)
        return encoded_feature

    def make_feature_collection(self, features_list):
        """
        Given a list containing GeoJSON features, return as a
        GeoJSON Feature Collection.
        """
        features_json = [json.loads(feature) for feature in features_list]
        feature_collection = dict(type='FeatureCollection', features=features_json)
        encoded_feature_collection = json.dumps(feature_collection)
        return encoded_feature_collection

    def encode(self):
        """
        Return back a string representing a GeoJSON feature collection.
        """
        features = [self.make_feature(row, self.geom_col) for row in self.records]
        feature_collection = self.make_feature_collection(features)
        return feature_collection

class GistAPIHandler(object):
    """
    Provides methods for interacting with the Github Gist API.

    Required parameters:
    file (STRING) - File name. Required to be in extension '.geojson' OR '.topojson'
    description (STRING) - A brief description of the gist contents
    content (STRING) - Implied to be Valid GeoJSON or TopoJSON, but not required.
    """
    def __init__(self, file, description, content, public="false"):
        self.content = content
        self.description = description
        self.file = file
        self.public = public
        self.response_content = None
        self.response_headers = None
        self.url = 'https://api.github.com/gists'

    def _build_request(self):
        """
        Given instance attributes, generate a properly formatted
        JSON request for the gist API.
        """
        data = {
            "description": self.description,
            "public": self.public,
            "files": {
                self.file: {
                    "content": self.content
                }
            }
        }
        return json.dumps(data)

    def _submit_request(self, json_data):
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

    def create(self):
        """
        Execute a series of internal class methods responsible for processing
        the request/response interaction between the client and the github API.

        This method updates the class instance's response_content attribute, which
        contains the gist url.
        """

        data_as_json = self._build_request()
        response = self._submit_request(data_as_json)
        self.response_headers = response.headers.dict

        # Populate instance attribute with JSON response from github.
        if response.code == 201:
            self.response_content = json.loads(response.read())
            return True
        else:
            print "Gist creation failed. Server returned HTTP code: ", response.code
            raise SystemExit


class CLIInterface(object):
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
        if self._validate_args_dict(args_dict):
            return args_dict

    def _validate_args_dict(self, args_dict):
        """
        Internal method to perform validation tasks against the argparse arguments (as dict).
        Each validation function should return True or raise an error with an error message.
        Each raised error will be caught by a generic Error exception, and will raise a
        SystemExit error, terminating the script.
        """
        validation_functions = [self._validate_file_ext, self._validate_topojson_geojson_call]
        for func in validation_functions:
            try:
                func(args_dict)
            except Exception, e:
                print "Terminating Script"
                raise SystemExit
        return True

    def _validate_file_ext(self, args_dict):
        """
        Validate that file extensions are either geojson or topojson.
        Required for data to render in mapping interface.
        """
        valid_extensions = ['.geojson','topojson']
        ext_is_valid = False
        for ext in valid_extensions:
            if args_dict['file'].endswith(ext):
                ext_is_valid  = True
        if ext_is_valid:
            return True
        else:
            print 'ERROR: File extension does not end in .geojson or .topojson'
            raise ValueError

    def _validate_topojson_geojson_call(self, args_dict):
        """
        Validate that a user has invoked a call to ST_AsGeoJSON() or ST_AsTopoJSON()
        in their SELECT statement.
        """
        valid_calls = ['st_asgeojson', 'st_astopojson']
        call_is_valid = False
        for call in valid_calls:
            if call.lower() in args_dict['SELECT'].lower():
                call_is_valid = True
        if call_is_valid:
            return True
        else:
            print 'ERROR: SELECT statement does not contain call to ST_AsGeoJSON() or ST_AsTopoJSON()'
            raise ValueError


if __name__ == '__main__':
    # Setup CLI; Parse User Input
    arg_parse = CLIInterface()
    args = arg_parse.get_args_dict()

    # Open DB Connection; Execute Query
    with PostGISConnection(**args) as db:
        try:
            db.execute(args["SELECT"])
        except Error as e:
            print "PostGIS SQL Execution Error: ", e.message
            print 'Terminating Script'
            raise SystemExit
        # Get results
        query_results = db.fetchall()

    # Create GeoJSON Feature Collection
    features = GeoJSONConstructor(query_results, args["geom_col"]).encode()
    # Setup and create request to Gist API
    gist_handler = GistAPIHandler(args["file"], args["description"], features)
    gist_handler.create()

    # Return rate limit and gist url to user.
    if "x-ratelimit-limit" in gist_handler.response_headers:
        req_remaining = gist_handler.response_headers["x-ratelimit-remaining"]
        req_limit = gist_handler.response_headers["x-ratelimit-limit"]
        reset_time_epoch = gist_handler.response_headers["x-ratelimit-reset"]
        reset_time_human = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(reset_time_epoch)))
        print "%s requests remaining of %s total. Reset in: %s" % (req_remaining, req_limit, reset_time_human)
    if "html_url" in gist_handler.response_content:
        print "Gist URL: ", gist_handler.response_content["html_url"]
