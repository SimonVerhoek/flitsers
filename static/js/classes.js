moment.locale('nl');

const GMap = {
	map: {},
	speeding_cams: [],
	coordinates: [52.13263300000001, 5.2912659999999505],

	init(elem) {
		this.elem = elem;

		this.map = L.map(this.elem.id).setView(this.coordinates, 8);

		L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
			attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
			maxZoom: 18,
			id: 'mapbox/streets-v11',
			tileSize: 512,
			zoomOffset: -1,
			accessToken: backendData.mapbox_access_token
		}).addTo(this.map);

		for (let item of backendData.todays_speed_cams) {
			if (item.locatie_lat != null && item.locatie_lon != null) {
				const speeding_cam = new SpeedingCam(item);
				this.speeding_cams.push(speeding_cam)
			}
		}
	},

	updateSpeedingCamsOnMap(date_min, date_max) {
		const _this = this;

		for (let speeding_cam of _this.speeding_cams) {
			GMap.map.removeLayer(speeding_cam.marker)
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

		if (this.locatie_lat != null && this.locatie_lon != null) {
			const marker = L.marker([this.locatie_lat, this.locatie_lon]).addTo(GMap.map)

			const content = this.getContent();
			marker.bindPopup(content);

			this.marker = marker;
		}
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
			},
			formatter: (date_obj) => this.changeDateFormat(date_obj)
		});
	},

	changeDateFormat(date_obj) {
		const day_name = moment(date_obj).format('ddd');
		const day = date_obj.getDate();
		const month = moment.monthsShort()[date_obj.getMonth()];
		const year = date_obj.getFullYear();
		return `${day_name} ${day} ${month} ${year}`;
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
