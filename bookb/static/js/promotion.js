$('#form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")
    save();
});


function save(){

    $.ajax({
        type : 'POST',
        url : '',
        data : {'csrfmiddlewaretoken':csrf,'subject':$('#subject').val().trim(),'action':'send_mass_mail','users':$('#user').val()},
        success: function (result) {
            $('#form')[0].reset();
            console.log(result.data);
            alert("Mail sent");
        }
    });
    }