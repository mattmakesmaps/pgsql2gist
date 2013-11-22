__author__ = 'matt'
__date__ = '11/10/13'

"""
Copying stuff from TileStache VecTiles provider
"""

try:
    from psycopg2.extras import RealDictCursor
    from psycopg2 import connect

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

        """
        Lookup example of dynamic geojson creation
        """

        for row in db.fetchall():
            print row

    # Connection should be closed.
    print db