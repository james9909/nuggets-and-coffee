$("#login-form").submit(function(e) {
    e.preventDefault();
    var data = $(this).serializeObject();
    console.log(data);
    api_call("POST", "/login", data, function(result) {
        console.log(result);
        if (result.success) {
            window.location.href = "/";
        } else {
            $.notify(result.message, "error");
        }
    });
});

$("#register-form").submit(function(e) {
    e.preventDefault();
    var data = $(this).serializeObject();
    api_call("POST", "/register", data, function(result) {
        console.log(result);
        if (result.success) {
            $.notify(result.message, "success");
        } else {
            $.notify(result.message, "error");
        }
    });
});
