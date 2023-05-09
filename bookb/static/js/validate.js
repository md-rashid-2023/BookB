function validate(){
    let pwd1 = document.getElementById('password').value;

    let pwd2 = document.getElementById('psw-repeat').value;

    if (pwd1==pwd2){
        return true
    }
    else{
        document.getElementById('psw-repeat').style.border="1px solid red";
    }

    return false;

}