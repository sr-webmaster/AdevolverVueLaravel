
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.min.js"></script>

<script>

$(function() {
  
	// $(".pause-adverts").click(pauseAdverts);

	// $(".enable-adverts").click(enableAdverts);

	//$(".datatable").dataTable();

	getNotifications();

	pollNotifications();

});



function pauseAdverts()
{
	var id = $(this).data("id");

	$("#status-button-" + id).html('<i class="fas fa-pause-circle adwords-paused"></i> <span class="icon-dropdown mdi mdi-chevron-down"></span>');
	
	
	$(this).unbind('click').addClass('text-muted').removeClass("font-weight-bold");

	$.post(
		"{{ url('user/pause-adverts') }}",
		{
			scope: $(this).data("scope"),
			id: $(this).data("id")
		}
	);

	//activate the enable link
	$("#enable-link-" + id).click(enableAdverts).removeClass('text-muted');

}

function enableAdverts()
{
	var id = $(this).data("id");

	$("#status-button-" + id).html('<i class="fas fa-circle adwords-enabled"></i> <span class="icon-dropdown mdi mdi-chevron-down"></span>');
	
	$(this).unbind('click').addClass('text-muted');

	$.post(
		"{{ url('user/enable-adverts') }}",
		{
			scope: $(this).data("scope"),
			id: $(this).data("id")
		}
	);
		
	$("#pause-link-" + id).click(pauseAdverts).removeClass('text-muted');
}

function pollNotifications()
{
	setTimeout(function() {
   
   	//	$.gritter.removeAll();//so we don't end up with copies of the same notification

    	getNotifications();

    	pollNotifications();

	}, 5000);
}

function getNotifications()
{
	$.getJSON(
    	"{{ url('user/notifications/unread') }}",
    	"",
    	function (data){

    		$.each(data, function(key, notification ){
    			addNotification(notification);
    		});
    		
    	}
    );
}

function addNotification(notification)
{
	
	$.gritter.add({
 
        text: notification.data.message,
        class_name: "clean",
        time: 6000,
        after_close: function(){
			
			markNotificationRead(notification);
		}
      });
	
}

function markNotificationRead(notification)
{
	$.post(
		"{{ url('user/notifications') }}",
		{
			id: notification.id
		},
		function(){

		}
	);
}


jQuery(function ($) {

	$("#close-sidebar").click(function() {
		$(".be-left-sidebar").addClass("sidebar-hidden");
		$(".be-content").addClass("content-full-width-sidebar-hidden");
		$("#show-sidebar").removeClass("show-sidebar-button-hidden");
		$("#show-sidebar").addClass("btn btn-sm btn-dark");
		// $("#right-sidebar").addClass("right-sidebar-left-sidebar-hidden");
		
	});

	$("#show-sidebar").click(function() {
		$(".be-left-sidebar").removeClass("sidebar-hidden");
		$(".be-content").removeClass("content-full-width-sidebar-hidden");
		$("#show-sidebar").addClass("show-sidebar-button-hidden");
		// $("#right-sidebar").removeClass("right-sidebar-left-sidebar-hidden");
	});

	$("#show-sidebar").mouseenter( function() {

		$("#show-sidebar").addClass("move-right");

	} ).mouseleave( function (){
	
		$("#show-sidebar").removeClass("move-right");

	} );


	setInterval(function (){

		if($(window).scrollTop() > 62) {
			$("#right-sidebar").addClass("right-sidebar-scrolled");
			
		}

		if($(window).scrollTop() < 63) {
			$("#right-sidebar").removeClass("right-sidebar-scrolled");
		}

	}, 500)

});



</script>


<script defer src="https://use.fontawesome.com/releases/v5.1.1/js/all.js" integrity="sha384-BtvRZcyfv4r0x/phJt9Y9HhnN5ur1Z+kZbKVgzVBAlQZX4jvAuImlIz+bG7TS00a" crossorigin="anonymous"></script>
