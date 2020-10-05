let delivery = document.getElementById('set-delivery')
let pickup = document.getElementById('set-pickup')
let confirmBtn = document.getElementById('confirm-btn')

delivery.addEventListener('click', function(){
  confirmBtn.className = 'checkout-btn'
  document.getElementById("address_div").className = ''
  document.getElementById('street_one').setAttribute('required', 'required')
  document.getElementById('street_two').setAttribute('required', 'required')
  document.getElementById('city').setAttribute('required', 'required')
  document.getElementById('state').setAttribute('required', 'required')
  document.getElementById('zip').setAttribute('required', 'required')
})

pickup.addEventListener('click', function(){
  confirmBtn.disabled = false
  confirmBtn.className = 'checkout-btn'
  document.getElementById("address_div").className = 'hide'
  document.getElementById('street_one').setAttribute('required', '')
  document.getElementById('street_two').setAttribute('required', '')
  document.getElementById('city').setAttribute('required', '')
  document.getElementById('state').setAttribute('required', '')
  document.getElementById('zip').setAttribute('required', '')
})

confirmBtn.addEventListener('click', function(){
  if (confirmBtn.disabled === false) {
    document.getElementById('checkout-form').submit()
    alert('uh oh')
  }
})
