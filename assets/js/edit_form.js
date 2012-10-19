$(document).ready(function(){
	var habitation_type = $('#id_habitation_type').val();
	var correspondance = ['apartment', 'house', '', '', '', '', '', 'parking', 'others'];
	function init_form(){
		$('.atom').each(function(evt){
			if(habitation_type != ''){
				if(!$(this).hasClass(correspondance[parseInt(habitation_type)])){
					$(this).hide()
					$(this).find(':input').val('').removeAttr('checked').removeAttr('selected')
				}else{
					$(this).show()
				}
			}
			else{
				if(!$(this).hasClass('base')){
					$(this).hide()
				}
			}
		})
	}
	$('#id_habitation_type').change(function(evt){
		habitation_type = $(this).val()
		init_form()
	})
	init_form();
	$('#pictures').insertBefore($("#description"));
})