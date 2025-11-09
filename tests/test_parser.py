import unittest
from parser.xml_parser import ScoutGISParser

class TestXMLParser(unittest.TestCase):

    def setUp(self):
        self.parser = ScoutGISParser('tests/sample-data/scout-gis-export.xml')
        self.data = self.parser.to_dict()

    def test_to_dict_point(self):
        layer = self.data[0]
        self.assertEqual(layer['name'], 'Cities')
        self.assertEqual(layer['type'], 'point')
        feature = layer['features'][0]
        self.assertEqual(feature['id'], '1')
        self.assertEqual(feature['geometry']['type'], 'Point')
        self.assertEqual(feature['geometry']['coordinates'], [-122.4194, 37.7749])

    def test_to_dict_linestring(self):
        layer = self.data[1]
        self.assertEqual(layer['name'], 'Rivers')
        self.assertEqual(layer['type'], 'line')
        feature = layer['features'][0]
        self.assertEqual(feature['id'], '2')
        self.assertEqual(feature['geometry']['type'], 'LineString')
        self.assertEqual(feature['geometry']['coordinates'], [[-122.4, 37.8], [-122.5, 37.9], [-122.6, 37.8]])

    def test_to_dict_polygon(self):
        layer = self.data[2]
        self.assertEqual(layer['name'], 'Parks')
        self.assertEqual(layer['type'], 'polygon')
        feature = layer['features'][0]
        self.assertEqual(feature['id'], '3')
        self.assertEqual(feature['geometry']['type'], 'Polygon')
        self.assertEqual(feature['geometry']['coordinates'], [[[-122.45, 37.75], [-122.4, 37.7], [-122.45, 37.7], [-122.45, 37.75]]])

if __name__ == '__main__':
    unittest.main()
