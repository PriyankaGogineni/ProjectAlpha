$(document).ready(function() {
	var endpoint = 'us-east-2:152196704760:project/GreenCount/1676441484321.execute-api.us-east-1.amazonaws.com/prod/trashcount';
	
	$.get(endpoint, function(data, status) {
		if (status === 'success') {
			$('#glassCount').text(data.glass);
			$('#plasticCount').text(data.plastic);
			$('#paperCount').text(data.paper);
			$('#metalCount').text(data.metal);
		} else {
			console.error('Failed to get trash count data');
		}
	});
});
