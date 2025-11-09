from parser.xml_parser import ScoutGISParser

class GeometryConverter:
    def __init__(self, data):
        self.data = data

    def to_geojson(self):
        """
        Converts the parsed Scout GIS data to a GeoJSON FeatureCollection.
        """
        features = []
        for layer in self.data:
            for feature_data in layer['features']:
                feature = {
                    'type': 'Feature',
                    'id': feature_data['id'],
                    'geometry': self._convert_geometry(feature_data['geometry']),
                    'properties': {
                        **feature_data['attributes'],
                        'style': feature_data['style']
                    }
                }
                features.append(feature)

        return {
            'type': 'FeatureCollection',
            'features': features
        }

    def _convert_geometry(self, geometry_data):
        """
        Converts a single geometry to GeoJSON format.
        """
        if geometry_data['type'] == 'Point':
            return {
                'type': 'Point',
                'coordinates': geometry_data['coordinates']
            }
        if geometry_data['type'] == 'LineString':
            return {
                'type': 'LineString',
                'coordinates': geometry_data['coordinates']
            }
        if geometry_data['type'] == 'Polygon':
            return {
                'type': 'Polygon',
                'coordinates': geometry_data['coordinates']
            }
        return None
