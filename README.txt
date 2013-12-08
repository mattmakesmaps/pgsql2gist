==========
pgsql2gist
==========

Like pgsql2shp, but for gists.

Objective
=========

Create a command line utility similar to pgsql2shp, but the output of which should be
a link to an anonymous private gist. The gist link should leverage github’s
rendering of GeoJSON/TopoJSON, e.g. render a map.

See issues for additional features to be implemented.

Current Usage / Caveats
=======================

Listed below is the --help usage information.::

    POST GeoJSON or TopoJSON features from PostGIS to a Github Gist.

    Example usage: pgsql2gist --host localhost --user matt tilestache \
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

Resources
=========

Gist API: (http://developer.github.com/v3/gists/)

Thanks
======

The spiffy idea behind a db context manager comes from Migurski's awesome TileStache
map server. http://tilestache.org
