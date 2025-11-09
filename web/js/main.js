d3.json('data/sample-layers.geojson').then(data => {
    const mapRenderer = new MapRenderer('#map-container');
    mapRenderer.addLayer(data);
});
