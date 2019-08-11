$(document).ready(function() {
	GMap.init();
	TimeChart.init();

	const lower_bound = moment(backendData.first_speed_cam_date).toDate();
	const upper_bound = moment().endOf('day').toDate();

	Slider.init(lower_bound, upper_bound);

	// update markers shown
	Slider.elem.bind('valuesChanged', function(e, data) {
		TimeChart.update(data.values.min, data.values.max);

		const date_format_str = 'YYYY-MM-DD';
		const date_min_backend = moment(data.values.min).format(date_format_str);
		const date_max_backend = moment(data.values.max).format(date_format_str);

    GMap.updateSpeedingCamsOnMap(date_min_backend, date_max_backend)
	});

	[...$('button.period_button')].forEach(function (e) {
		const button = new PeriodButton(
			elem = $(e),
			unit = e.dataset.unit,
			subtract_type = e.dataset.subtract_type,
			subtract = e.dataset.subtract
		);

		button.elem.on('click', function () {
			Slider.update(button.start, button.stop)
		})
	});
});
