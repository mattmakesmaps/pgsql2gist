__author__ = 'matt'
__date__ = '11/23/13'
import sys, unittest
from nose.tools import with_setup, raises
from pgsql2gist import GeoJSONConstructor, OutOfBoundsError

class TestOutOfBoundsErrorX(object):
    def setup(self):
        self.records = [
            {'geometry': '{"type":"Point","coordinates":[-122.27,47.69]}', 'hoods_': 2.0},
            {'geometry': '{"type":"Point","coordinates":[-199,47.64]}', 'hoods_': 3.0}
        ]

    @raises(OutOfBoundsError)
    def test_outofboundserror(self):
        """
        Check that given a properly formatted dict, that a string representing a
        GeoJSON Feature Collection is returned.
        """
        constructor = GeoJSONConstructor(self.records, 'geometry')
        feature_collection = constructor.encode()
        expected_value = '{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [-122.27, 47.69]}, "type": "Feature", "properties": {"hoods_": 2.0}}, {"geometry": {"type": "Point", "coordinates": [-122.28, 47.64]}, "type": "Feature", "properties": {"hoods_": 3.0}}]}'

class TestOutOfBoundsErrorY(object):
    def setup(self):
        self.records = [
            {'geometry': '{"type":"Point","coordinates":[-122.27,47.69]}', 'hoods_': 2.0},
            {'geometry': '{"type":"Point","coordinates":[-111,100.64]}', 'hoods_': 3.0}
        ]

    @raises(OutOfBoundsError)
    def test_outofboundserror(self):
        """
        Check that given a properly formatted dict, that a string representing a
        GeoJSON Feature Collection is returned.
        """
        constructor = GeoJSONConstructor(self.records, 'geometry')
        feature_collection = constructor.encode()
        expected_value = '{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [-122.27, 47.69]}, "type": "Feature", "properties": {"hoods_": 2.0}}, {"geometry": {"type": "Point", "coordinates": [-122.28, 47.64]}, "type": "Feature", "properties": {"hoods_": 3.0}}]}'

class TestPointFeatureCollectionCreation(object):
    def setup(self):
        self.records = [
            {'geometry': '{"type":"Point","coordinates":[-122.27,47.69]}', 'hoods_': 2.0},
            {'geometry': '{"type":"Point","coordinates":[-122.28,47.64]}', 'hoods_': 3.0}
        ]

    def test_encoding(self):
        """
        Check that given a properly formatted dict, that a string representing a
        GeoJSON Feature Collection is returned.
        """
        constructor = GeoJSONConstructor(self.records, 'geometry')
        feature_collection = constructor.encode()
        expected_value = '{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [-122.27, 47.69]}, "type": "Feature", "properties": {"hoods_": 2.0}}, {"geometry": {"type": "Point", "coordinates": [-122.28, 47.64]}, "type": "Feature", "properties": {"hoods_": 3.0}}]}'
        assert feature_collection == expected_value

class TestMultiPolygonFeatureCollectionCreation(object):
    def setup(self):
        self.records = [
            {'geometry': '{ "type": "MultiPolygon","coordinates": [[[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],[[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],[[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]]}', 'hoods_': 2.0},
        ]

    def test_encoding(self):
        """
        Check that given a properly formatted dict, that a string representing a
        GeoJSON Feature Collection is returned.
        """
        constructor = GeoJSONConstructor(self.records, 'geometry')
        feature_collection = constructor.encode()
        expected_value = '{"type": "FeatureCollection", "features": [{"geometry": {"type": "MultiPolygon", "coordinates": [[[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]], [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]], [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]]}, "type": "Feature", "properties": {"hoods_": 2.0}}]}'
        assert feature_collection == expected_value
