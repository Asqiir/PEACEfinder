var mapLayers = null;
var mapOverlayOptions = document.getElementById('map-overlay-options');

var silentStart = location.href.includes("silent");

/*var specialHeatmap = new ol.layer.Heatmap({
			source: new ol.source.Vector({
				format: new ol.format.GeoJSON(),
				url: "best-places-0.01.json",
				strategy: ol.loadingstrategy.bbox
			}),
			radius: 20
		});

specialHeatmap.getSource().on('addfeature', function(event) {
	var envpriority = event.feature.get('envpriority');
	console.log(envpriority);
	event.feature.set('weight', envpriority / 100);
});*/

/*var best5Places = new ol.layer.Vector({
	source: new ol.source.Vector({
		format: new ol.format.GeoJSON(),
		url: "best-5-places.json",
		strategy: ol.loadingstrategy.bbox
	}),
	radius: 20
});*/

var map = new ol.Map({
	target: 'map',
	layers: [
		new ol.layer.Tile({
			source: new ol.source.OSM()
		}) // Add layers here, when 
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
			opacity: Math.abs(mapLayers[i].envpriority) / 120,
			radius: (mapLayers[i].radius != undefined ? mapLayers[i].radius : 20 * Math.abs(mapLayers[i].envpriority) / 120),
			shadow: 0
		});

		vectorLayer.setVisible(!silentStart);

		mapLayers[i].olLayer = vectorLayer;

		map.addLayer(vectorLayer);

		mapOverlayOptions.innerHTML += "<label class=\"mdl-switch " + (mapLayers[i].envpriority < 0 ? "mdl-switch-red" : "") + " mdl-js-switch mdl-js-ripple-effect\" for=\"" + mapLayers[i].id + "\"><input type=\"checkbox\" id=\"" + mapLayers[i].id + "\" class=\"mdl-switch__input\" onchange=\"setMapLayerVisibility(this.id, this.checked)\" " + (silentStart ? "" : "checked") + "><span class=\"mdl-switch__label\">" + mapLayers[i].name + "</span></label>";
	}
}

function setMapLayerVisibility(id, visible) {
	for (var i = 0; i < mapLayers.length; i++) {
		if (mapLayers[i].id == id) {
			mapLayers[i].olLayer.setVisible(visible);
		}
	}
}

// SEARCH FOR PLACE

/*var placeMarker = new ol.

document.getElementById("search-input").addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        searchForPlace();
    }
});

function searchForPlace() {

}*/