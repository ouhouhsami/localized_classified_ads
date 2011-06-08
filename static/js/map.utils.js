var selectedFeature

/*
function onFeatureUnselect(feature) {

	map.removePopup(feature.popup);
	feature.popup.destroy();
	feature.popup = null;

	console.log('selected')
} 

function onFeatureSelect(feature) {

	selectedFeature = feature;
	popup = new OpenLayers.Popup.FramedCloud("chicken",
	feature.geometry.getBounds().getCenterLonLat(),
	null,
	"<div style='font-size:.8em'>Feature: " + feature.id +"<br />Area: " + feature.geometry.getArea()+"</div>",
	null, true, onPopupClose);
	feature.popup = popup;
	map.addPopup(popup);

} 

*/

function add_layer(map){

	renderer = OpenLayers.Util.getParameters(window.location.href).renderer;
	renderer = (renderer) ? [renderer] : OpenLayers.Layer.Vector.prototype.renderers; 

	layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
	layer_style.fillOpacity = 0.2;
	layer_style.graphicOpacity = 1; 

	vectorLayer = new OpenLayers.Layer.Vector("Simple Geometry", {
		style: layer_style,
		renderers: renderer,
		displayInLayerSwitcher: false,
	}); 



	
	function selected (evt) {
		console.log(evt.feature.id + " selected on " + this.name);
	}
	
	map.addLayer(vectorLayer);
	map.ads_layer = vectorLayer
	map.layer_style = layer_style	
	
	/*
	map.ads_layer.events.register("featureselected", map.ads_layer, selected);
	
	var control = new OpenLayers.Control.SelectFeature(map.ads_layer);
	map.addControl(control);
	control.activate();
	*/
	

}


function create_map(id){
	// create map and layer
	
	map = new OpenLayers.Map('map', 
					{
						projection: new OpenLayers.Projection('EPSG:900913'), 
						displayProjection: new OpenLayers.Projection('EPSG:4326'),
					}
				);

	renderer = OpenLayers.Util.getParameters(window.location.href).renderer;
	renderer = (renderer) ? [renderer] : OpenLayers.Layer.Vector.prototype.renderers; 
    //console.log(renderer)
	//map.addControl(new OpenLayers.Control.LayerSwitcher());

	var gmap = new OpenLayers.Layer.Google(
	    "Google Streets", // the default
	    {numZoomLevels: 20, sphericalMercator: true}
	);
	var ghyb = new OpenLayers.Layer.Google(
	    "Google Hybrid",
	    {type: google.maps.MapTypeId.HYBRID, numZoomLevels: 20, sphericalMercator: true}
	);
	var gsat = new OpenLayers.Layer.Google(
	    "Google Satellite",
	    {type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22, sphericalMercator: true}
	);
	map.addLayers([gmap, ghyb, gsat]);
		
	add_layer(map)
	
	return map
}

function center_map(map, lon, lat){
	var pt = new OpenLayers.LonLat(lon, lat);
	pt.transform(map.displayProjection, map.projection);
	map.setCenter(pt, 12);
}

function add_marker(map, lon, lat){
	var style_blue = OpenLayers.Util.extend({}, map.layer_style);
	style_blue.strokeColor = "blue";
	style_blue.fillColor = "#3BB9FF";
	style_blue.graphicName = "circle";
	style_blue.pointRadius = 10;
	style_blue.strokeWidth = 2;
	style_blue.strokeLinecap = "butt";
	style_blue.externalGraphic = "/static/img/home_icon.png";
	
	var point = new OpenLayers.Geometry.Point(lon, lat);
	point.transform(map.displayProjection, map.projection);
	var pointFeature = new OpenLayers.Feature.Vector(point,null,style_blue); 
	
	map.ads_layer.addFeatures([pointFeature])
    return pointFeature
}



