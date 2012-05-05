$(document).ready(function(){
	/* move map to the right location */
	//$('#div_id_location').appendTo($("#maps"))
		
	$('.atom_content').each(function(index) {
		if($(this).find('.has_value').length == 0){
			$(this).hide('fast')
		}else {
			$(this).parent().find('.icon').removeClass('plus').addClass('cross')
			$(this).parent().find('.extend').html('-')
		}
	})
	$('.extend').click(function(evt){
		if($(this).html() == '+'){
			$(this).html('-')
			$(this).parent().next().show('fast')
		}else{
			$(this).html('+')
			$(this).parent().next().find(':input').val('').removeAttr('checked').removeAttr('selected')
			$(this).parent().next().hide('fast')
		}
		evt.stopPropagation()
	})
	$('.atom_title').click(function(evt){ 
		$(this).find('.extend').trigger('click')
	})

});
$(function (){
	$('.result_header a').click(function(evt){
		$("#search").attr('action', $(this).attr('href'))
		$("#search").submit()
		return false
	})
});