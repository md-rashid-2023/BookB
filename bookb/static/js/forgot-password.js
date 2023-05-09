
$('#form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")
    save();
});


function save(){

$.ajax({
    type : 'POST',
    url : '',
    data : {'csrfmiddlewaretoken':csrf,'email':$('#email').val().trim(),'action':'forgot-password'},
    success: function (result) {
        let div_otp = document.getElementById('div_otp');
        let send_otp = document.getElementById('send-otp');
        send_otp.style.display = 'none';
        let verify_otp = document.getElementById('verify-otp');
        verify_otp.style.display = 'block';
        div_otp.style.display = 'block';

    }
});
}

$('#verify-form').on('submit', function(event){
    event.preventDefault();
    console.log("Verify form submitted!")
    verify();
});

function verify(){

    $.ajax({
        type : 'POST',
        url : '',
        data : {'csrfmiddlewaretoken':csrf,'email':$('#email').val().trim(),'otp':$('#otp').val().trim(),'action':'verify-otp'},
        success: function (result) {
        $('#verify-form')[0].reset();
            let div_otp = document.getElementById('div_otp');
            let send_otp = document.getElementById('send-otp');
            send_otp.style.display = 'none';
            let verify_otp = document.getElementById('verify-otp');
            verify_otp.style.display = 'block';
            div_otp.style.display = 'block';
            if (result.is_verified){
                verify_otp.innerHTML = 'OTP Verified';
                document.getElementById('div_update_password').style.display = 'block';
            }
            else{
                verify_otp.innerHTML = 'OTP Does not Match';
            }
        }
    });
    }

$('#update-password-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")
    let password = $('#password').val().trim();
    let c_password = $('#c_password').val().trim();
    if (password != c_password){
        alert("Password does not matched");
        return;
    }
    else {
        change_password();

    }
});

function change_password(){

    $.ajax({
        type : 'POST',
        url : '',
        data : {'csrfmiddlewaretoken':csrf,'email':$('#email').val().trim(),'action':'update-password','password':$('#password').val().trim()},
        success: function (result) {

            let message = result.data;
            if(message == 'User Does not Exist'){
                alert(message);
            }
            else {
                alert("Matched & Successfully Changed");
                window.location.href = login;
            }
        }
    });
    }
