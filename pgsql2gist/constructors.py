__author__ = 'matt'
__date__ = '11/24/13'
"""
Constructors are classes that are designed to accept geometry/attribute data as input,
and convert to a serialized string, for POST'ing to Github using the Gist API.

Constructor classes rely on a duck typed interface. A stub class looks like the following:

class TopoJSONConstructor(object):
    def __init__(self, records, geometry_col='geometry', **kwargs):
        self.records = records
        self.geometry_col = geometry_col
        self.kwargs = kwargs

    def encode(self):
        raise NotImplementedError("TopoJSON Support Not Implemented In This Version.")

As seen above the required attributes for a constructor class are:
records - A list of dictionaries. Each dictionary represents a record to be serialized.
          Dictionary key/values represent properties (tabular+geometry) for the record.
          This attribute can be populated from any data source, but within the context
          of this application, is the result of a call to psycopg2's fetchall() method.
geometry_col - A string representing the key for the a record dictionary (contained in the
           records list) that holds geometry information. Defaults to 'geometry'
kwargs - Any additionalal keyword arguments. For the topojson constructor, this represents CLI arguments output from
         argparse.

An 'encode()' method is also required. This method should return a string representing the
serialized geometry with attributes.

Bad Example: https://gist.github.com/anonymous/2f761f3d36c995abb3fa
"""

from . import PostGISConnection
from psycopg2 import Error
import collections
import simplejson as json


class OutOfBoundsError(Exception):
    pass


class VerboseConstructorDecorator(object):
    """
    Decorator class to provide verbose output for any class implementing
    the constructor interface (e.g. an encode() method).
    """

    def __init__(self, constructor):
        self.constructor = constructor

    def encode(self):
        """
        Return back a string representing a GeoJSON feature collection.
        """
        print 'Begin Encoding Process'
        # Execute encode method, creating serialized string
        encoded_str = self.constructor.encode()
        # Return verbose output to user
        for row in self.constructor.records:
            print row
        print 'Total Records Processed: %s' % len(self.constructor.records)
        # Return serialized string to caller
        return encoded_str


class GeoJSONConstructor(object):
    """
    Given the following inputs, generate a GeoJSON feature collection.

    Required Parameters:
    records (LIST) - Each element is a dictionary representing
    columns and values for a single geojson feature.
    geom_col (STRING) - Indicates which dict key represents the geometry column.
    """

    def __init__(self, records, geometry_col='geometry', **kwargs):
        self.records = records
        self.geometry_col = geometry_col
        self.kwargs = kwargs

    def _get_coordinates(self, coordinates):
        """
        Given a MULTI geometry, return a list of individual coordinate pairs.

        A "coordinate" is considered to be a two-element list not containing
        lists itself (rather then explicitly checking for floats or ints.
        """
        if isinstance(coordinates, collections.Iterable) and not isinstance(coordinates[0], collections.Iterable):
            yield coordinates
        for coordinate in coordinates:
            # If we're a list and our first member is a list, continue to dive deeper
            if isinstance(coordinate, collections.Iterable):
                if isinstance(coordinate[0], collections.Iterable):
                    for sub in self._get_coordinates(coordinate):
                        yield sub
                # else, yield the coordinate
                else:
                    yield coordinate

    def _is_feat_wgs84(self, geometry):
        """
        Given a geometry check that is within a valid WGS84 lat lon bbox.
        """
        coordinates = self._get_coordinates(geometry['coordinates'])
        for pair in coordinates:
            self._is_coord_wgs84(pair)
            # Didn't get an exception, return True.
        return True

    @staticmethod
    def _is_coord_wgs84(coordinate):
        if 180 < coordinate[0] or coordinate[0] < -180:
            raise OutOfBoundsError("Coordinate %f, %f is not valid WGS84" % (coordinate[0], coordinate[1]))
        if 90 < coordinate[1] or coordinate[1] < -90:
            raise OutOfBoundsError("Coordinate %f, %f is not valid WGS84" % (coordinate[0], coordinate[1]))
        return True

    def _make_feature(self, record, geom_column):
        """
        Given a database row via Psycopg's RealDictCursor
        return back a completed GeoJSON feature containing
        properties and geometries.
        """
        geometry = json.loads(record.pop(geom_column))
        if self._is_feat_wgs84(geometry):
            feature = dict(type='Feature', geometry=geometry, properties=record)
            encoded_feature = json.dumps(feature)
            return encoded_feature

    @staticmethod
    def _make_feature_collection(features_list):
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
        features = [self._make_feature(row, self.geometry_col) for row in self.records]
        feature_collection = self._make_feature_collection(features)
        return feature_collection


