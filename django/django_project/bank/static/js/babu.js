
	$(document).ready(function()
	{	
	
	
	
				var url=window.location.href;
				//alert(url.substr(url.indexOf('?')+1));
						if (url.indexOf("bit") >= 0)
						{var emb='https://www.youtube.com/embed/';
						
			$('#rowbox').fadeOut(2000);
		   $("div#divLoading").addClass('show');
				var sub=(url.substr(url.indexOf('?')+1));
				sub = 'https://'+sub.replace("bit", "");
				//alert(sub);
				$.ajax({          
								 type : 'POST',
								url: '{% url 'you:index1' %}',
								dataType: "json",
								async: true,
							    // performing a POST request
							  data : {
								data1 : sub,
								csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
							  },
							  dataType: 'json',                   
							  success: function(response)         
							  {
               // document.getElementById("like-count").innerHTML = {{ like_count }};
			   //$('#below').html({{NameForm.your_name}});
			   $("#im").attr('src', emb+response[0].display);
			   $('#below').html( response[0].channel);
			  
			   $('#p').html(response[0].video_title);
			    $("div#divLoading").removeClass('show');
				$('#rowbox').fadeIn();
			   // $('#rowbox').show();
				
				var class_tr;
				var aftercross;
				$.each(response, function(i, item)
			 {
					if(response[i].ext=='m4a')
								{
								aftercross ='audio';}
						else
								{
								aftercross=aftercross = response[i].resolution.split("x").pop().trim()+'p';
								}
					if (i==0) {
								class_tr="info";
							} else if (i==1) {
								class_tr="success";
							}
							else if (i==2) {
								class_tr="danger";
							} 
							else if (i==3) {
								class_tr="info";
							} 
							else if (i==4) {
								class_tr="warning";
							} 
							else if (i==5) {
								class_tr="active";
							} 
							else if (i==6) {
								class_tr="success";
							} 
							else {
								class_tr="success";
							}
					if(i==0){	
					$("#id_tbody").html(
									
									'<tr class='+class_tr+'>'+
				
									"<td>" + response[i].resolution + "</td>"+
									"<td>" + response[i].format_note + "</td>"+
									"<td>" + response[i].ext + "</td>"+
									'<td><a href="'+response[i].url+'"class="btn btn-primary" download="2" role="button">'+aftercross+' Download  <a/></td></tr>');
									}
									
									else
									
									{
									
									$('<tr class='+class_tr+'>').html(
				
										
				
									"<td>" + response[i].resolution + "</td>"+
									"<td>" + response[i].format_note + "</td>"+
									"<td>" + response[i].ext + "</td>"+
									'<td><a href="'+response[i].url+'"class="btn btn-primary"  target="_blank" download="2" role="button">'+aftercross+' Download <a/></td>').appendTo('#id_table');
								
									}
								
								
					});

            },
			 error: function (data) { $('#below').html("<b>please retry or check url</b>");
			 $("div#divLoading").removeClass('show');
			 }
					});
				
				
			}
});
















	
	 $("#form").submit(function (ev)
	 {
							 // $("div#row").addClass('trans');
							//var text=$("#form").val();
							var emb='https://www.youtube.com/embed/'
							 $('#rowbox').fadeOut(2000);
							   $("div#divLoading").addClass('show');
							//$('#below').html(text);
							ev.preventDefault();
		$.ajax({
            type : 'POST',
            url: '{% url 'you:index' %}',
			dataType: "json",
			async: true,
			  data: $(this).serialize(),
           
            success: function (response) 
			{
               // document.getElementById("like-count").innerHTML = {{ like_count }};
			   $('#below').html({{NameForm.your_name}});
			   $("#im").attr('src', emb+response[0].display);
			   $('#below').html( response[0].channel);
			  
			   $('#p').html(response[0].video_title);
			     $("div#divLoading").removeClass('show');
				  $('#rowbox').fadeIn();
			   // $('#rowbox').show();
				
				var class_tr;
				var aftercross;
				$.each(response, function(i, item)
			 {
					if(response[i].ext=='m4a')
				{
								aftercross ='audio';}
						else
								{
								aftercross=aftercross = response[i].resolution.split("x").pop().trim()+'p';
								}
					if (i==0) {
								class_tr="info";
							} else if (i==1) {
								class_tr="success";
							}
							else if (i==2) {
								class_tr="danger";
							} 
							else if (i==3) {
								class_tr="info";
							} 
							else if (i==4) {
								class_tr="warning";
							} 
							else if (i==5) {
								class_tr="active";
							} 
							else if (i==6) {
								class_tr="success";
							} 
							else {
								class_tr="success";
							}
					if(i==0){	
					$("#id_tbody").html(
									
									'<tr class='+class_tr+'>'+
				
									"<td>" + response[i].resolution + "</td>"+
									"<td>" + response[i].format_note + "</td>"+
									"<td>" + response[i].ext + "</td>"+
									'<td><a href="'+response[i].url+'"class="btn btn-primary" download="2" role="button">'+aftercross+' Download  <a/></td></tr>');
									}
									
									else
									
									{
									
									$('<tr class='+class_tr+'>').html(
				
										
				
									"<td>" + response[i].resolution + "</td>"+
									"<td>" + response[i].format_note + "</td>"+
									"<td>" + response[i].ext + "</td>"+
									'<td><a href="'+response[i].url+'"class="btn btn-primary" target="_blank" download="2" role="button">'+aftercross+' Download <a/></td>').appendTo('#id_table');
								
									}
								
								
					});

            },
			 error: function (data) { $('#below').html("<b>please retry or check url</b>");
			 $("div#divLoading").removeClass('show');
			 }
        });

        
    });
	
