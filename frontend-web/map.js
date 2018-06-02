var mapLayers = null;
var mapOverlay = document.getElementById('map-overlay');

var map = new ol.Map({
	target: 'map',
	layers: [
		new ol.layer.Tile({
			source: new ol.source.OSM()
		})
	],
	view: new ol.View({
		center: ol.proj.fromLonLat([12.110148, 54.123435]),
		zoom: 12
	})
});

function downloadMapLayers() {
	var xhr = new XMLHttpRequest();
	xhr.addEventListener("readystatechange", function() {
		if (xhr.status == 200) {
			if(mapLayers == null) {
				mapLayers = JSON.parse(xhr.responseText).layers;
				addMapLayersToMap();
			}
		}
	});
	xhr.open("GET", "map-layers.json");
	xhr.send();
}

function addMapLayersToMap() {
	for (var i = 0; i < mapLayers.length; i++) {
		var vectorSource = new ol.source.Vector({
			format: new ol.format.GeoJSON(),
			url: mapLayers[i].url,
			strategy: ol.loadingstrategy.bbox
		});

		var vectorLayer = new ol.layer.Heatmap({
			source: vectorSource,
			gradient: (mapLayers[i].envpriority > 0 ? ['#F1F8E9', '#8BC34A'] : ['#FFEBEE', '#F44336']),
			opacity: Math.abs(mapLayers[i].envpriority) / 100
		});

		mapLayers.olLayer = vectorLayer;

		map.addLayer(vectorLayer);

		mapOverlay.innerHTML += "<label class=\"mdl-switch mdl-js-switch mdl-js-ripple-effect\" for=\"" + mapLayers[i].id + "\"><input type=\"checkbox\" id=\"" + mapLayers[i].id + "\" class=\"mdl-switch__input\" checked><span class=\"mdl-switch__label\">" + mapLayers[i].name + "</span></label>";
	}
}