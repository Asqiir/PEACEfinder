//window.onload = function() {

//var map = new ol.Map({target: 'map'});

//map.setView(new ol.View({
//    center: [0, 0],
//    zoom: 2
//  }));

//};

window.onload = function() {

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

};