__author__ = 'matt'
__date__ = '11/24/13'

import argparse


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
        # Internal Attribute will be used to populate dictionary in get_args_dict() method.
        self._format = None
        # Build Parser
        self.setup()

    def setup(self):
        # Add positional arguments first
        self.parser.add_argument("database", help="PostGIS database name.")
        self.parser.add_argument("SELECT",
                                 help="SELECT Statement. NOTE: Geometry must be WGS84; wrapped in ST_AsGeoJSON() or AsTopoJSON().")
        # Add optional arguments.
        self.parser.add_argument("-f", "--file",
                                 help="Filename. NOTE: Must end in 'geojson' or 'topojson' extension.",
                                 default="upload.geojson")
        self.parser.add_argument("-d", "--description",
                                 help="Description of upload",
                                 default="File uploaded using pgsql2gist.")
        self.parser.add_argument("-h", "--host", help="PostGIS database hostname.")
        self.parser.add_argument("-p", "--port", help="PostGIS database port.", type=int, default=5432)
        self.parser.add_argument("-P", "--password", help="PostGIS user password.")
        self.parser.add_argument("-u", "--user", help="PostGIS database user.", default="postgres")
        self.parser.add_argument("-g", "--geom-col",
                                 help="Geometry column name as defined in SELECT statement.",
                                 default="geometry")
        self.parser.add_argument("-t", "--topology-layer", help="For TopoJSON Queries; Name of Topology Layer")
        self.parser.add_argument("-v", "--verbose", help="Verbose output.", action="store_true")
        # Add custom help flag
        self.parser.add_argument("-?", "--help", action="help")

    def get_args_dict(self):
        """
        Given an argparse parser object, wrap in a call to vars(), returning a dictionary of attributes.
        This method also calls the input validation method.
        """
        args = self.parser.parse_args()
        args_dict = vars(args)
        if self._validate_args_dict(args_dict):
            # Expose internal _format attribute along with dictionary of arg parse attributes.
            args_dict["format"] = self._format
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
            func(args_dict)
        return True

    def _validate_file_ext(self, args_dict):
        """
        Validate that file extensions are either geojson or topojson.
        Required for data to render in mapping interface.

        Set the class' _format attribute.
        """
        valid_extensions = ['geojson', 'topojson']
        ext_is_valid = False
        for ext in valid_extensions:
            if args_dict['file'].endswith(ext):
                self._format = ext
                ext_is_valid = True
        if ext_is_valid:
            return True
        else:
            raise ValueError("File does not end in '.geojson' or '.topojson'. NOTE: Gist API is case-sensitive.")

    def _validate_topojson_geojson_call(self, args_dict):
        """
        Validate that a user has invoked a call to ST_AsGeoJSON() or ST_AsTopoJSON()
        in their SELECT statement.
        """
        valid_calls = ['st_asgeojson', 'astopojson']
        call_is_valid = False
        for call in valid_calls:
            if call.lower() in args_dict['SELECT'].lower():
                call_is_valid = True
        if call_is_valid:
            return True
        else:
            raise ValueError('SELECT statement does not contain call to ST_AsGeoJSON() or AsTopoJSON()')
