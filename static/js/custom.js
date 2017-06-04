// variables passed by backend
var flitsers_today = flitsers_today;
var first_flitser_date = first_flitser_date;
var datasets = datasets;
var time_slots = time_slots;


var infowindow = new google.maps.InfoWindow();
var sliderElement = $('#slider');

var flitsers = [];
var flitsers_today_obj = [];

var today = {
	start: moment().startOf('day').toDate(),
	stop: moment().endOf('day').toDate(),
	start_backend: moment.utc().startOf('day').toDate(),
	stop_backend: moment.utc().endOf('day').toDate(),
};
var yesterday = {
	start: moment().subtract(1, 'days').startOf('day').toDate(),
	stop: moment().subtract(1, 'days').endOf('day').toDate(),
	start_backend: moment.utc().subtract(1, 'days').startOf('day').toDate(),
	stop_backend: moment.utc().subtract(1, 'days').endOf('day').toDate()
};
var this_week = {
	start: moment().startOf('isoweek').toDate(),
	stop: moment().endOf('isoweek').toDate(),
	start_backend: moment.utc().startOf('isoweek').toDate(),
	stop_backend: moment.utc().endOf('isoweek').toDate(),
}
var last_week = {
	start: moment().subtract(1, 'week').startOf('isoweek').toDate(),
	stop: moment().subtract(1, 'week').endOf('isoweek').toDate(),
	start_backend: moment.utc().subtract(1, 'week').startOf('isoweek').toDate(),
	stop_backend: moment.utc().subtract(1, 'week').endOf('isoweek').toDate(),
}
var this_month = {
	start: moment().startOf('month').toDate(),
	stop: moment().endOf('month').toDate(),
	start_backend: moment.utc().startOf('month').toDate(),
	stop_backend: moment.utc().endOf('month').toDate(),
}
var last_month = {
	start: moment().subtract(1, 'month').startOf('month').toDate(),
	stop: moment().subtract(1, 'month').endOf('month').toDate(),
	start_backend: moment.utc().subtract(1, 'month').startOf('month').toDate(),
	stop_backend: moment.utc().subtract(1, 'month').endOf('month').toDate(),
}
var this_year = {
	start: moment().startOf('year').toDate(),
	stop: moment().endOf('year').toDate(),
	start_backend: moment.utc().startOf('year').toDate(),
	stop_backend: moment.utc().endOf('year').toDate(),
}
var last_year = {
	start: moment().subtract(1, 'year').startOf('year').toDate(),
	stop: moment().subtract(1, 'year').endOf('year').toDate(),
	start_backend: moment.utc().subtract(1, 'year').startOf('year').toDate(),
	stop_backend: moment.utc().subtract(1, 'year').endOf('year').toDate(),
}


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

var TimeChart = {
	ctx: $('#chart'),
	chart: null,
	options: {
    scales: {
      yAxes: [{
        stacked: true
      }]
    }
  },
  init: function() {
		TimeChart.chart = new Chart(TimeChart.ctx, {
		  type: 'bar',
		  data: {
		    labels: time_slots,
		    datasets: datasets
		  },
  		options: TimeChart.options
		});
	},

	update(start, stop) {
		var start = moment(start).format('YYYY-MM-DD');
		var stop = moment(stop).format('YYYY-MM-DD');

		var params = {
			start: start,
			stop: stop
		};
		$.ajax({
			url: '/get_chart_data',
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json;charset=UTF-8',
			data: JSON.stringify(params, null, '\t'),
			success: function(data) {
				TimeChart.chart.config.data.datasets = data.datasets;
				TimeChart.chart.update();
			}
		});
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
		var lower_bound = moment(first_flitser_date).toDate();
		var upper_bound = moment().endOf('day').toDate()

		Slider.init(lower_bound, upper_bound);

		// show today's flitsers on initialisation
		var today = moment().format('YYYY-MM-DD');
		var yesterday = moment().subtract(1, 'day').format('YYYY-MM-DD');	

		// create flitsers
		for (var i = 0; i < flitsers_today.length; i++) {
			if (flitsers_today[i].locatie_lat && flitsers_today[i].locatie_lon) {
				var flitser = new Flitser(flitsers_today[i]);
				flitser.updateVisibility(yesterday, today);
				flitsers_today_obj.push(flitser);
			}
		}
	}
}

