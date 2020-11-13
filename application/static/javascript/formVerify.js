function passVerify() {
  const createdPass = document.getElementById('passInit').value;
  const confirmPass = document.getElementById('passConfirm').value;

  if (confirmPass != '' && !(confirmPass === createdPass)) {
    // alert("not same dude");
    document.getElementById('passError').innerHTML = 'Passwords do not match';
  } else {
    document.getElementById('passError').innerHTML = null;
  }
}

function clearError() {
  document.getElementById('emailError').innerHTML = null;
}

function emailCheck() {
  const emailSuffix1 = '@sfsu.edu'; //suffix to check if its a sfsu account
  const emailSuffix2 = '@mail.sfsu.edu';
  const emailInput = document.getElementById('emailAddress').value; //gets value in the texbox

  if (
    emailInput != '' &&
    emailInput.match(emailSuffix1) == null &&
    emailInput.match(emailSuffix2) == null
  ) {
    //if filled out and isn"t sfsu account
    document.getElementById('emailError').innerHTML = 'Must be a sfsu email'; //error shows
  } else if (emailInput != '') {
    //filled out and is a sfsu account
    document.getElementById('emailError').innerHTML = null; //accepted and error removed
  } else {
    //empty case so error won"t be presented
    document.getElementById('emailError').innerHTML = null;
  }
}

function emptyFieldCheck() {
  const fName = document.getElementById('firstName').value;
  const lName = document.getElementById('lastName').value;
  const userName = document.getElementById('userName').value;
  const email = document.getElementById('emailAddress').value;
  const passCreated = document.getElementById('passInit').value;
  const passVerify = document.getElementById('passVerify').value;
}

function captchaCallback() {
  document.getElementById('submitButton').removeAttribute('disabled');
}

function alphaNumericCheck(element) {
  const input_text = document.getElementById(element).value; //gets input text from provided element
  // alert(input_text);
  if (!input_text.match(/^[a-z0-9]+$/i | /^+$/)) { // if input contains characters
    alert('Please enter only alphanumerics');
    return false;
  } else { // input is good
    // alert('correct');
    return true;
  }
}
