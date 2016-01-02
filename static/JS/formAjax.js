$(function() {
    $('#modal-form').submit(function(e) {
        e.preventDefault();
        var number = document.getElementById('phone_number').value
        var crn = document.getElementById('modal-crn').value
        if(number.length == 10) {
            var url = '/alert/' + crn + '/' + number + '/';
            $.ajax({
                type: 'POST',
                url: url,
                data: {},
                success: function(response) {
                     Materialize.toast(response, 4000)
                },
                error: function(error) {
                     console.log("error: " + error);
                     Materialize.toast(error, 4000);
                }
            });
        } else {
            Materialize.toast('Number must be 10 digits long', 4000)
        }
    });
});