class TopoJSONConstructor(object):
    """
    Given the following inputs, generate a TopoJSON GeometryCollection object
    comprised of individual features.

    Required Parameters:
    records (LIST) - Each element is a dictionary representing
    columns and values for a single TopoJSON feature.
    geometry_col (STRING) - Indicates which dict key represents the geometry column.
    **kwargs (DICT) - CLI args parsed via argparse. Used to scrape the filename.

    NOTE: This class currently relies on querying PostGIS to retrieve edge (arc)
    geometries. As such, it is non-portable.
    """

    def __init__(self, records, geometry_col='geometry', **kwargs):
        self.records = records
        self.geometry_col = geometry_col
        self.kwargs = kwargs

    @staticmethod
    def _delta_encode(arcs):
        """
        Given a list of arcs, perform delta encoding for each arc,
        returning the modified list.
        """
        dest_arcs = []
        for arc in arcs:
            delta_arc = []
            previous_position = [0, 0]
            for current_position in arc:
                delta_position = [current_position[0]-previous_position[0],
                                  current_position[1]-previous_position[1]]
                previous_position = current_position
                delta_arc.append(delta_position)
            dest_arcs.append(delta_arc)
        return dest_arcs

    @staticmethod
    def _make_feature(record, geom_column):
        """
        Given a database row via Psycopg's RealDictCursor
        return back a completed TopoJSON feature containing
        properties and geometries.
        """
        geometry = json.loads(record.pop(geom_column))
        feature = dict(dict(geometry), properties=record)
        encoded_feature = json.dumps(feature)
        return encoded_feature

    def _make_geometry_collection(self, features_list, arcs_list):
        """
        Given a list containing GeoJSON features, return as a
        TopoJSON Topology GeometryCollection.
        """
        features_json = [json.loads(feature) for feature in features_list]
        layer_name = self.kwargs['file'].split('.')[0]
        feature_collection = dict(type='Topology',
                                  transform=dict(scale=[1, 1], translate=[0, 0]),
                                  objects={
                                      # Alternative dictionary comprehension pattern
                                      # Use if you don't want to wrap these features in
                                      # GeometryCollection object.
                                      # feat['properties']['gid']: feat for feat in features_json
                                      layer_name: {'type': 'GeometryCollection', 'geometries': features_json}
                                  },
                                  arcs=arcs_list)
        encoded_feature_collection = json.dumps(feature_collection)
        return encoded_feature_collection

    def _get_arcs(self):
        """
        Query postgis to populate "arcs" array. Will delta-encode arcs.
        NOTE: Might want to revise to utilize the topology_id and layer_id
              attributes of the topogeometry composite datatype.
              See: http://postgis.net/docs/topogeometry.html
        """
        # Given a topology layer name, SELECT the topology dataset
        # which the layer is a member of.
        select_topology_by_layer = "SELECT name " \
                        "FROM layer as l " \
                        "INNER JOIN topology AS t " \
                        "ON l.topology_id = t.id " \
                        "WHERE l.table_name = '%s' " % self.kwargs["topology_layer"]


        with PostGISConnection(**self.kwargs) as db:
            try:
                db.execute(select_topology_by_layer)
                query_results = db.fetchall()
                root_topology_name = query_results[0]['name']

                # NOTE We're forcing a transform to WGS84 and sorting edges.
                select_arcs_by_root_topology = "SELECT ST_AsGeoJSON(ST_Transform(geom, 4326)) as arc_geom " \
                                               "FROM %s.edge AS e " \
                                               "ORDER BY e.edge_id" % root_topology_name
                db.execute(select_arcs_by_root_topology)
                arc_query_results = db.fetchall()
                # Convert query results into a list of arcs
                arcs = [json.loads(arc['arc_geom'])['coordinates'] for arc in arc_query_results]
                delta_arcs = self._delta_encode(arcs)
                return delta_arcs
            except Error as e:
                print "PostGIS SQL Execution Error: ", e.message
                raise e

    def encode(self):
        """
        Return back a string representing a TopoJSON Topology GeometryCollection.
        """
        features = [self._make_feature(row, self.geometry_col) for row in self.records]
        arcs = self._get_arcs()
        feature_collection = self._make_geometry_collection(features, arcs)
        return feature_collection

