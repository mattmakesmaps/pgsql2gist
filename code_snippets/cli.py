__author__ = 'matt'
__date__ = '11/10/13'

"""
Copying stuff from TileStache VecTiles provider

manpage for pgsql2shp

USAGE: pgsql2shp [<options>] <database> [<schema>.]<table>
       pgsql2shp [<options>] <database> <query>

OPTIONS:
  -f <filename>  Use this option to specify the name of the file to create.
  -h <host>  Allows you to specify connection to a database on a
     machine other than the default.
  -p <port>  Allows you to specify a database port other than the default.
  -P <password>  Connect to the database with the specified password.
  -u <user>  Connect to the database as the specified user.
  -g <geometry_column> Specify the geometry column to be exported.
  -b Use a binary cursor.
  -r Raw mode. Do not assume table has been created by the loader. This would
     not unescape attribute names and will not skip the 'gid' attribute.
  -k Keep PostgreSQL identifiers case.
  -m <filename>  Specify a file containing a set of mappings of (long) column
     names to 10 character DBF column names. The content of the file is one or
     more lines of two names separated by white space and no trailing or
     leading space. For example:
         COLUMNNAME DBFFIELD1
         AVERYLONGCOLUMNNAME DBFFIELD2
  -? Display this help screen.

"""

import argparse

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
        self.parser.add_argument("SELECT",
                            help="SELECT Statement. NOTE: Geometry must be GeoJSON stored in WGS84.")
        # Add optional arguments.
        self.parser.add_argument("-f", "--file",
                            help="Filename. NOTE: Must end in 'geosjon' or 'topojson' extension.",
                            default="upload.geojson")
        self.parser.add_argument("-h", "--host", help="PostGIS database hostname.", default="localhost")
        self.parser.add_argument("-p", "--port", help="PostGIS database port.", type=int, default=5432)
        self.parser.add_argument("-P", "--password", help="PostGIS user password.")
        self.parser.add_argument("-u", "--user", help="PostGIS database user.", default="postgres")
        self.parser.add_argument("-g", "--geom-col", help="Geometry Column.", default="geometry")
        # Add custom help flag
        self.parser.add_argument("-?", "--help", action="help")

if __name__ == '__main__':
    new_interface = interface().parser
    args = new_interface.parse_args()
    print args.file

