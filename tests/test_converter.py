import unittest
import json
from parser.xml_parser import ScoutGISParser
from parser.geometry_converter import GeometryConverter

class TestGeometryConverter(unittest.TestCase):

    def setUp(self):
        parser = ScoutGISParser('tests/sample-data/scout-gis-export.xml')
        self.converter = GeometryConverter(parser.to_dict())
        self.geojson = self.converter.to_geojson()

    def test_to_geojson_point(self):
        feature = self.geojson['features'][0]
        self.assertEqual(feature['geometry']['type'], 'Point')
        self.assertEqual(feature['geometry']['coordinates'], [-122.4194, 37.7749])

    def test_to_geojson_linestring(self):
        feature = self.geojson['features'][1]
        self.assertEqual(feature['geometry']['type'], 'LineString')
        self.assertEqual(feature['geometry']['coordinates'], [[-122.4, 37.8], [-122.5, 37.9], [-122.6, 37.8]])

    def test_to_geojson_polygon(self):
        feature = self.geojson['features'][2]
        self.assertEqual(feature['geometry']['type'], 'Polygon')
        self.assertEqual(feature['geometry']['coordinates'], [[[-122.45, 37.75], [-122.4, 37.7], [-122.45, 37.7], [-122.45, 37.75]]])

if __name__ == '__main__':
    unittest.main()
