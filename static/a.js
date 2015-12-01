$(document).ready(function() {
	$("input").on("click",function(){
		$.post("/giverating", $("#ratingform").serialize(), function(data, status) {
			console.log(data);
			$('#tips').removeClass('novisible');
		});
	});
});