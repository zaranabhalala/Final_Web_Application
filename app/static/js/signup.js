function checkPassword(form) {
    password1 = form.pswd.value.trim();
    password2 = form.pswd2.value.trim();

    // If name is blank
    if (form.name.value.trim() == '')
        alert("Please enter your name.");
    else if (form.email.value.trim() == '')
        alert("Please enter your email.");

    // If password not entered
    else if (password1 == '')
        alert("Please enter Password");

    // If confirm password not entered
    else if (password2 == '')
        alert("Please enter confirm password");

    // If Not same return False.
    else if (password1 != password2)
        alert("\nPassword did not match: Please try again...")
    // If same return True.
    else {
        return true;
    }
    return false;
}