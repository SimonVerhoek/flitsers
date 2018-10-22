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
            var flitser = new Flitser(flitsers_today[i]);
            flitser.updateVisibility(yesterday, today);
            flitsers_today_obj.push(flitser);
		}
	}
};


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
		var date_min = moment(date_min).format('YYYY-MM-DD');
		var date_max = moment(date_max).format('YYYY-MM-DD');

		if (this.datum >= date_min && this.datum <= date_max) {
			this.marker.setMap(map);
		} else {
			this.marker.setMap(null);
		}
	};

	this.initMarker();
};
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
	  "				<td>Datum:</td><td>" + moment(this.datum).format('DD-MM-YYYY') + "</td>",
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
};


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
};

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
		var start_str = moment(start).format('YYYY-MM-DD');
		var stop_str = moment(stop).format('YYYY-MM-DD');

		var params = {
			start: start_str,
			stop: stop_str
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
};
