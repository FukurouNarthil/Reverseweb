
// 1. Submit form
$(document).ready(function(){

	
	// 登录
    $('#login').click(function() {
        $.ajax({
            url: '/web/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
				if(response.success) {
					console.log(response);
					window.location = response.redirect;
				}
            },
            error: function(error) {
                
            }
        });
    });

    // 注册
    $('#signup').click(function() {
    	var password = $('input[name="password"]').val()
    	var confirm = $('input[name="confirm_password"]').val()

    	// 密码校验
    	if(password == confirm) {
    		$.ajax({
            	url: '/web/signup',
            	data: $('form').serialize(),
            	type: 'POST',
            	success: function(response) {
					// window.location = '/';
					if(response.success) {
						console.log(response);
						window.location = response.redirect;
					}
				},
            	error: function(error) {
               		console.log(error);
            	}
        	});
    	}
    	else {
    		$('.wrong-password').show();
    	}
    });

	$('#upload_file').click(function() {
        $.ajax({
            url: '/web/upload',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
				if(response.success) {
					console.log(response);
					window.location = response.redirect;
				}
            },
            error: function(error) {
                
            }
        });
    });
});