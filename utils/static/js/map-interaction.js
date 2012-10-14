/* map interaction
hold map interaction in home page
1. center map w/ browser location
2. center map w/ user input
*/

localizeMe = function(){
	$("#localize").button('loading');
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position) {
			$("#localize").button('reset');
			var latlng = new L.LatLng(position.coords.latitude, position.coords.longitude);
			map.setView(latlng, 13);
		});
	}else{
		$("#localize").button('reset');
	}
};


$(document).ready(function() {
	// prevent return to submit form
	$("#address").keypress(function(e) {
		if (e.which == 13) {
			$("#center_map").trigger('click');
			$(this).blur();
			return false;
		}
	});
	// init input each time focus is in
	/*$('#address').focus(function(evt){
		$(this).val('');
	});*/
	// js geocode location to center the map on user input address
	// use nominatim webservice w/ jsonp callback
	$("#center_map").click(function(evt){
		$(this).button('loading');
		var address = document.getElementById("address").value;
		var self = this;
		$.ajax({
			url: "http://nominatim.openstreetmap.org/search/"+address+' ',
			data: {format: 'json', addressdetails:'1', limit:'1', countrycodes:'fr', polygon:'1', json_callback:'jsonpCallback'},
			dataType: 'jsonp',
			jsonp: 'callback',
			jsonpCallback: "jsonpCallback",
			success: function(data){
				$(self).button('reset');
				if(data.length > 0){
					// result
					var latlng = new L.LatLng(data[0].lat, data[0].lon);
					map.setView(latlng, 13);
				}else{
					// no results
					$("#address").attr('placeholder', 'adresse erronée').val('')
				}
				// below, to create a geo for the address search based on nominatin json
				// console.log(L.geoJSON.coordsToLatlngs(data[0].polygonpoints))
			}
		});
		return false;
	});
	//$('#address').keyup(function(evt){$("#center_map").trigger('click');});
});
