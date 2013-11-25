__author__ = 'matt'
__date__ = '11/24/13'

import json

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

    def make_feature(self, record, geom_column):
        """
        Given a database row via Psycopg's RealDictCursor
        return back a completed GeoJSON feature containing
        properties and geometries.
        """
        geometry = json.loads(record.pop(geom_column))
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
