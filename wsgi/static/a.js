$(document).ready(function() {
	$("input").on("click",function(){
		$.post("/giverating", $("#ratingform").serialize(), function(data, status) {
			$('#tips').removeClass('novisible');
		});
	});

	$(document).on('keydown', function(e) {
		console.log(e.which);
		if (e.which == 68) {
			var href = $('li.next').children('a').attr("href");
			window.location.href = href;
		} else if (e.which == 65) {
			var href = $('li.previous').children('a').attr("href");
			window.location.href = href;
		}
	});
});
