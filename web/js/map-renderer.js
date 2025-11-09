class MapRenderer {
    constructor(containerSelector) {
        this.container = d3.select(containerSelector);
        this.width = this.container.node().getBoundingClientRect().width;
        this.height = this.container.node().getBoundingClientRect().height;

        this.svg = this.container.append('svg')
            .attr('width', this.width)
            .attr('height', this.height);

        this.projection = d3.geoMercator()
            .scale(1)
            .translate([0, 0]);

        this.path = d3.geoPath().projection(this.projection);

        this.g = this.svg.append('g');

        const zoom = d3.zoom()
            .scaleExtent([1, 8])
            .on('zoom', (event) => {
                this.g.attr('transform', event.transform);
            });

        this.svg.call(zoom);
    }

    addLayer(data) {
        // Fit the projection to the data
        this.projection.fitSize([this.width, this.height], data);

        // Draw the features, excluding points, which are handled separately
        this.g.selectAll('path')
            .data(data.features.filter(d => d.geometry.type !== 'Point'))
            .enter().append('path')
            .attr('d', this.path)
            .attr('fill', d => {
                if (d.geometry.type === 'Polygon') {
                    return d.properties.style.fill.color;
                }
                return 'none';
            })
            .attr('stroke', d => {
                if (d.properties.style.stroke) {
                    return d.properties.style.stroke.color;
                }
                return 'none';
            })
            .attr('stroke-width', d => {
                if (d.properties.style.stroke) {
                    return d.properties.style.stroke.width;
                }
                return 0;
            })
            .attr('opacity', d => {
                if (d.properties.style.fill && d.properties.style.fill.opacity) {
                    return d.properties.style.fill.opacity;
                }
                return 1;
            });

        // Draw points as circles
        this.g.selectAll('circle')
            .data(data.features.filter(d => d.geometry.type === 'Point'))
            .enter().append('circle')
            .attr('cx', d => this.projection(d.geometry.coordinates)[0])
            .attr('cy', d => this.projection(d.geometry.coordinates)[1])
            .attr('r', d => d.properties.style.size.value)
            .attr('fill', d => d.properties.style.fill.color);
    }
}
