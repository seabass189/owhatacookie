function showAddress() {
  document.getElementById("address_div").className = ''
  document.getElementById('street_one').setAttribute('required', 'required')
  document.getElementById('street_two').setAttribute('required', 'required')
  document.getElementById('city').setAttribute('required', 'required')
  document.getElementById('state').setAttribute('required', 'required')
  document.getElementById('zip').setAttribute('required', 'required')
}

function hideAddress() {
  document.getElementById("address_div").className = 'hide'
  document.getElementById('street_one').setAttribute('required', '')
  document.getElementById('street_two').setAttribute('required', '')
  document.getElementById('city').setAttribute('required', '')
  document.getElementById('state').setAttribute('required', '')
  document.getElementById('zip').setAttribute('required', '')
}
