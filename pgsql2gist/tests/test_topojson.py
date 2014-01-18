__author__ = 'matt'
__date__ = '12/30/13'
"""
test_topojson.py

Due to the implementation of the TopoJSONConstructor class, these tests require
that a database, 'pgsql2gist_test' has been created and populated using test_data.sql

See .travis.yml for example instructions on creating a PostGIS-enabled db and
populating it with test_data.sql.
"""
from decimal import Decimal
from pgsql2gist import TopoJSONConstructor

class TestTopoJSONLineCreation(object):
    """
    Test TopoJSONConstructor.encode() returns expected values for a set of MultiLineString geometries.
    """
    def setup(self):
        self.records = [
            {'geometry': '{ "type": "MultiLineString", "arcs": [[1]]}', 'id': Decimal('3'), 'name': 'Neptune'},
            {'geometry': '{ "type": "MultiLineString", "arcs": [[2]]}', 'id': Decimal('2'), 'name': 'Venus'},
            {'geometry': '{ "type": "MultiLineString", "arcs": [[3]]}', 'id': Decimal('1'), 'name': 'Mars'}
        ]

        self.args_dict = {'description': 'sample description',
                          'format': 'topojson',
                          'geom_col': 'geometry',
                          'database': 'pgsql2gist_test',
                          'host': 'localhost',
                          'user': 'postgres',
                          'file': 'test_lines.topojson',
                          'password': None,
                          'topology_layer': 'test_lines',
                          'port': 5432,
                          'SELECT': 'SELECT id, name, AsTopoJSON(topogeoms, NULL) AS geometry FROM test_data.test_lines;'}

    def test_encoding(self):
        constructor = TopoJSONConstructor(self.records, 'geometry', **self.args_dict)
        feature_collection = constructor.encode()
        expected_value = '{"objects": {"test_lines": {"type": "GeometryCollection", "geometries": [{"type": "MultiLineString", "properties": {"id": 3, "name": "Neptune"}, "arcs": [[1]]}, {"type": "MultiLineString", "properties": {"id": 2, "name": "Venus"}, "arcs": [[2]]}, {"type": "MultiLineString", "properties": {"id": 1, "name": "Mars"}, "arcs": [[3]]}]}}, "type": "Topology", "transform": {"translate": [0, 0], "scale": [1, 1]}, "arcs": [[[84.4609252640606, 55.4177466161223], [-1.327480161319599, -94.25109145369291], [49.116765968826, 2.654960322639198], [-6.637400806598009, 75.66636919521821]], [[-50.9420511905403, -20.2486225790959], [112.83581371216741, 0.0]], [[-126.276550345429, 3.97789036498713], [38.165054637939406, 43.47497528321747]], [[-131.586470990707, -17.2617922161267], [36.837574476619295, 3.318700403299001], [-0.3318700403298891, -39.160664758928704], [-36.505704436289406, -0.3318700403299033], [0.0, 36.1738343959596]], [[28.7067584886367, 34.1780640350084], [29.204563549031597, 1.3274801613196061], [4.3143105242887, -31.859523871670774], [-29.868303629691297, -1.65935020164952], [-3.6505704436290003, 32.191393912000684]], [[-151.830543450831, 67.3650680679988], [24.558382984412987, 0.9956101209896957], [1.9912202419790077, -19.2484623391344], [-25.885863145732017, 0.9956101209896957], [-0.6637400806599771, 17.257242097155007]]]}'
        assert feature_collection == expected_value


class TestTopoJSONPolygonCreation(object):
    """
    Test TopoJSONConstructor.encode() returns expected values for a set of Polygon geometries.
    """
    def setup(self):
        self.records = [
            {'geometry': '{ "type": "MultiPolygon", "arcs": [[[3]]]}', 'id': Decimal('3'), 'name': 'Pie'},
            {'geometry': '{ "type": "MultiPolygon", "arcs": [[[4]]]}', 'id': Decimal('2'), 'name': 'Cookie'},
            {'geometry': '{ "type": "MultiPolygon", "arcs": [[[5]]]}', 'id': Decimal('1'), 'name': 'Mint'}
        ]

        self.args_dict = {'description': 'sample description',
                          'format': 'topojson',
                          'geom_col': 'geometry',
                          'database': 'pgsql2gist_test',
                          'host': 'localhost',
                          'user': 'postgres',
                          'file': 'test_polygons.topojson',
                          'password': None,
                          'topology_layer': 'test_polygons',
                          'port': 5432,
                          'SELECT': 'SELECT id, name, AsTopoJSON(topogeoms, NULL) AS geometry FROM test_data.test_polygons;'}

    def test_encoding(self):
        constructor = TopoJSONConstructor(self.records, 'geometry', **self.args_dict)
        feature_collection = constructor.encode()
        expected_value = '{"objects": {"test_polygons": {"type": "GeometryCollection", "geometries": [{"type": "MultiPolygon", "properties": {"id": 3, "name": "Pie"}, "arcs": [[[3]]]}, {"type": "MultiPolygon", "properties": {"id": 2, "name": "Cookie"}, "arcs": [[[4]]]}, {"type": "MultiPolygon", "properties": {"id": 1, "name": "Mint"}, "arcs": [[[5]]]}]}}, "type": "Topology", "transform": {"translate": [0, 0], "scale": [1, 1]}, "arcs": [[[84.4609252640606, 55.4177466161223], [-1.327480161319599, -94.25109145369291], [49.116765968826, 2.654960322639198], [-6.637400806598009, 75.66636919521821]], [[-50.9420511905403, -20.2486225790959], [112.83581371216741, 0.0]], [[-126.276550345429, 3.97789036498713], [38.165054637939406, 43.47497528321747]], [[-131.586470990707, -17.2617922161267], [36.837574476619295, 3.318700403299001], [-0.3318700403298891, -39.160664758928704], [-36.505704436289406, -0.3318700403299033], [0.0, 36.1738343959596]], [[28.7067584886367, 34.1780640350084], [29.204563549031597, 1.3274801613196061], [4.3143105242887, -31.859523871670774], [-29.868303629691297, -1.65935020164952], [-3.6505704436290003, 32.191393912000684]], [[-151.830543450831, 67.3650680679988], [24.558382984412987, 0.9956101209896957], [1.9912202419790077, -19.2484623391344], [-25.885863145732017, 0.9956101209896957], [-0.6637400806599771, 17.257242097155007]]]}'
        assert feature_collection == expected_value
