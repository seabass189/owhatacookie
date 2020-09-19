// this will literally just run once, and then it will leave a cookie and never run again
$(document).ready(function () {
  if(Cookies.get("scriptExecuted")!="yes") {
    $('#title-span').hide()
    $('#title-span').fadeIn(3000);
    //Scroll div you the bottom onpage load
    // $("#divTest").scrollTop($("#divTest")[0].scrollHeight);
    Cookies.set("scriptExecuted", "yes");
  }
});

// CART BUTTON
let cartBtn = document.querySelector('#cart-btn')

cartBtn.addEventListener('mouseover', function(e) {
  let cartImg = document.querySelector('#cart-img')
  cartImg.src = 'static/images/cart-white.png'
})

cartBtn.addEventListener('mouseout', function(e) {
  let cartImg = document.querySelector('#cart-img')
  cartImg.src = 'static/images/cart.png'
})
