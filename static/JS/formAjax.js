$(function() {
    $('#modal-form').submit(function(e) {
		  e.preventDefault();
		  var number = document.getElementById('phone_number').value
		  var crn = document.getElementById('modal-crn').value
		  var url = '/alert/' + number + '/' + crn + '/';
        $.ajax({
            type: 'POST',
            url: url,
            data: {},
            success: function(response) {
					 Materialize.toast('success: check your phone for a text', 4000) },
            error: function(error) {
                console.log("error: " + error);
					 Materialize.toast('error: invalid crn or phone number', 4000)
            }
        });
    });
});
