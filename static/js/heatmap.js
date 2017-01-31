function setContent(flitser) {
	var weather_conditions = 'Onbekend';
	if (flitser.weer_beschrijving != null && flitser.weer_temp != null) {
		weather_conditions = flitser.weer_beschrijving + ", " + flitser.weer_temp + "&deg;C";
	}

	var last_activity = 'Onbekend';
	if (flitser.laatste_activiteit != null) {
		last_activity = flitser.laatste_activiteit.substring(0, 8)
	}

	var content = [
	  "<div id='InfoWindow'>",
	  "	<table id='InfoWindow-table'>",
	  "		<tbody>",
	  "			<tr>",
	  "				<td>Datum:</td><td>" + flitser.datum + "</td>",
	  "			</tr>",
	  "			<tr>",
	  "				<td>Type flitser:</td><td>" + flitser.type_controle + "</td>",
	  "			</tr>",
	  "			<tr>",
	  "				<td>Locatie:</td><td>" + flitser.wegnummer + " (" + flitser.soort_weg + "), hectometerpaal " + flitser.hm_paal + "</td>",
	  "			</tr>",
	  "			<tr>",
	  "				<td>Activiteit:</td><td>van " + flitser.tijd_van_melden + " tot " + last_activity + "</td>",
	  "			</tr>",
	  "			<tr>",
	  "				<td>Weer:</td><td>" + weather_conditions + "</td>",
	  "			</tr>",
	  "		</tbody>",
	  "	</table>",
	  "</div>"
	].join("\n");

	return content;
}

function initMap() {
	var Nederland = new google.maps.LatLng(52.13263300000001, 5.2912659999999505);

	map = new google.maps.Map(document.getElementById('map'), {
		center: Nederland,
		zoom: 8,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});

	for (var i = 0; i < flitsers_today.length; i++) {	
		var lat = flitsers_today[i].locatie_lat;
		var lng = flitsers_today[i].locatie_lon;

		if (lat && lng) {
			var marker = new google.maps.Marker({
				position: {lat: lat, lng: lng}
			});

			marker.setMap(map);
		}
	};

	// show today's flitsers on initialisation
	var currentDate = new Date();
	var today = currentDate.toJSON().slice(0, 10);

	// init slider bar
	$('#slider').dateRangeSlider({
		bounds: {
			min: new Date(flitsers[0].datum),
			max: currentDate,
		},
		defaultValues: {
			min: currentDate,
			max: currentDate,
		}
	});
}

function createMarker(flitser, infowindow) {
	var latLng = new google.maps.LatLng(flitser.locatie_lat, flitser.locatie_lon);
	var marker = new google.maps.Marker({
		position: latLng
	});

  google.maps.event.addListener(marker, 'click', function(){
      infowindow.close();
      infowindow.setContent( setContent(flitser) );
      infowindow.open(map, marker);
  });

	flitser.marker = marker;
}

function updateMarkerVisibility(flitser, date_min, date_max) {
	if (flitser.datum >= date_min && flitser.datum <= date_max) {
		flitser.marker.setMap(map);
	} else {
		flitser.marker.setMap(null);
	}
}


$(document).ready(function() {
	initMap();

	var infowindow = new google.maps.InfoWindow();

	// create markers
	for (var i = 0; i < flitsers.length; i++) {
		if (flitsers[i].locatie_lat && flitsers[i].locatie_lon) {
			createMarker( flitsers[i], infowindow );
		}
	}

	// update markers shown
	$('#slider').bind("valuesChanged", function(e, data) {
		var date_min = data.values.min.toJSON().slice(0, 10);
		var date_max = data.values.max.toJSON().slice(0, 10);
		
		for (i = 0; i < flitsers.length; i++) {
			if (flitsers[i].marker) {
				updateMarkerVisibility( flitsers[i], date_min, date_max );
			}
		}

	})
});