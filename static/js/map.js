var infowindow = new google.maps.InfoWindow();
var sliderElement = $('#slider');

var Slider = {
	init: function(lower_bound, upper_bound) {
		$(sliderElement).dateRangeSlider({
			bounds: {
				min: lower_bound,
				max: upper_bound,
			},
			defaultValues: {
				min: upper_bound,
				max: upper_bound,
			}
		});
	},

	update: function(lower_bound, upper_bound) {
		$(sliderElement).dateRangeSlider('values', lower_bound, upper_bound);
	}
}

var GMap = {
	init: function() {
		var Nederland = new google.maps.LatLng(52.13263300000001, 5.2912659999999505);

		map = new google.maps.Map(document.getElementById('map'), {
			center: Nederland,
			zoom: 8,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		});

		// init slider bar
		var lower_bound = new Date(first_flitser_date);
		var upper_bound = moment(today);
		Slider.init(lower_bound, upper_bound);

		// show today's flitsers on initialisation
		var today = moment().format('YYYY-MM-DD');
		var yesterday = moment().subtract(1, 'day').format('YYYY-MM-DD');	

		// create markers
		for (var i = 0; i < flitsers_today.length; i++) {
			if (flitsers_today[i].locatie_lat && flitsers_today[i].locatie_lon) {
				Marker.init( flitsers_today[i], infowindow );
				Marker.updateVisibility(flitsers_today[i], yesterday, today)
			}
		}
	}
}

var Marker = {
	init: function(flitser, infowindow) {
		var latLng = new google.maps.LatLng(flitser.locatie_lat, flitser.locatie_lon);
		var marker = new google.maps.Marker({
			position: latLng
		});

	  google.maps.event.addListener(marker, 'click', function(){
	    infowindow.close();
	    infowindow.setContent( getContent(flitser) );
	    infowindow.open(map, marker);
	  });

		flitser.marker = marker;
	},

	updateVisibility: function(flitser, date_min, date_max) {
		if (flitser.datum > date_min && flitser.datum <= date_max) {
			flitser.marker.setMap(map);
		} else {
			flitser.marker.setMap(null);
		}
	}
}

function getContent(flitser) {
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


$(document).ready(function() {
	GMap.init();

	var flitsers;

	// get all flitsers
	$.ajax({
		url: '/get_all_flitsers',
		type: 'GET',
		dataType: 'json',
		data: { get_param: 'value' },
		success: function(data) {
			flitsers = data;
			// create markers
			for (var i = 0; i < data.length; i++) {
				if (data[i].locatie_lat && data[i].locatie_lon) {
					Marker.init( data[i], infowindow );
				}
			}
		}
	});
	
	// update markers show
	$('#slider').bind("valuesChanged", function(e, data) {
		var date_min = data.values.min.toJSON().slice(0, 10);
		var date_max = data.values.max.toJSON().slice(0, 10);
		
		for (i = 0; i < flitsers.length; i++) {
			if (flitsers[i].marker) {
				Marker.updateVisibility( flitsers[i], date_min, date_max );
			}
		}
	});

});

$(document).ajaxComplete(function(event, xhr, settings) {
	var todayStart = moment().startOf('day').toDate();
	var todayEnd = moment().endOf('day').toDate();

	var yesterdayStart = moment().subtract(1, 'days').startOf('day').toDate();
	var yesterdayEnd = moment().subtract(1, 'days').endOf('day').toDate();

	var startOfWeek = moment().startOf('isoweek').toDate();
	var endOfWeek = moment().endOf('isoweek').toDate();

	var startOfLastWeek = moment().subtract(1, 'week').startOf('isoweek').toDate();
	var endOfLastWeek = moment().subtract(1, 'week').endOf('isoweek').toDate();
	
	var startOfMonth = moment().startOf('month').toDate();
	var endOfMonth = moment().endOf('month').toDate();

	var startOfLastMonth = moment().subtract(1, 'month').startOf('month').toDate();
	var endOfLastMonth = moment().subtract(1, 'month').endOf('month').toDate();

	var startOfYear = moment().startOf('year').toDate();
	var endOfYear = moment().endOf('year').toDate();

	var startOfLastYear = moment().subtract(1, 'year').startOf('year').toDate();
	var endOfLastYear = moment().subtract(1, 'year').endOf('year').toDate();
	
	$('#today').on('click', function() {
		Slider.update(todayStart, todayEnd);
	});

	$('#yesterday').on('click', function() {
		Slider.update(yesterdayStart, yesterdayEnd);
	});

	$('#this_week').on('click', function() {
		Slider.update(startOfWeek, endOfWeek);
	});

	$('#last_week').on('click', function() {
		Slider.update(startOfLastWeek, endOfLastWeek);
	});

	$('#this_month').on('click', function() {
		Slider.update(startOfMonth, endOfMonth);
	});

	$('#last_month').on('click', function() {
		Slider.update(startOfLastMonth, endOfLastMonth);
	});

	$('#this_year').on('click', function() {
		Slider.update(startOfYear, endOfYear);
	});

	$('#last_year').on('click', function() {
		Slider.update(startOfLastYear, endOfLastYear);
	});
});