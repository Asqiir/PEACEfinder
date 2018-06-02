var map = new ol.Map({
	target: 'map',
	layers: [
		new ol.layer.Tile({
			source: new ol.source.OSM()
		}),
		new ol.layer.Heatmap({
			source: new ol.source.Vector({
			format: new ol.format.GeoJSON(),
			loader: function(extent, resolution, projection) {
				var xhr = new XMLHttpRequest();
				xhr.open('GET', null); // TODO: insert request URL
				xhr.onload = function() {
					if (xhr.status == 200) {
						map.addFeatures(map.getFormat().readFeatures(xhr.responseText));
					}
				}
				xhr.send();
			},
			strategy: ol.loadingstrategy.bbox
		 })
		})
	],
	view: new ol.View({
		center: ol.proj.fromLonLat([12.110148, 54.123435]),
		zoom: 12
	})
});

