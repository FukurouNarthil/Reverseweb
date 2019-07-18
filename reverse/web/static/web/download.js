$(document).ready(function(){

	// 搜索
    $('#search').click(function() {
        var filename = $('input[name="filename"]').val();
    	$.ajax({
            	url: '/search?filename=' + $filename,
                // url: '/search',
            	data: $('form').serialize(),
            	type: 'GET',
            	success: function(response) {
            		$('#display-files').html(response);
	               	
            	},
            	error: function(error) {
               		console.log(error);
            	}
        	});
    });

    // 下载
    $('.download_url').click(function() {
        var $row = $(this).closest("tr");
        var $item = $row.find(".filename").text();
        window.open('/download/' + $item)
        $.ajax({
                url: '/download/' + $item,
                // data: $item,
                // type: 'POST',
                success: function(response) {
                    
                },
                error: function(error) {
                    console.log(error);
                }
            });
    });
});