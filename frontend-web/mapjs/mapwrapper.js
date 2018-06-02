var mapwrapper = {
	init: function() {
		this.map = document.getElementById("map");
		this.map.addLayer(new OpenLayers.Layer.OSM());
		this.markers = new OpenLayers.Layer.Markers( "Markers" );
		this.map.addLayer(this.markers);
	},

	addPlace: function(place) {
		place.olLonLat = new OpenLayers.LonLat(place.lon, place.lat)
				.transform(
					new OpenLayers.Projection("EPSG:4326"),
					map.getProjectionObject()
				);
		this.markers.addMarker(new OpenLayers.Marker(place.olLonLat));
	},

	centerPlace: function(place, zoom) {
		this.map.setCenter(lonLat, zoom);
	}
}