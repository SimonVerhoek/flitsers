var heatmapData = [];

for (var i = 0; i < flitsers.length; i++) {
	var flitser = new google.maps.LatLng(
		flitsers[i].locatie_lat, 
		flitsers[i].locatie_lon
	);
	heatmapData.push(flitser);
};

var Nederland = new google.maps.LatLng(52.13263300000001, 5.2912659999999505);
var gradient = [
	'rgba(255,204,204, 0)',
	'rgba(255,153,153, 1)',
	'rgba(255,102,102, 1)',
	'rgba(255,51,51, 1)',
	'rgba(255,0,0, 1)',
	'rgba(204,0,0, 1)',
	'rgba(153,0,0, 1)',
	'rgba(102,0,0, 1)',
];

map = new google.maps.Map(document.getElementById('map'), {
	center: Nederland,
	zoom: 8,
	mapTypeId: google.maps.MapTypeId.ROADMAP
});

var heatmap = new google.maps.visualization.HeatmapLayer({
	data: heatmapData
});
heatmap.setMap(map);
heatmap.set('radius', 60);
heatmap.set('dissipating', true);
heatmap.set('gradient', gradient);
heatmap.set('opacity', 0.7);