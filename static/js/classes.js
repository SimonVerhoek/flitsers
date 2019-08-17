const GMap = {
	map: {},
	speeding_cams: [],
	coordinates: [52.13263300000001, 5.2912659999999505],

	init(elem) {
		const Nederland = new google.maps.LatLng(...this.coordinates);

		this.elem = elem;
		this.map = new google.maps.Map(this.elem, {
			center: Nederland,
			zoom: 8,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		});

		this.infowindow = new google.maps.InfoWindow();

		for (let item of backendData.todays_speed_cams) {
			const speeding_cam = new SpeedingCam(item);
			this.speeding_cams.push(speeding_cam)
		}
	},

	updateSpeedingCamsOnMap(date_min, date_max) {
		const _this = this;

		for (let speeding_cam of _this.speeding_cams) {
			speeding_cam.marker.setMap(null);
		}
		_this.speeding_cams.length = 0;

		backendData.getSpeedingCamData(date_min, date_max)
			.then(data => {
				const new_speeding_cams = data.speeding_cams;
				for (let item of new_speeding_cams) {
					if (item.locatie_lat && item.locatie_lon) {
						const new_speeding_cam = new SpeedingCam(item);
						_this.speeding_cams.push(new_speeding_cam)
					}
				}

				TimeChart.update(data.datasets);
			})
			.catch(err => console.log(err));
	}
};


class SpeedingCam {
	constructor(obj) {
		// get properties of given JSON object
		Object.assign(this, obj);

		const marker = new google.maps.Marker({
			position: new google.maps.LatLng(this.locatie_lat, this.locatie_lon),
			map: GMap.map
		});

		const content = this.getContent();

		marker.addListener('click', function () {
			GMap.infowindow.close();
			GMap.infowindow.setContent(content);
			GMap.infowindow.open(GMap.map, marker);
		});

		this.marker = marker;
	}

	getContent() {
		let weather_conditions = 'Onbekend';
		if (this.weer_beschrijving != null && this.weer_temp != null) {
			weather_conditions = `${this.weer_beschrijving}, ${this.weer_temp}&deg;C`;
		}

		let last_activity = 'Onbekend';
		if (this.laatste_activiteit != null) {
			last_activity = this.laatste_activiteit.substring(0, 8)
		}

		return `
			<div id='InfoWindow'>
				<table id='InfoWindow-table'>
					<tbody>
						<tr>
							<td>Datum:</td><td>${moment(this.datum).format('DD-MM-YYYY')}</td>
						</tr>
						<tr>
							<td>Type:</td><td>${this.type_controle}</td>
						</tr>
						<tr>
							<td>Locatie:</td><td>${this.wegnummer} (${this.soort_weg}), hectometerpaal ${this.hm_paal}</td>
						</tr>
						<tr>
							<td>Activiteit:</td><td>van  ${this.tijd_van_melden} tot ${last_activity}</td>
						</tr>
						<tr>
							<td>Weer:</td><td>${weather_conditions}</td>
						</tr>
					</tbody>
				</table>
			</div>
		`;
	}
}


const Slider = {
	init(obj, lower_bound, upper_bound) {
		this.elem = obj;

		this.elem.dateRangeSlider({
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

	update(lower_bound, upper_bound) {
		this.elem.dateRangeSlider('values', lower_bound, upper_bound);
	}
};


const TimeChart = {
	chart: null,
	options: {
		scales: {
			yAxes: [{
				stacked: true
			}]
		}
	},

	init(obj) {
		this.ctx = obj;
		this.chart = new Chart(this.ctx, {
			type: 'bar',
			data: {
				labels: backendData.time_slots,
				datasets: backendData.datasets
			},
			options: this.options
		});
	},

	update(datasets) {
		this.chart.config.data.datasets = datasets;
		this.chart.update();
	}
};


class PeriodButton {
	constructor(elem, unit, subtract_type, subtract = 0) {
		this.elem = elem;
    this.unit = unit;
    this.subtract = subtract;
		this.start = moment().subtract(subtract, `${unit}s`).startOf(unit).toDate();
		this.stop = moment().subtract(subtract, `${unit}s`).endOf(unit).toDate();
	};
}
