__author__ = 'matt'
__date__ = '11/22/13'
import sys, unittest
from nose.tools import with_setup, raises
from pgsql2gist import CLI_Interface

class TestKeyValues(object):
    def setup(self):
        self.args = ['/Users/matt/Projects/pgsql2gist/pgsql2gist.py',
                '-h', 'localhost',
                '-f', 'test.geojson',
                '-d', 'sample description',
                '-p', '5432',
                '-g', 'geometry',
                '--user', 'matt',
                'tilestache',
                'SELECT hoods_, ST_AsGeoJSON(geom) AS geometry FROM neighborhoods LIMIT 5;']
        sys.argv = self.args
        self.arg_parser = CLI_Interface()

    def test_keys(self):
        """
        Check that argparse is returning all keys as expected.
        """
        expected_keys = ['description', 'database', 'geom_col', 'host', 'user', 'password', 'file', 'port', 'SELECT']
        args_dict = self.arg_parser.get_args_dict()
        for key in expected_keys:
            assert key in args_dict

    def test_values(self):
        """
        Check that argparse is returning both user provided values
        as well as properly setting default values.
        """
        expected_args_dict =  {'description': 'sample description',
                               'database': 'tilestache',
                               'geom_col': 'geometry',
                               'host': 'localhost',
                               'user': 'matt',
                               'file': 'test.geojson',
                               'password': None,
                               'port': 5432,
                               'SELECT': 'SELECT hoods_, ST_AsGeoJSON(geom) AS geometry FROM neighborhoods LIMIT 5;'}

        args_dict = self.arg_parser.get_args_dict()
        for key, value in expected_args_dict.iteritems():
            assert args_dict[key] == value


class TestBadInput(object):
    def setup(self):
        self.args = ['/Users/matt/Projects/pgsql2gist/pgsql2gist.py',
                     '-f', 'test.badfileext',
                     'tilestache',
                     'SELECT hoods_, ST_AsGeoJSON(geom) AS geometry FROM neighborhoods LIMIT 5;']
        sys.argv = self.args
        self.arg_parser = CLI_Interface()

    @raises(ValueError)
    def test_file_extension_validation(self):
        """
        Check that an error message is populated
        """
        args_dict = self.arg_parser.get_args_dict()