var Flitser = function(obj) {
	this.marker = {};

	// get properties of given JSON object
	for (var prop in obj) this[prop] = obj[prop];	

	this.initMarker = function() {
		var latLng = new google.maps.LatLng(this.locatie_lat, this.locatie_lon);
		var marker = new google.maps.Marker({
			position: latLng
		});

		var content = this.getContent();

		google.maps.event.addListener(marker, 'click', function(){
	    infowindow.close();
	    infowindow.setContent( content );
	    infowindow.open(map, marker);
	  });

	  this.marker = marker;
	};

	this.updateVisibility = function(date_min, date_max) {
		if (this.datum > date_min && this.datum <= date_max) {
			this.marker.setMap(map);
		} else {
			this.marker.setMap(null);
		}
	};

	this.initMarker();
}
Flitser.prototype.getContent = function() {
	var weather_conditions = 'Onbekend';
	if (this.weer_beschrijving != null && this.weer_temp != null) {
		weather_conditions = this.weer_beschrijving + ", " + this.weer_temp + "&deg;C";
	}

	var last_activity = 'Onbekend';
	if (this.laatste_activiteit != null) {
		last_activity = this.laatste_activiteit.substring(0, 8)
	}

	var content = [
	  "<div id='InfoWindow'>",
	  "	<table id='InfoWindow-table'>",
	  "		<tbody>",
	  "			<tr>",
	  "				<td>Datum:</td><td>" + this.datum + "</td>",
	  "			</tr>",
	  "			<tr>",
	  "				<td>Type this:</td><td>" + this.type_controle + "</td>",
	  "			</tr>",
	  "			<tr>",
	  "				<td>Locatie:</td><td>" + this.wegnummer + " (" + this.soort_weg + "), hectometerpaal " + this.hm_paal + "</td>",
	  "			</tr>",
	  "			<tr>",
	  "				<td>Activiteit:</td><td>van " + this.tijd_van_melden + " tot " + last_activity + "</td>",
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

function create_markers(flitsers_list) {
	for (var i = 0; i < flitsers_list.length; i++) {
		if (flitsers_list[i].locatie_lat && flitsers_list[i].locatie_lon) {
			var flitser = new Flitser( flitsers_list[i] );
			flitsers.push(flitser);
		}
	}
}


$(document).ready(function() {
	GMap.init();
	TimeChart.init();

	// get all flitsers
	$.ajax({
		url: '/get_flitser_data',
		type: 'GET',
		dataType: 'json',
		success: function(data) {
			create_markers(data.flitsers);
		}
	});
	
	// update markers show
	$('#slider').bind("valuesChanged", function(e, data) {
		var date_min = data.values.min;
		var date_max = data.values.max;
		
		for (i = 0; i < flitsers.length; i++) {
			if (flitsers[i].marker) {
				flitsers[i].updateVisibility(date_min, date_max);
			}
		};

		TimeChart.update(date_min, date_max);
	});

	// remove flitsers passed on initial load
	$('button').click(function() {
		for (i = 0; i < flitsers_today_obj.length; i++) {
			flitsers_today_obj[i].marker.setMap(null);
		}
	});

	// set buttons
	$('#today').on('click', function() {
		Slider.update(today.start, today.stop);
	});

	$('#yesterday').on('click', function() {
		Slider.update(yesterday.start, yesterday.stop);
	});

	$('#this_week').on('click', function() {
		Slider.update(this_week.start, this_week.stop);
	});

	$('#last_week').on('click', function() {
		Slider.update(last_week.start, last_week.stop);
	});

	$('#this_month').on('click', function() {
		Slider.update(this_month.start, this_month.stop);
	});

	$('#last_month').on('click', function() {
		Slider.update(last_month.start, last_month.stop);
	});

	$('#this_year').on('click', function() {
		Slider.update(this_year.start, this_year.stop);
	});

	$('#last_year').on('click', function() {
		Slider.update(last_year.start, last_year.stop);
	});

});