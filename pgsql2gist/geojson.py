__author__ = 'matt'
__date__ = '11/24/13'

import collections
import json


class OutOfBoundsError(Exception):
    pass


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
                # raise a bad coordinate error.

    def _is_feat_wgs84(self, geometry):
        """
        Given a geometry check that is within a valid WGS84 lat lon bbox.
        """
        coordinates = self._get_coordinates(geometry['coordinates'])
        for pair in coordinates:
            self._is_coord_wgs84(pair)
        # Didn't get an exception, return True.
        return True

    def _is_coord_wgs84(self, coordinate):
        if 180 < coordinate[0] or coordinate[0] < -180:
            raise OutOfBoundsError("Coordinate %f, %f is not valid WGS84" % (coordinate[0], coordinate[1]))
        if 90 < coordinate[1] or coordinate[1] < -90:
            raise OutOfBoundsError("Coordinate %f, %f is not valid WGS84" % (coordinate[0], coordinate[1]))
        return True

    def make_feature(self, record, geom_column):
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
