#! /usr/bin/env python
__author__ = 'Matthew Kenny'
__date__ = '11/19/13'
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

# Import relevant modules from the pgsql2gist package.
import time
from psycopg2 import Error
from pgsql2gist import GistAPIHandler, PostGISConnection, CLIInterface, GeoJSONConstructor


def main():
    try:
        # Setup CLI; Parse User Input
        arg_parse = CLIInterface()
        args = arg_parse.get_args_dict()

        # Open DB Connection; Execute Query
        with PostGISConnection(**args) as db:
            try:
                db.execute(args["SELECT"])
            except Error as e:
                print "PostGIS SQL Execution Error: ", e.message
                raise e
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
    except Exception as e:
        if e.message:
            print "ERROR: ", e.message
        print 'Terminating Script'
        raise SystemExit


if __name__ == '__main__':
    main()