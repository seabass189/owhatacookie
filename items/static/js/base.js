// let btn = document.querySelector('#home-btn')
//
// btn.addEventListener('click', function() {
//   alert('ow!! that smarts!')
// })
//
// let secretBtn = document.querySelector('#secret-btn')


$(document).ready(function(){
  $("#secret-button").click(function(){
    $('#secret-text').fadeIn("slow");
  });
});
