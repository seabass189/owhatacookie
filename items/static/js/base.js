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
