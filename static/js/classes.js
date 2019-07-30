const GMap = {
	map: {},

	init() {
		const Nederland = new google.maps.LatLng(52.13263300000001, 5.2912659999999505);

		this.map = new google.maps.Map(document.getElementById('map'), {
			center: Nederland,
			zoom: 8,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		});

		this.infowindow = new google.maps.InfoWindow();

		// create flitsers
		for (let i = 0; i < flitsers_today.length; i++) {
			const flitser = new Flitser(flitsers_today[i]);
			flitsers_today_obj.push(flitser);
		}
	}
};


class Flitser {
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
			weather_conditions = this.weer_beschrijving + ", " + this.weer_temp + "&deg;C";
		}

		let last_activity = 'Onbekend';
		if (this.laatste_activiteit != null) {
			last_activity = this.laatste_activiteit.substring(0, 8)
		}

		const content = [
			"<div id='InfoWindow'>",
			"	<table id='InfoWindow-table'>",
			"		<tbody>",
			"			<tr>",
			"				<td>Datum:</td><td>" + moment(this.datum).format('DD-MM-YYYY') + "</td>",
			"			</tr>",
			"			<tr>",
			"				<td>Type:</td><td>" + this.type_controle + "</td>",
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
}


const Slider = {
	elem: $('#slider'),

	init(lower_bound, upper_bound) {
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
	ctx: $('#chart'),
	chart: null,
	options: {
		scales: {
			yAxes: [{
				stacked: true
			}]
		}
	},

	init() {
		this.chart = new Chart(this.ctx, {
			type: 'bar',
			data: {
				labels: time_slots,
				datasets: datasets
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
	constructor(elem, unit, subtract_type = 'days', subtract = 0) {
		this.elem = elem;
		this.start = moment().subtract(subtract, subtract_type).startOf(unit).toDate();
		this.stop = moment().subtract(subtract, subtract_type).endOf(unit).toDate();
	}
}
