const flitsers = [];
const flitsers_today_obj = [];
const date_format_str = 'YYYY-MM-DD';


function create_markers(flitsers_list) {
	for (let i = 0; i < flitsers.length; i++) {
		flitsers[i].marker.setMap(null);
	}
	flitsers.length = 0;

	for (let j = 0; j < flitsers_list.length; j++) {
		if (flitsers_list[j].locatie_lat && flitsers_list[j].locatie_lon) {
			const flitser = new Flitser( flitsers_list[j] );
			flitsers.push(flitser);
		}
	}
}


function get_flitsers(date_min, date_max) {
	$.ajax({
		url: '/get_chart_data',
		type: 'POST',
		dataType: 'json',
		contentType: 'application/json',
		data: JSON.stringify({start: date_min, stop: date_max}),
		success: function(data) {
			create_markers(data.flitsers);
			TimeChart.update(data.datasets);
		}
	});
}

function remove_initial_markers() {
	// remove flitsers passed on initial load
	for (i = 0; i < flitsers_today_obj.length; i++) {
		flitsers_today_obj[i].marker.setMap(null);
	}
	flitsers_today_obj.length = 0;
}


$(document).ready(function() {
	GMap.init();
	TimeChart.init();

	const lower_bound = moment(first_flitser_date).toDate();
	const upper_bound = moment().endOf('day').toDate();
	Slider.init(lower_bound, upper_bound);

	// update markers shown
	Slider.elem.bind('valuesChanged', function(e, data) {
		TimeChart.update(data.values.min, data.values.max);

		const date_min_backend = moment(data.values.min).format(date_format_str);
		const date_max_backend = moment(data.values.max).format(date_format_str);

		get_flitsers(date_min_backend, date_max_backend)
	});

	[...$('button.period_button')].forEach(function (e) {
		const button = new PeriodButton(
			elem = $(e),
			unit = e.dataset.unit,
			subtract_type = e.dataset.subtract_type,
			subtract = e.dataset.subtract
		);

		button.elem.on('click', function () {
			if (flitsers_today_obj.length > 0) {
				remove_initial_markers();
			}

			Slider.update(button.start, button.stop)
		})
	});

	const today_start = moment.utc().startOf('day').format(date_format_str);
	const today_stop = moment.utc().endOf('day').format(date_format_str);

	get_flitsers(today_start, today_stop);
});
