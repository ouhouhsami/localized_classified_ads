var homes = [];
var map;

var drawingManager;
$(document).ready(function() {
	
	addUpdatePathEventListerner = function(){
		google.maps.event.addListener(overlay.getPath(), 'set_at', function(index){setPathToTextarea();});
		google.maps.event.addListener(overlay.getPath(), 'insert_at', function(index){setPathToTextarea()});
		google.maps.event.addListener(overlay.getPath(), 'remove_at', function(index){setPathToTextarea();});		
	}
	
	localizeMe = function(){
		if (navigator.geolocation) {
				navigator.geolocation.getCurrentPosition(function(position) {
					initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
					map.setCenter(initialLocation);
				});
			}else{
		}
	}
	var overlay = null;
    var options = {
        zoom: 12,
        center: new google.maps.LatLng(lat, lng),
        mapTypeControl: true,
        panControl: false,
        mapTypeControl: false,
        streetViewControl: false,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
        },
        zoomControl: true,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.SMALL,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

	var map = new google.maps.Map(document.getElementById("map"),options);
	drawingManager = new google.maps.drawing.DrawingManager({
		/*drawingControl: false, */
		drawingMode:google.maps.drawing.OverlayType.POLYGON,
		polygonOptions: polygonStyle,
		drawingControlOptions: {
			position: google.maps.ControlPosition.TOP_LEFT,
			drawingModes: [google.maps.drawing.OverlayType.POLYGON]
		}
	});
	drawingManager.setMap(map);
	drawingManager.setOptions({drawingMode:null});
	google.maps.event.addListener(drawingManager, 'overlaycomplete', function(event) {
		try {
			overlay.setMap(null);
		}
		catch(err) {		
		}
		overlay = event.overlay;
		overlay.setEditable(true);
		drawingManager.setOptions({drawingMode:null});
		setPathToTextarea();
		addUpdatePathEventListerner();
	});
	
	/*
	google.maps.event.addListener(map, 'click', function(event){
		
		try{
			overlay.setMap(null);
		}
		catch(err){
			
		}
		overlay = null;
		drawingManager.setOptions({drawingMode:google.maps.drawing.OverlayType.POLYGON});
		
	});
	*/
	
	setPathToTextarea = function(){
		var polygon = "SRID=900913;POLYGON(("
		for (var i = 0; i < overlay.getPath().getLength(); i++) {
			var p = {'x':overlay.getPath().getAt(i).lng() , 'y':overlay.getPath().getAt(i).lat()}
			polygon += p.x + " " + p.y + ','
			if (i == 0) {
				pZero = p.x + " " + p.y + ")"
			}
		}
		polygon += pZero + ")";
		$('#id_location').val(polygon);	
	};
	getPathFromTextarea = function(){
		if ($('#id_location').val() != '') {
			overlay = new google.maps.Polygon(polygonStyle);
			overlay.setMap(map);
			path = overlay.getPath();
			var points = $('#id_location').val().split('SRID=900913;POLYGON((')[1].split('))')[0].split(',');
			var latlngbounds = new google.maps.LatLngBounds();
			for (i = 0; i < points.length - 1; i++) {
				var point = points[i].split(" ")
				var p = {'x':point[0] , 'y':point[1]}
				path.insertAt(i, new google.maps.LatLng(p.y, p.x))
				latlngbounds.extend(new google.maps.LatLng(p.y, p.x));
			}
			overlay.setPath(path);
			overlay.setEditable(true);
			drawingManager.setOptions({drawingMode:null});
			addUpdatePathEventListerner()
			map.fitBounds(latlngbounds);
			/*
			google.maps.event.addListener(overlay, 'mouseout', function (e) {
				$(tt).show()
			})
			google.maps.event.addListener(overlay, 'mouseover', function (e) {
				$(tt).hide()
			})
			*/
		};
	};
	getPathFromTextarea();

	var infowindow = new google.maps.InfoWindow({ content: 'Annonce'});
	for (var i = 0; i < homes.length; i++) {
		var p = {'x':homes[i].x , 'y':homes[i].y}
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(p.y, p.x),
            map: map,
            icon: new google.maps.MarkerImage(homes[i].icon)
        });
        marker.html = $('.' + homes[i].id).html()
        google.maps.event.addListener(marker, 'click', function (e) {
            this.setMap(map)
            infowindow.setContent(this.html)
            infowindow.open(map, this);
        });
		/*
		google.maps.event.addListener(marker, 'mouseover', function (e) {
			$(tt).hide();
		})
		google.maps.event.addListener(marker, 'mouseout', function (e) {
			$(tt).show();
		})
		*/
        if(homes[i].visible == 'false'){
            marker.setMap(null)
        }
        homes[i].marker = marker
    }


	$("#address").keypress(function(e) {
   			if (e.which == 13) {
   				return false;
   			}
   	});
	$('#address').focus(function(evt){
		$(this).val('')
	})
	var geocoder = new google.maps.Geocoder();
	$("#center_map").hide()
	$("#center_map").click(function(evt){
		var address = document.getElementById("address").value+' ';
		if (geocoder) {
			geocoder.geocode( { 'address': address, 'region':'FR'}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				var lon = results[0].geometry.location.lng()
				var lat = results[0].geometry.location.lat()
				initialLocation = new google.maps.LatLng(lat,lon);
				map.setCenter(initialLocation);
				map.setZoom(12)
			} 
			else 
			{
				//alert("Geocode was not successful for the following reason: " + status);
			}
		});
		}			
	})
	$('#address').keyup(function(evt){$("#center_map").trigger('click')});
});

add_home = function (x, y, url, id, visible, icon) {
	homes.push({'x': x, 'y': y, 'url': url, 'id': id, 'visible': visible, 'icon':icon});
}

open_popup = function (x, y, id) {
    for (var i = 0; i < homes.length; i++) {
        if (homes[i].id == id) {
            google.maps.event.trigger(homes[i].marker, 'click')
        }
    }
}