$(document).ready(function() {
  $('.accordion-toggle').click(function () {
    var icon = $(this).find(".icon-chevron");
    if(icon.hasClass('icon-chevron-down')){
        icon.removeClass('icon-chevron-down').addClass('icon-chevron-right')
    }else{
        icon.removeClass('icon-chevron-right').addClass('icon-chevron-down')
    }
  })
})