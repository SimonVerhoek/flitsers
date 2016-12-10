var Nederland = new google.maps.LatLng(52.13263300000001, 5.2912659999999505);

function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
};

map = new google.maps.Map(document.getElementById('map'), {
	center: Nederland,
	zoom: 8,
	mapTypeId: google.maps.MapTypeId.ROADMAP
});

for (var i = 0; i < flitsers.length; i++) {	
	var lat = flitsers[i].locatie_lat;
	var lng = flitsers[i].locatie_lon;

	if (isNumeric(lat) && isNumeric(lng)) {
		var marker = new google.maps.Marker({
			map: map,
			position: {lat: lat, lng: lng}
		})
	}
	
};