#! /usr/bin/env python
__author__ = 'Matthew Kenny'
__date__ = '11/19/13'
"""
POST GeoJSON or TopoJSON features from PostGIS to a Github Gist.

Example usage: pgsql2gist --host localhost --user matt tilestache \
               "SELECT name, ST_AsGeoJSON(geom) AS geometry FROM neighborhoods LIMIT 5;"

usage: pgsql2gist [-f FILE] [-d DESCRIPTION] [-h HOST] [-p PORT] [-P PASSWORD]
                  [-u USER] [-g GEOM_COL] [-t TOPOLOGY_LAYER] [-v] [-?]
                  database SELECT

positional arguments:
  database              PostGIS database name.
  SELECT                SELECT Statement. NOTE: Geometry must be WGS84;
                        wrapped in ST_AsGeoJSON() or AsTopoJSON().

optional arguments:
  -f FILE, --file FILE  Filename. NOTE: Must end in 'geojson' or 'topojson'
                        extension. (default: upload.geojson)
  -d DESCRIPTION, --description DESCRIPTION
                        Description of upload (default: File uploaded using
                        pgsql2gist.)
  -h HOST, --host HOST  PostGIS database hostname. (default: None)
  -p PORT, --port PORT  PostGIS database port. (default: 5432)
  -P PASSWORD, --password PASSWORD
                        PostGIS user password. (default: None)
  -u USER, --user USER  PostGIS database user. (default: postgres)
  -g GEOM_COL, --geom-col GEOM_COL
                        Geometry column name as defined in SELECT statement.
                        (default: geometry)
  -t TOPOLOGY_LAYER, --topology-layer TOPOLOGY_LAYER
                        For TopoJSON Queries; Name of Topology Layer (default:
                        None)
  -v, --verbose         Verbose output. (default: False)
  -?, --help
"""

# Import relevant modules from the pgsql2gist package.
import time
from psycopg2 import Error
import pgsql2gist


def main():
    try:
        # Setup CLI; Parse User Input
        arg_parse = pgsql2gist.CLIInterface()
        args = arg_parse.get_args_dict()

        # Open DB Connection; Execute Query
        with pgsql2gist.PostGISConnection(**args) as db:
            try:
                db.execute(args["SELECT"])
            except Error as e:
                print "PostGIS SQL Execution Error: ", e.message
                raise e
                # Get results
            query_results = db.fetchall()

        # Mapping of file extensions to constructor classes
        constructor_lookup = {'geojson': pgsql2gist.GeoJSONConstructor,
                              'topojson': pgsql2gist.TopoJSONConstructor}
        # Reference constructor class
        constructor = constructor_lookup[args["format"]]
        # Instanciate constructor class
        selected_constructor = constructor(query_results, args["geom_col"], **args)
        if args["verbose"]:
            selected_constructor = pgsql2gist.VerboseConstructorDecorator(selected_constructor)
        features = selected_constructor.encode()

        # Setup and create request to Gist API
        gist_handler = pgsql2gist.GistAPIHandler(args["file"], args["description"], features)
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
    except Exception as e:
        if e.message:
            print "ERROR: ", e.message
        print 'Terminating Script'
        raise SystemExit


if __name__ == '__main__':
    main()