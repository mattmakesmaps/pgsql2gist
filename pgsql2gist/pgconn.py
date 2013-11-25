__author__ = 'matt'
__date__ = '11/24/13'

from psycopg2 import connect
from psycopg2._psycopg import Error
from psycopg2.extras import RealDictCursor


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
            raise e
        return self.db

    def __exit__(self, type, value, traceback):
        self.db.connection.close()