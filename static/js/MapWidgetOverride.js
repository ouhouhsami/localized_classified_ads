

MapWidget.prototype.getControls = function(layer) {
	this.panel = new OpenLayers.Control.Panel({'displayClass': 'olControlEditingToolbar'});
	var nav = [new OpenLayers.Control.Navigation()];
	var draw_ctl;
	if (this.options.is_linestring) {
		draw_ctl = new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Path, {'displayClass': 'olControlDrawFeaturePath'});
	} else if (this.options.is_polygon) {
		draw_ctl = new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Polygon, {'displayClass': 'olControlDrawFeaturePolygon'});
	} else if (this.options.is_point) {
		draw_ctl = new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Point, {'displayClass': 'olControlDrawFeaturePoint'});
	} else { // generic geometry
		var point_ctl = new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Point, {'displayClass': 'olControlDrawFeaturePoint'});
		var path_ctl = new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Path, {'displayClass': 'olControlDrawFeaturePath'});
		var poly_ctl = new OpenLayers.Control.DrawFeature(layer, OpenLayers.Handler.Polygon, {'displayClass': 'olControlDrawFeaturePolygon'});
		draw_ctl = [point_ctl, path_ctl, poly_ctl];
	}
	if (this.options.modifiable) {
		var mod = [new OpenLayers.Control.ModifyFeature(layer, {'displayClass': 'olControlModifyFeature'})];
		this.controls = nav.concat(draw_ctl, mod);
	} else {
		if (!layer.features.length) {
			this.controls = nav.concat(draw_ctl);
		} else {
			this.controls = nav;
		}
	}
	if (this.options.has_results){
		this.layers.ads = new OpenLayers.Layer.Vector("Simple Geometry", {displayInLayerSwitcher: false}); 
		this.map.addLayer(this.layers.ads);
		var view = [new OpenLayers.Control.SelectFeature(
												this.layers.ads, 
												{
													'displayClass': 'olControlViewFeature',
													clickFeature: function(feature){
														popup = new OpenLayers.Popup(feature.classname, 
															new OpenLayers.LonLat(
																feature.coord_0,
																feature.coord_1), 
																new OpenLayers.Size(200,40), 
																'html', 
																true
														);
														popup.panMapIfOutOfView = true;
														popup.contentHTML = $('.'+feature.classname).html()
														this.map.addPopup(popup);
													}, 
													
												}
											)
											];
		this.controls = nav.concat(view, this.controls)
		
	}
};