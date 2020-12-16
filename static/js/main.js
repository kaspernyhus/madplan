function googleAuthenticate(){ 
	$.ajax({ 
		type: "GET", 
		url: "ajax/bookings/googleAuthenticate", 
		// data: '', 
		success: function (data) { 
			console.log('Done') 
		} 
	}); 
}; 
