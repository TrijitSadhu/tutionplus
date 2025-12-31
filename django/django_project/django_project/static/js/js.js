$(document).ready(function(){
    // $('#rowbox').hide();
   // $("#submit").click(function(){
     // $('#below').html("2");
	    
      
//});
});
 $("#form").submit(function (ev) {
        ev.preventDefault();
		$.ajax({
            type : "POST",
            //url: "{% url 'index' %}",
			url:app.init("{% url 'query' %}");
            //data: frm{{ post.id }}.serialize(),
			//data: $(this).serialize(),
			data: { csrfmiddlewaretoken: '{{ csrf_token }}'}
            success: function (data) {
               // document.getElementById("like-count").innerHTML = {{ like_count }};
			   $('#below').html("new");
            },
			 error: function (data) { $('#below').html("error");}
        });

        ev.preventDefault();
    });