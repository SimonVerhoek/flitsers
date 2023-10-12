$(document).ready(function() {
	SpeedCamMap.init( document.getElementById('map') );
	TimeChart.init( $('#chart') );

	const lower_bound = moment(new Date(backendData.first_speed_cam_date)).toDate();
	const upper_bound = moment().endOf('day').toDate();

	Slider.init($('#slider'), lower_bound, upper_bound);

	// update markers shown
	Slider.elem.bind('valuesChanged', (e, data) => {
		TimeChart.update(data.values.min, data.values.max);

		const date_format_str = 'YYYY-MM-DD';
		const date_min_backend = moment(data.values.min).format(date_format_str);
		const date_max_backend = moment(data.values.max).format(date_format_str);

    SpeedCamMap.updateSpeedingCamsOnMap(date_min_backend, date_max_backend)
	});

	[...$('button.period_button')].forEach((e) => {
		const button = new PeriodButton(
			elem = $(e),
			unit = e.dataset.unit,
			subtract_type = e.dataset.subtract_type,
			subtract = e.dataset.subtract
		);

		button.elem.on('click', () => Slider.update(button.start, button.stop))
	});
});
