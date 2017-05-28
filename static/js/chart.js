function drawChart(labels, chart_data) {
	var ctx = $('#chart');
	var myChart = new Chart(ctx, {
	  type: 'bar',
	  data: {
	    labels: labels,
	    datasets: [{
	      label: 'Radar',
	      data: chart_data.Radar,
	      backgroundColor: "rgba(153,255,51,0.4)"
	    }, {
	      label: 'Laser',
	      data: chart_data.Laser,
	      backgroundColor: "rgba(255,153,0,0.4)"
	    }, {
	      label: 'ANPR',
	      data: chart_data.ANPR,
	      backgroundColor: "rgba(7,5,6,0.4)"
	    }]
	  },
	  options: {
	    scales: {
	      yAxes: [{
	        stacked: true
	      }]
	    }
	  }
	});
}



$(document).ready(function() {
	// get chart data
	$.ajax({
		url: '/get_chart_data',
		type: 'GET',
		dataType: 'json',
		success: function(data) {
			var time_slots = data.time_slots;
			var chart_data = data.flitser_count_per_time_slot;

			drawChart(time_slots, chart_data);
		}
	});
});