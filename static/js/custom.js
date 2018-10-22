var infowindow = new google.maps.InfoWindow();
var sliderElement = $('#slider');

var flitsers = [];
var flitsers_today_obj = [];

var today = {
	name: '#today',
	start: moment().startOf('day').toDate(),
	stop: moment().endOf('day').toDate(),
	start_backend: moment.utc().startOf('day').toDate(),
	stop_backend: moment.utc().endOf('day').toDate(),
};
var yesterday = {
	name: '#yesterday',
	start: moment().subtract(1, 'days').startOf('day').toDate(),
	stop: moment().subtract(1, 'days').endOf('day').toDate(),
	start_backend: moment.utc().subtract(1, 'days').startOf('day').toDate(),
	stop_backend: moment.utc().subtract(1, 'days').endOf('day').toDate()
};
var this_week = {
	name: '#this_week',
	start: moment().startOf('isoweek').toDate(),
	stop: moment().endOf('isoweek').toDate(),
	start_backend: moment.utc().startOf('isoweek').toDate(),
	stop_backend: moment.utc().endOf('isoweek').toDate(),
}
var last_week = {
	name: '#last_week',
	start: moment().subtract(1, 'week').startOf('isoweek').toDate(),
	stop: moment().subtract(1, 'week').endOf('isoweek').toDate(),
	start_backend: moment.utc().subtract(1, 'week').startOf('isoweek').toDate(),
	stop_backend: moment.utc().subtract(1, 'week').endOf('isoweek').toDate(),
}
var this_month = {
	name: '#this_month',
	start: moment().startOf('month').toDate(),
	stop: moment().endOf('month').toDate(),
	start_backend: moment.utc().startOf('month').toDate(),
	stop_backend: moment.utc().endOf('month').toDate(),
}
var last_month = {
	name: '#last_month',
	start: moment().subtract(1, 'month').startOf('month').toDate(),
	stop: moment().subtract(1, 'month').endOf('month').toDate(),
	start_backend: moment.utc().subtract(1, 'month').startOf('month').toDate(),
	stop_backend: moment.utc().subtract(1, 'month').endOf('month').toDate(),
}
var this_year = {
	name: '#this_year',
	start: moment().startOf('year').toDate(),
	stop: moment().endOf('year').toDate(),
	start_backend: moment.utc().startOf('year').toDate(),
	stop_backend: moment.utc().endOf('year').toDate(),
}
var last_year = {
	name: '#last_year',
	start: moment().subtract(1, 'year').startOf('year').toDate(),
	stop: moment().subtract(1, 'year').endOf('year').toDate(),
	start_backend: moment.utc().subtract(1, 'year').startOf('year').toDate(),
	stop_backend: moment.utc().subtract(1, 'year').endOf('year').toDate(),
}
var buttons = [
	today, yesterday, this_week, last_week, 
	this_month, last_month, this_year, last_year
];


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

	function setButtonEvent(button_obj) {
		return function() {
			Slider.update(button_obj.start, button_obj.stop)	
		}
	}

	for (var i = 0; i < buttons.length; i++) {
		var button = buttons[i];
		$(button.name).on('click', setButtonEvent(button))
	}
});
