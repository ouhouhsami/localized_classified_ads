
var source = new Proj4js.Proj('EPSG:4326');    
var dest = new Proj4js.Proj('EPSG:900913');  

$(function(){
	var options = {
		zoom: 15,
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

	var marker = new google.maps.Marker({
		map: map,
		title:"Annonce",
		icon: new google.maps.MarkerImage('/static/img/home.png')
	});

	var geocoder = new google.maps.Geocoder();
	$("#center_map").hide()

	$("#center_map").click(function(evt){
		var address = document.getElementById("address").value+' ';
			if (geocoder) {
				geocoder.geocode( { 'address': address, 'region':'FR'}, function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					$('#id_address').val(JSON.stringify(results[0]['address_components']))
					var lon = results[0].geometry.location.lng()
					var lat = results[0].geometry.location.lat()
					var latlon = new google.maps.LatLng(lat, lon)
					marker.setPosition(latlon)
					map.setCenter(latlon)
					var p = new Proj4js.Point(lon, lat);
					Proj4js.transform(source, dest, p);  
					$('#id_location').val('POINT('+p.x+' '+p.y+')')
				} 
			else{
				//alert("Geocode was not successful for the following reason: " + status);
			}
		});
		}			
	})

	$("#address").keypress(function(e) {
		if (e.which == 13) {
			return false; 
		}
    });
	$('#address').keyup(function(evt){$("#center_map").trigger('click')})
	
	if($('#id_location').val() != ''){
		var point = $('#id_location').val().split('(')[1].split(')')[0].split(' ')
		var p = new Proj4js.Point(point[0], point[1]);
		Proj4js.transform(dest, source, p); 
		var latlon = new google.maps.LatLng(p.y, p.x)
		marker.setPosition(latlon)
		map.setCenter(latlon)
		/* for reverse geocoding
		geocoder.geocode({'latLng': latlon}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				$('#address').val(results[0].formatted_address)
			}
		});
		*/
	}
})