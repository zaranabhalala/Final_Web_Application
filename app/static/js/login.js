function checkPassword(form) {

    strEmail = form.email.value.trim()
    strPassword = form.pswd.value.trim()


    //If name is left blank
    if (strEmail == '')
        alert("Please enter your Email.");
    else if (strPassword == '')
        alert("Please enter your password.");
    // If password not entered
    else
        return true;
    return false;
}