//
// formVerify.js
// Description:
// This file handles form verification
//
// Contents:
// -password verification
// -email verification
// -captcha captcha callback
// -alphanumeric verification
//

// This function verifies that the passwords match
function passVerify() {
  const createdPass = document.getElementById('passInit').value; // created password
  const confirmPass = document.getElementById('passConfirm').value; // password confirmed

  if (confirmPass != '' && !(confirmPass === createdPass)) {
    // if the passwords are not enpty and not equal
    // alert("not same dude");
    document.getElementById('passError').innerHTML = 'Passwords do not match';
  } else {
    //passwords match
    document.getElementById('passError').innerHTML = null;
  }
}

// This function clears the error displayed
function clearError() {
  document.getElementById('emailError').innerHTML = null;
}

// This function verifies that the email is a sfsu account
function emailCheck() {
  const emailSuffix1 = '@sfsu.edu'; // suffix to check if its a sfsu account
  const emailSuffix2 = '@mail.sfsu.edu'; // second suffix
  const emailInput = document.getElementById('emailAddress').value; // gets value in the texbox

  if (
    emailInput != '' &&
    emailInput.match(emailSuffix1) == null &&
    emailInput.match(emailSuffix2) == null
  ) {
    // if filled out and isn"t sfsu account
    document.getElementById('emailError').innerHTML = 'Must be a sfsu email'; // error shows
  } else if (emailInput != '') {
    // filled out and is a sfsu account
    document.getElementById('emailError').innerHTML = null; // accepted and error removed
  } else {
    // empty case so error won"t be presented
    document.getElementById('emailError').innerHTML = null;
  }
}

// This function checks if there are any empty fields(not used as of right now)
function emptyFieldCheck() {
  const fName = document.getElementById('firstName').value;
  const lName = document.getElementById('lastName').value;
  const userName = document.getElementById('userName').value;
  const email = document.getElementById('emailAddress').value;
  const passCreated = document.getElementById('passInit').value;
  const passVerify = document.getElementById('passVerify').value;
}

// This function enables the submit button after captcha has completed
function captchaCallback() {
  document.getElementById('submitButton').removeAttribute('disabled');
}

// This function checks if the text input is alphanumeric (A-Z both cases, 0-9, no special characters)
function alphaNumericCheck(element) {
  const input_text = document.getElementById(element).value; //gets input text from provided element
  // alert(input_text);
  if (input_text.match(/[\s~`!@#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?()\._]/)) {
    // console.log('no');
    alert('Please enter only alphanumerics');
    return false;
  }
  if (
    input_text.match(/^[a-z0-9]+$/i) ||
    input_text.match(/\s/) ||
    !input_text
  ) {
    // input is good
    // alert('correct');
    return true;
  } else {
    // input contains invalid characters
    alert('Please enter only alphanumerics');
    return false;
  }
}

// this function checks for invalid characters
function specialCharCheck(element) {
  const input_text = document.getElementById(element).value; //gets input text from provided element
  if (input_text.match(/[\s~`!#$%\^&*+=\-\[\]\\';,/{}|\\":<>\?()_]/)) {
    // console.log('no');
    alert('Invalid character in email');
    return false;
  }
}
