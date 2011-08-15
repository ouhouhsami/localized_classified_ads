
var source = new Proj4js.Proj('EPSG:4326');    
var dest = new Proj4js.Proj('EPSG:900913');  
var homes = []


// initialize
$(function(){
	var options = {
		zoom: 12,
		center: new google.maps.LatLng(48.858, 2.333),
		mapTypeControl: true,
		panControl: false,
		mapTypeControl: false,
		streetViewControl: false,
		mapTypeControlOptions: { style: google.maps.MapTypeControlStyle.DROPDOWN_MENU },
		zoomControl: true,
		zoomControlOptions: {
			style: google.maps.ZoomControlStyle.SMALL,
			position: google.maps.ControlPosition.TOP_RIGHT
		},
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.getElementById('map'), options);
	var poly = null;
	var markers = []
	var has_poly = 'false';
	var image = new google.maps.MarkerImage('/static/img/marker-edition.png', new google.maps.Size(9, 9), new google.maps.Point(0, 0), new google.maps.Point(5, 5));
	
	google.maps.event.addListener(map, 'click', function (event) {
		console.log(has_poly)
		if(has_poly == 'true'){
			initPath()
			has_poly = 'false'
		}
		if(!poly){
			// create poly
			poly = new google.maps.Polygon({strokeWeight: 2, strokeColor: '#20B2AA', fillColor: '#eae56d', map:map});
		}
		path = poly.getPath();
		path.insertAt(path.length, event.latLng);
		marker = new google.maps.Marker({position: event.latLng, map: map, icon: image});
		markers.push(marker)
		poly.setPath(path)
		setPath()
	});
	// setPath from textarea
	setPath = function(){
		var polygon = "SRID=900913;POLYGON(("
		for(var i = 0; i<poly.getPath().getLength(); i++){
			var p = new Proj4js.Point(path.getAt(i).lng(), path.getAt(i).lat());
			Proj4js.transform(source, dest, p);    
			polygon += p.x+" "+p.y+','
			if(i == 0){
				pZero = p.x+" "+p.y+")"
			}
		}
		polygon += pZero+")"
		$('#id_location').val(polygon)
	}
	// getPath from textarea
	getPath = function(){
		if($('#id_location').val() != ''){
			console.log('getpath')
			has_poly = 'true';
			poly = new google.maps.Polygon({strokeWeight: 2, strokeColor: '#20B2AA', fillColor: '#eae56d', map:map});  
			path = poly.getPath();
			var points = $('#id_location').val().split('SRID=900913;POLYGON((')[1].split('))')[0].split(',');
			var latlngbounds = new google.maps.LatLngBounds( );
			for(i = 0; i<points.length-1; i++){
				var point = points[i].split(" ")
				var p = new Proj4js.Point(point[0], point[1]);
				Proj4js.transform(dest, source, p);
				path.insertAt(i, new google.maps.LatLng(p.y, p.x))
				latlngbounds.extend( new google.maps.LatLng(p.y, p.x) );
			}
			poly.setPath(path);
			map.fitBounds( latlngbounds );	
		};	
	}
	// initPath
	initPath = function(){
		poly.setMap(null)
		poly = null
		for(var i = 0; i<markers.length; i++){
			markers[i].setMap(null)
		}
		markers = [];
		has_poly = 'false';
	}
	
	// add homes
	var infowindow = new google.maps.InfoWindow({content: 'Annonce'})
	for(var i=0; i<homes.length; i++){
		var p = new Proj4js.Point(homes[i].x, homes[i].y);
		Proj4js.transform(dest, source, p);
		var marker = new google.maps.Marker({
			position: new google.maps.LatLng(p.y, p.x),
			map: map,
			icon: new google.maps.MarkerImage('/static/img/home.png')
		});
		marker.html = $('.'+homes[i].id).html()
		google.maps.event.addListener(marker, 'click', function(e) {
			infowindow.setContent(this.html)
			infowindow.open(map,this);
		});
		homes[i].marker = marker
    }
	getPath()
})

add_home = function(x, y, url, id){
	homes.push({'x':x, 'y':y, 'url':url, 'id':id})
}

open_popup = function(x, y, id){
	for(var i = 0; i<homes.length; i++){
		if(homes[i].id == id){
			google.maps.event.trigger(homes[i].marker, 'click')
		}
	}
}