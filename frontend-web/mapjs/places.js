var places = [];

class Place {
	constructor(lon, lat, qualities = null) {
		this.lon = lon;
		this.lat = lat;
		this.qualities = qualities;
		places.push(this);
		this.index = places.lenght - 1;
		this.olLonLat = null;
	}
}