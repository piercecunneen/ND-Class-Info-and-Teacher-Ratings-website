var typingTimer;
var doneTypingInterval = 500;

$("#searchForm").keyup(function(e) {
	clearTimeout(typingTimer);
	if ($('#myInput').val) {
		typingTimer = setTimeout(doneTyping, doneTypingInterval);
	}
});

function doneTyping(e) {

	// Select the results list and clear its entries
	var list = document.getElementById('ResultList');
	while(list.firstChild) {
		list.removeChild(list.firstChild);
	}

	var url = "/search/" + document.getElementById('search').value + "/";
	$.ajax({
		type: "POST",
		url: url,
		data: {},
		contentType: 'application/json;charset=UTF-8',
		success: function(data)
		{
			var queryCount = 0;
			$.each(data, function(professorName, professorUrl) {
				if(queryCount++ < 5) {
					var link = document.createElement("a");
					link.setAttribute("class", "collection-item");
					link.setAttribute("href", professorUrl);
					link.appendChild(document.createTextNode(professorName));
					list.appendChild(link);
				}
			});
			// hide ul if no elements
			if(!list.firstChild) {
				list.style.display = 'None';
			} else {
				list.style.display = 'block';
			}
		},
		error: function(data)
		{
			list.style.display='None';
		}
	});
}
