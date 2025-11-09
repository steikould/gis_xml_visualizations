import xml.etree.ElementTree as ET

class ScoutGISParser:
    def __init__(self, filepath):
        self.tree = ET.parse(filepath)
        self.root = self.tree.getroot()

    def to_dict(self):
        """
        Parses the Scout GIS XML file and returns a dictionary representation.
        """
        layers = []
        for layer_element in self.root.findall('Layer'):
            layer = {
                'name': layer_element.get('name'),
                'type': layer_element.get('type'),
                'features': []
            }
            for feature_element in layer_element.findall('Feature'):
                feature = {
                    'id': feature_element.get('id'),
                    'geometry': self._parse_geometry(feature_element.find('Geometry')),
                    'attributes': self._parse_attributes(feature_element.find('Attributes')),
                    'style': self._parse_style(feature_element.find('Style'))
                }
                layer['features'].append(feature)
            layers.append(layer)
        return layers

    def _parse_geometry(self, geometry_element):
        """
        Parses the geometry element.
        """
        point_element = geometry_element.find('Point')
        if point_element is not None:
            return {
                'type': 'Point',
                'coordinates': [
                    float(point_element.get('x')),
                    float(point_element.get('y'))
                ]
            }

        linestring_element = geometry_element.find('LineString')
        if linestring_element is not None:
            coords_text = linestring_element.find('Coordinates').text
            coordinates = [
                [float(coord) for coord in pair.split(' ')]
                for pair in coords_text.split(', ')
            ]
            return {
                'type': 'LineString',
                'coordinates': coordinates
            }

        polygon_element = geometry_element.find('Polygon')
        if polygon_element is not None:
            coords_text = polygon_element.find('Coordinates').text
            coordinates = [
                [float(coord) for coord in pair.split(' ')]
                for pair in coords_text.split(', ')
            ]
            return {
                'type': 'Polygon',
                'coordinates': [coordinates] # GeoJSON polygons have an extra level of nesting for rings
            }

        return None

    def _parse_attributes(self, attributes_element):
        """
        Parses the attributes element.
        """
        attributes = {}
        for attribute_element in attributes_element.findall('Attribute'):
            attributes[attribute_element.get('name')] = attribute_element.get('value')
        return attributes

    def _parse_style(self, style_element):
        """
        Parses the style element.
        """
        style = {}
        if style_element is not None:
            for element in style_element:
                style[element.tag.lower()] = element.attrib
        return style
