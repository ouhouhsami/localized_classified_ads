
var source = new Proj4js.Proj('EPSG:4326');    
var dest = new Proj4js.Proj('EPSG:900913');  
var homes = []

var map

var eraseControlDiv

function EraseControl(controlDiv, map) {

	  // Set CSS styles for the DIV containing the control
	  // Setting padding to 5 px will offset the control
	  // from the edge of the map
	  /*controlDiv.style.padding = '1px';*/
	  controlDiv.className = 'erase_button'
	  // Set CSS for the control border
	  var controlUI = document.createElement('DIV');
	  /*
	  controlUI.style.backgroundColor = 'white';
	  controlUI.style.borderStyle = 'solid';
	  controlUI.style.borderWidth = '2px';
	  controlUI.style.cursor = 'pointer';
	  controlUI.style.textAlign = 'center';
	  */
	  controlUI.title = 'Click to set the map to Home';
	  controlDiv.appendChild(controlUI);

	  // Set CSS for the control interior
	  var controlText = document.createElement('DIV');
	  /*
	  controlText.style.fontFamily = 'Arial,sans-serif';
	  controlText.style.fontSize = '12px';
	  controlText.style.paddingLeft = '4px';
	  controlText.style.paddingRight = '4px';
	  */
	  controlText.innerHTML = 'Effacer la zone';
	  controlUI.appendChild(controlText);

	  // Setup the click event listeners: simply set the map to Chicago
	  google.maps.event.addDomListener(controlUI, 'click', function() {
	    //map.setCenter(chicago)
	    $(eraseControlDiv).hide()
	    initPath()
	  });
}


// initialize
$(function(){
	
	
	var tt = document.createElement('DIV');
	tt.className = 'tooltip';
	var tt_text = document.createElement('DIV');
	$(tt_text).html("Cliquer pour définir le 1<sup>er</sup> point de votre zone de recherche")
	tt.appendChild(tt_text);
	
	var options = {
		zoom: 12,
		/*center: new google.maps.LatLng(48.858, 2.333),*/
		center: new google.maps.LatLng(48.856, 2.333),
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
	map = new google.maps.Map(document.getElementById('map'), options);
	
 	eraseControlDiv = document.createElement('DIV');
	var eraseControl = new EraseControl(eraseControlDiv, map);

	eraseControlDiv.index = 1;
	map.controls[google.maps.ControlPosition.TOP_RIGHT].push(eraseControlDiv);
	$(eraseControlDiv).hide()

	map.controls[google.maps.ControlPosition.TOP_RIGHT].push(tt);
	$(tt).hide()

	var poly = null;
	var poly_listener = null;
	var markers = []
	var has_poly = 'false';
	var image = new google.maps.MarkerImage('/static/img/marker-edition.png', new google.maps.Size(9, 9), new google.maps.Point(0, 0), new google.maps.Point(5, 5));
	
	google.maps.event.addListener(map, 'click', function (event) {
		if(has_poly == 'true'){
			initPath()
			has_poly = 'false'
		}
		if(!poly){
			// create poly
			$(eraseControlDiv).show()
			poly = new google.maps.Polygon({strokeWeight: 2, strokeColor: '#20B2AA', fillColor: '#FFB82E', map:map});
			poly_listener = google.maps.event.addListener(poly, 'click', function (event) {
						path = poly.getPath();
						path.insertAt(path.length, event.latLng);
						marker = new google.maps.Marker({position: event.latLng, map: map, icon: image});
						markers.push(marker)
						poly.setPath(path)
						setPath()
			})

			/*
			google.maps.event.addListener(poly, 'mousemove', function (event) {
				if(poly.getPath().getLength() > 1){
					poly.getPath().pop()
				}
				poly.getPath().push(event.latLng)
			})
			*/
			
		}
		path = poly.getPath();
		path.insertAt(path.length, event.latLng);
		marker = new google.maps.Marker({position: event.latLng, map: map, icon: image});
		markers.push(marker)
		poly.setPath(path)
		setPath()
		if(poly.getPath().getLength() > 0){
			$(tt_text).html("Cliquer pour ajouter un point à votre zone de recherche")
		} else {
			$(tt_text).html("Cliquer pour définir le 1<sup>er</sup> point de votre zone de recherche")
		}
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
			$(eraseControlDiv).show()
			has_poly = 'true';
			poly = new google.maps.Polygon({strokeWeight: 2, strokeColor: '#20B2AA', fillColor: '#FFB82E', map:map});  
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
		poly = null;
		/*
		google.maps.event.removeListener(poly_listener);
		*/
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

		google.maps.event.addListener(map, 'mouseout', function(e) {
			$(tt).hide()
			//poly.setPath(poly.getPath().pop())
		})
		google.maps.event.addListener(map, 'mouseover', function(e) {
			$(tt).show()
			//poly.setPath(poly.getPath().push(e.latLng))
		})
		google.maps.event.addListener(map, 'mousemove', function(e) {
			$(tt).css('top', e.pixel.y+10)
			$(tt).css('left', e.pixel.x+10)
			$(tt).css('width', 140)
			try
				{
					if(poly.getPath().getLength() < 3){
						if(poly.getPath().getLength() > 1){
							poly.getPath().pop()
						}
						poly.getPath().push(e.latLng)
					}
				}
			catch(err)
  				{
	
				}
		})		

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