/* map interaction
hold map interaction in home page
1. center map w/ browser location
2. center map w/ user input
*/

localizeMe = function(){
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(position) {
			var latlng = new L.LatLng(position.coords.latitude, position.coords.longitude);
			map.setView(latlng, 13);
		});
	}
};


$(document).ready(function() {
	// prevent return to submit form
	$("#address").keypress(function(e) {
		if (e.which == 13) {
			$("#center_map").trigger('click');
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
		var address = document.getElementById("address").value;
		$.ajax({
			url: "http://nominatim.openstreetmap.org/search/"+address+' ',
			data: {format: 'json', addressdetails:'1', limit:'1', countrycodes:'fr', polygon:'1', json_callback:'jsonpCallback'},
			dataType: 'jsonp',
			jsonp: 'callback',
			jsonpCallback: "jsonpCallback",
			success: function(data){
				var latlng = new L.LatLng(data[0].lat, data[0].lon);
				map.setView(latlng, 13);
				// below, to create a geo for the address search based on nominatin json
				// console.log(L.geoJSON.coordsToLatlngs(data[0].polygonpoints))
			}
		});
		return false;
	});
	//$('#address').keyup(function(evt){$("#center_map").trigger('click');});
});
